package main

import (
	"context"
	"crypto/sha1"
	"fmt"
	"log"
	"math/big"
	"sync"
	"time"

	pb "chord/protocol"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

const (
	defaultPort       = "3410"
	successorListSize = 3
	keySize           = sha1.Size * 8
	maxLookupSteps    = 32
)

var (
	two     = big.NewInt(2)
	hashMod = new(big.Int).Exp(big.NewInt(2), big.NewInt(keySize), nil)
)

// Node represents a node in the Chord DHT.
type Node struct {
	pb.UnimplementedChordServer
	mu sync.RWMutex

	Address     string
	Predecessor string
	Successors  []string
	FingerTable []string

	Bucket map[string]string
}

// hash computes the sha1 hash of a string as a big.Int.
func hash(elt string) *big.Int {
	hasher := sha1.New()
	hasher.Write([]byte(elt))
	return new(big.Int).SetBytes(hasher.Sum(nil))
}

// jump calculates the address for a finger table entry.
func jump(address string, fingerentry int) *big.Int {
	n := hash(address)
	fingerentryminus1 := big.NewInt(int64(fingerentry) - 1)
	distance := new(big.Int).Exp(two, fingerentryminus1, nil)
	sum := new(big.Int).Add(n, distance)
	return new(big.Int).Mod(sum, hashMod)
}

// between returns true if elt is between start and end on the ring.
func between(start, elt, end *big.Int, inclusive bool) bool {
	if end.Cmp(start) > 0 {
		return (start.Cmp(elt) < 0 && elt.Cmp(end) < 0) || (inclusive && elt.Cmp(end) == 0)
	} else {
		return start.Cmp(elt) < 0 || elt.Cmp(end) < 0 || (inclusive && elt.Cmp(end) == 0)
	}
}

// Ping is a simple health check.
func (n *Node) Ping(ctx context.Context, req *pb.PingRequest) (*pb.PingResponse, error) {
	//log.Print("ping: received request")
	return &pb.PingResponse{}, nil
}

// Put stores a key-value pair in the node’s bucket.
func (n *Node) Put(ctx context.Context, req *pb.PutRequest) (*pb.PutResponse, error) {
	n.mu.Lock()
	defer n.mu.Unlock()
	log.Printf("put: [%s] => [%s]", req.Key, req.Value)
	n.Bucket[req.Key] = req.Value
	return &pb.PutResponse{}, nil
}

// Get retrieves a value for a key.
func (n *Node) Get(ctx context.Context, req *pb.GetRequest) (*pb.GetResponse, error) {
	n.mu.RLock()
	defer n.mu.RUnlock()
	value, exists := n.Bucket[req.Key]
	if !exists {
		log.Printf("get: [%s] miss", req.Key)
		return &pb.GetResponse{Value: ""}, nil
	}
	log.Printf("get: [%s] found [%s]", req.Key, value)
	return &pb.GetResponse{Value: value}, nil
}

// Delete removes a key from the bucket.
func (n *Node) Delete(ctx context.Context, req *pb.DeleteRequest) (*pb.DeleteResponse, error) {
	n.mu.Lock()
	defer n.mu.Unlock()
	if _, exists := n.Bucket[req.Key]; exists {
		log.Printf("delete: found and deleted [%s]", req.Key)
		delete(n.Bucket, req.Key)
	} else {
		log.Printf("delete: not found [%s]", req.Key)
	}
	return &pb.DeleteResponse{}, nil
}

// GetAll returns all key-value pairs.
func (n *Node) GetAll(ctx context.Context, req *pb.GetAllRequest) (*pb.GetAllResponse, error) {
	n.mu.RLock()
	defer n.mu.RUnlock()
	log.Printf("getall: returning %d key-value pairs", len(n.Bucket))
	keyValues := make(map[string]string)
	for k, v := range n.Bucket {
		keyValues[k] = v
	}
	return &pb.GetAllResponse{KeyValues: keyValues}, nil
}

// checkPredecessor pings the predecessor and resets it if unreachable.
func (n *Node) checkPredecessor() {
	n.mu.RLock()
	pred := n.Predecessor
	n.mu.RUnlock()
	if pred == "" || pred == n.Address {
		return
	}
	conn, err := grpc.Dial(pred, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Printf("checkPredecessor: failed to connect to %s: %v", pred, err)
		n.mu.Lock()
		n.Predecessor = ""
		n.mu.Unlock()
		return
	}
	defer conn.Close()
	client := pb.NewChordClient(conn)
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()
	_, err = client.Ping(ctx, &pb.PingRequest{})
	if err != nil {
		log.Printf("checkPredecessor: ping to %s failed: %v", pred, err)
		n.mu.Lock()
		n.Predecessor = ""
		n.mu.Unlock()
	}
}

// stabilize maintains the successor pointer and notifies the successor.
func (n *Node) stabilize() {
	n.mu.Lock()
	successor := n.Successors[0]
	n.mu.Unlock()

	if successor == n.Address {
		return
	}

	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	conn, err := grpc.Dial(successor, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Printf("stabilize: failed to connect to successor %s: %v", successor, err)
		return
	}
	defer conn.Close()

	client := pb.NewChordClient(conn)
	response, err := client.GetPredecessorAndSuccessors(ctx, &pb.GetPredecessorAndSuccessorsRequest{})
	if err != nil {
		log.Printf("stabilize: failed to get predecessor from successor %s: %v", successor, err)
		return
	}

	pred := response.Predecessor
	if pred != "" && pred != n.Address {
		predID := hash(pred)
		selfID := hash(n.Address)
		succID := hash(successor)
		if between(selfID, predID, succID, false) {
			log.Printf("stabilize: updating successor from %s to %s", successor, pred)
			n.mu.Lock()
			n.Successors[0] = pred
			n.mu.Unlock()
		}
	}

	notifyCtx, notifyCancel := context.WithTimeout(context.Background(), time.Second)
	defer notifyCancel()

	_, err = client.Notify(notifyCtx, &pb.NotifyRequest{Address: n.Address})
	if err != nil {
		log.Printf("stabilize: notify failed: %v", err)
	}
}

// Notify is invoked by another node to suggest a new predecessor.
func (n *Node) Notify(ctx context.Context, req *pb.NotifyRequest) (*pb.NotifyResponse, error) {
	n.mu.Lock()
	defer n.mu.Unlock()
	if n.Predecessor == "" || between(hash(n.Predecessor), hash(req.Address), hash(n.Address), false) {
		log.Printf("notify: updating predecessor from %s to %s", n.Predecessor, req.Address)
		n.Predecessor = req.Address
	}
	return &pb.NotifyResponse{}, nil
}

// GetPredecessorAndSuccessors returns the predecessor and successors list.
func (n *Node) GetPredecessorAndSuccessors(ctx context.Context, req *pb.GetPredecessorAndSuccessorsRequest) (*pb.GetPredecessorAndSuccessorsResponse, error) {
	n.mu.RLock()
	defer n.mu.RUnlock()
	var successors []string
	if len(n.Successors) > 0 {
		successors = append(successors, n.Successors...)
	}
	return &pb.GetPredecessorAndSuccessorsResponse{
		Predecessor: n.Predecessor,
		Successors:  successors,
	}, nil
}

// fixFingers updates one finger table entry per call.
func (n *Node) fixFingers(nextFinger int) int {
	nextFinger++
	if nextFinger > keySize {
		nextFinger = 1
	}

	id := jump(n.Address, nextFinger)
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	client := pb.NewChordClient(grpcClient(n.Successors[0]))
	res, err := client.FindSuccessor(ctx, &pb.FindSuccessorRequest{Id: id.String()})
	if err != nil {
		log.Printf("fixFingers: failed to find successor for finger[%d]: %v", nextFinger, err)
		return nextFinger
	}

	n.mu.Lock()
	n.FingerTable[nextFinger] = res.Address
	n.mu.Unlock()

	//log.Printf("fixFingers: updated finger[%d] to %s", nextFinger, res.Address)
	return nextFinger
}

// grpcClient creates a new gRPC client connection.
func grpcClient(address string) *grpc.ClientConn {
	conn, err := grpc.Dial(address, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("grpcClient: failed to dial %s: %v", address, err)
	}
	return conn
}

// closestPrecedingNode returns the best finger preceding the target id.
func (n *Node) closestPrecedingNode(id *big.Int) string {
	selfID := hash(n.Address)
	for i := keySize; i >= 1; i-- {
		finger := n.FingerTable[i]
		if finger != "" && between(selfID, hash(finger), id, false) {
			return finger
		}
	}
	return n.Successors[0]
}

// FindSuccessor implements the core lookup: it returns the successor of a given id.
func (n *Node) FindSuccessor(ctx context.Context, req *pb.FindSuccessorRequest) (*pb.FindSuccessorResponse, error) {
	id := new(big.Int)
	id.SetString(req.Id, 10)

	n.mu.RLock()
	selfID := hash(n.Address)
	succID := hash(n.Successors[0])
	n.mu.RUnlock()

	if between(selfID, id, succID, true) {
		return &pb.FindSuccessorResponse{Address: n.Successors[0]}, nil
	}

	next := n.closestPrecedingNode(id)
	return &pb.FindSuccessorResponse{Address: next}, nil
}

// addr formats an address (and its hash) for printing.
func addr(a string) string {
	if a == "" {
		return "(empty)"
	}
	s := fmt.Sprintf("%040x", hash(a))
	return s[:8] + ".. (" + a + ")"
}

// dump prints the node’s state (neighbors, finger table, and stored keys).
func (n *Node) dump() {
	n.mu.RLock()
	defer n.mu.RUnlock()

	fmt.Println()
	fmt.Println("Dump: information about this node")
	fmt.Println("Neighborhood")
	fmt.Println("pred:   ", addr(n.Predecessor))
	fmt.Println("self:   ", addr(n.Address))
	for i, succ := range n.Successors {
		fmt.Printf("succ  %d: %s\n", i, addr(succ))
	}
	fmt.Println()
	fmt.Println("Finger table")
	i := 1
	for i <= keySize {
		for i < keySize && n.FingerTable[i] == n.FingerTable[i+1] {
			i++
		}
		fmt.Printf(" [%3d]: %s\n", i, addr(n.FingerTable[i]))
		i++
	}
	fmt.Println()
	fmt.Println("Data items")
	for k, v := range n.Bucket {
		s := fmt.Sprintf("%040x", hash(k))
		fmt.Printf("    %s.. %s => %s\n", s[:8], k, v)
	}
	fmt.Println()
}
