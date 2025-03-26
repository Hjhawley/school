package main

import (
	"context"
	"crypto/sha1"
	"fmt"
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

func between(start, elt, end *big.Int, inclusive bool) bool {
	if end.Cmp(start) > 0 {
		return (start.Cmp(elt) < 0 && elt.Cmp(end) < 0) || (inclusive && elt.Cmp(end) == 0)
	} else {
		return start.Cmp(elt) < 0 || elt.Cmp(end) < 0 || (inclusive && elt.Cmp(end) == 0)
	}
}

func (n *Node) Ping(ctx context.Context, req *pb.PingRequest) (*pb.PingResponse, error) {
	return &pb.PingResponse{}, nil
}

func (n *Node) Put(ctx context.Context, req *pb.PutRequest) (*pb.PutResponse, error) {
	n.mu.Lock()
	defer n.mu.Unlock()
	n.Bucket[req.Key] = req.Value
	return &pb.PutResponse{}, nil
}

func (n *Node) Get(ctx context.Context, req *pb.GetRequest) (*pb.GetResponse, error) {
	n.mu.RLock()
	defer n.mu.RUnlock()
	value, exists := n.Bucket[req.Key]
	if !exists {
		return &pb.GetResponse{Value: ""}, nil
	}
	return &pb.GetResponse{Value: value}, nil
}

func (n *Node) Delete(ctx context.Context, req *pb.DeleteRequest) (*pb.DeleteResponse, error) {
	n.mu.Lock()
	defer n.mu.Unlock()
	delete(n.Bucket, req.Key)
	return &pb.DeleteResponse{}, nil
}

func (n *Node) GetAll(ctx context.Context, req *pb.GetAllRequest) (*pb.GetAllResponse, error) {
	n.mu.RLock()
	defer n.mu.RUnlock()
	copy := make(map[string]string)
	for k, v := range n.Bucket {
		copy[k] = v
	}
	return &pb.GetAllResponse{KeyValues: copy}, nil
}

func (n *Node) PutAll(ctx context.Context, req *pb.PutAllRequest) (*pb.PutAllResponse, error) {
	n.mu.Lock()
	defer n.mu.Unlock()
	for k, v := range req.KeyValues {
		n.Bucket[k] = v
	}
	return &pb.PutAllResponse{}, nil
}

func (n *Node) GetSome(ctx context.Context, req *pb.GetSomeRequest) (*pb.GetSomeResponse, error) {
	n.mu.Lock()
	defer n.mu.Unlock()

	predID := hash(req.Address)
	selfID := hash(n.Address)

	transfer := make(map[string]string)
	keep := make(map[string]string)

	for k, v := range n.Bucket {
		keyID := hash(k)
		if between(predID, keyID, selfID, true) {
			transfer[k] = v
		} else {
			keep[k] = v
		}
	}
	n.Bucket = keep
	return &pb.GetSomeResponse{KeyValues: transfer}, nil
}

func (n *Node) checkPredecessor() {
	n.mu.RLock()
	pred := n.Predecessor
	n.mu.RUnlock()
	if pred == "" || pred == n.Address {
		return
	}
	conn, err := grpc.Dial(pred, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
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
		n.mu.Lock()
		n.Predecessor = ""
		n.mu.Unlock()
	}
}

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
		return
	}
	defer conn.Close()
	client := pb.NewChordClient(conn)
	response, err := client.GetPredecessorAndSuccessors(ctx, &pb.GetPredecessorAndSuccessorsRequest{})
	if err != nil {
		return
	}
	pred := response.Predecessor
	if pred != "" && pred != n.Address {
		predID := hash(pred)
		selfID := hash(n.Address)
		succID := hash(successor)
		if between(selfID, predID, succID, false) {
			n.mu.Lock()
			n.Successors[0] = pred
			n.mu.Unlock()
		}
	}
	notifyCtx, notifyCancel := context.WithTimeout(context.Background(), time.Second)
	defer notifyCancel()
	_, _ = client.Notify(notifyCtx, &pb.NotifyRequest{Address: n.Address})
}

func (n *Node) Notify(ctx context.Context, req *pb.NotifyRequest) (*pb.NotifyResponse, error) {
	n.mu.Lock()
	defer n.mu.Unlock()
	if n.Predecessor == "" || between(hash(n.Predecessor), hash(req.Address), hash(n.Address), false) {
		n.Predecessor = req.Address
	}
	return &pb.NotifyResponse{}, nil
}

func (n *Node) GetPredecessorAndSuccessors(ctx context.Context, req *pb.GetPredecessorAndSuccessorsRequest) (*pb.GetPredecessorAndSuccessorsResponse, error) {
	n.mu.RLock()
	defer n.mu.RUnlock()
	copy := make([]string, len(n.Successors))
	copy = append(copy[:0], n.Successors...)
	return &pb.GetPredecessorAndSuccessorsResponse{
		Predecessor: n.Predecessor,
		Successors:  copy,
	}, nil
}

func (n *Node) FindSuccessor(ctx context.Context, req *pb.FindSuccessorRequest) (*pb.FindSuccessorResponse, error) {
	id := new(big.Int).SetBytes(req.Id)
	n.mu.RLock()
	selfID := hash(n.Address)
	succID := hash(n.Successors[0])
	n.mu.RUnlock()

	if between(selfID, id, succID, true) {
		return &pb.FindSuccessorResponse{Found: true, NextAddress: n.Successors[0]}, nil
	} else {
		return &pb.FindSuccessorResponse{Found: false, NextAddress: n.Successors[0]}, nil
	}
}

func addr(a string) string {
	if a == "" {
		return "(empty)"
	}
	s := fmt.Sprintf("%040x", hash(a))
	return s[:8] + ".. (" + a + ")"
}

func (n *Node) dump() {
	n.mu.RLock()
	defer n.mu.RUnlock()
	fmt.Println("\nDump: information about this node")
	fmt.Println("Neighborhood")
	fmt.Println("pred:   ", addr(n.Predecessor))
	fmt.Println("self:   ", addr(n.Address))
	for i, succ := range n.Successors {
		fmt.Printf("succ  %d: %s\n", i, addr(succ))
	}
	fmt.Println("\nData items")
	for k, v := range n.Bucket {
		s := fmt.Sprintf("%040x", hash(k))
		fmt.Printf("    %s.. %s => %s\n", s[:8], k, v)
	}
	fmt.Println()
}
