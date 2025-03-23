package main

import (
	"context"
	"crypto/sha1"
	"fmt"
	"log"
	"math/big"
	"sync"
	"time"

	pb "chord/protocol" // Update as needed
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

// Node represents a node in the Chord DHT
type Node struct {
	pb.UnimplementedChordServer
	mu sync.RWMutex

	Address     string
	Predecessor string
	Successors  []string
	FingerTable []string

	Bucket map[string]string
}

// get the sha1 hash of a string as a bigint
func hash(elt string) *big.Int {
	hasher := sha1.New()
	hasher.Write([]byte(elt))
	return new(big.Int).SetBytes(hasher.Sum(nil))
}

// calculate the address of a point somewhere across the ring
// this gets the target point for a given finger table entry
// the successor of this point is the finger table entry
func jump(address string, fingerentry int) *big.Int {
	n := hash(address)

	fingerentryminus1 := big.NewInt(int64(fingerentry) - 1)
	distance := new(big.Int).Exp(two, fingerentryminus1, nil)

	sum := new(big.Int).Add(n, distance)

	return new(big.Int).Mod(sum, hashMod)
}

// returns true if elt is between start and end, accounting for the right
// if inclusive is true, it can match the end
func between(start, elt, end *big.Int, inclusive bool) bool {
	if end.Cmp(start) > 0 {
		return (start.Cmp(elt) < 0 && elt.Cmp(end) < 0) || (inclusive && elt.Cmp(end) == 0)
	} else {
		return start.Cmp(elt) < 0 || elt.Cmp(end) < 0 || (inclusive && elt.Cmp(end) == 0)
	}
}

// Ping implements the Ping RPC method
func (n *Node) Ping(ctx context.Context, req *pb.PingRequest) (*pb.PingResponse, error) {
	log.Print("ping: received request")
	return &pb.PingResponse{}, nil
}

// Put implements the Put RPC method
func (n *Node) Put(ctx context.Context, req *pb.PutRequest) (*pb.PutResponse, error) {
	n.mu.Lock()
	defer n.mu.Unlock()
	log.Print("put: [", req.Key, "] => [", req.Value, "]")
	n.Bucket[req.Key] = req.Value
	return &pb.PutResponse{}, nil
}

// Get implements the Get RPC method
func (n *Node) Get(ctx context.Context, req *pb.GetRequest) (*pb.GetResponse, error) {
	n.mu.RLock()
	defer n.mu.RUnlock()
	value, exists := n.Bucket[req.Key]
	if !exists {
		log.Print("get: [", req.Key, "] miss")
		return &pb.GetResponse{Value: ""}, nil
	}
	log.Print("get: [", req.Key, "] found [", value, "]")
	return &pb.GetResponse{Value: value}, nil
}

// Delete implements the Delete RPC method
func (n *Node) Delete(ctx context.Context, req *pb.DeleteRequest) (*pb.DeleteResponse, error) {
	n.mu.Lock()
	defer n.mu.Unlock()
	if _, exists := n.Bucket[req.Key]; exists {
		log.Print("delete: found and deleted [", req.Key, "]")
		delete(n.Bucket, req.Key)
	} else {
		log.Print("delete: not found [", req.Key, "]")
	}
	return &pb.DeleteResponse{}, nil
}

// GetAll implements the GetAll RPC method
func (n *Node) GetAll(ctx context.Context, req *pb.GetAllRequest) (*pb.GetAllResponse, error) {
	n.mu.RLock()
	defer n.mu.RUnlock()
	log.Printf("getall: returning %d key-value pairs", len(n.Bucket))

	// Create a copy of the bucket map
	keyValues := make(map[string]string)
	for k, v := range n.Bucket {
		keyValues[k] = v
	}

	return &pb.GetAllResponse{KeyValues: keyValues}, nil
}

func (n *Node) checkPredecessor() {
	// TODO: Student will implement this
}

func (n *Node) stabilize() {
    n.mu.Lock()
    successor := n.Successors[0] // Get first successor
    n.mu.Unlock()

    if successor == n.Address {
        // If we're our own successor (only one node in the ring), nothing to do
        return
    }

    // Contact successor to get its predecessor
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
            // If the predecessor of our successor is a better fit, update successor
            log.Printf("stabilize: updating successor from %s to %s", successor, pred)
            n.mu.Lock()
            n.Successors[0] = pred
            n.mu.Unlock()
        }
    }

    // Notify our (possibly updated) successor that we exist
    notifyCtx, notifyCancel := context.WithTimeout(context.Background(), time.Second)
    defer notifyCancel()

    _, err = client.Notify(notifyCtx, &pb.NotifyRequest{Address: n.Address})
    if err != nil {
        log.Printf("stabilize: notify failed: %v", err)
    }
}

func (n *Node) Notify(ctx context.Context, req *pb.NotifyRequest) (*pb.NotifyResponse, error) {
    n.mu.Lock()
    defer n.mu.Unlock()

    if n.Predecessor == "" || between(hash(n.Predecessor), hash(req.Address), hash(n.Address), false) {
        log.Printf("notify: updating predecessor from %s to %s", n.Predecessor, req.Address)
        n.Predecessor = req.Address
    }

    return &pb.NotifyResponse{}, nil
}

// GetPredecessorAndSuccessors returns the predecessor and successors list
func (n *Node) GetPredecessorAndSuccessors(ctx context.Context, req *pb.GetPredecessorAndSuccessorsRequest) (*pb.GetPredecessorAndSuccessorsResponse, error) {
	n.mu.RLock()
	defer n.mu.RUnlock()

	// Ensure we return a valid successor list (minimum 1)
	var successors []string
	if len(n.Successors) > 0 {
		successors = append(successors, n.Successors...)
	}

	return &pb.GetPredecessorAndSuccessorsResponse{
		Predecessor: n.Predecessor,
		Successors:  successors,
	}, nil
}

func (n *Node) fixFingers(nextFinger int) int {
	// TODO: Student will implement this
	nextFinger++
	if nextFinger > keySize {
		nextFinger = 1
	}
	return nextFinger
}

func (n *Node) closestPrecedingNode(id *big.Int) string {
    selfID := hash(n.Address)
    for i := keySize; i >= 1; i-- {
        finger := n.FingerTable[i]
        if finger != "" && between(selfID, hash(finger), id, false) {
            return finger
        }
    }
    return n.Successors[0] // fallback
}

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

    // Otherwise, forward to closest preceding node
    next := n.closestPrecedingNode(id)
    return &pb.FindSuccessorResponse{Address: next}, nil
}

// format an address for printing
func addr(a string) string {
	if a == "" {
		return "(empty)"
	}
	s := fmt.Sprintf("%040x", hash(a))
	return s[:8] + ".. (" + a + ")"
}

// print useful info about the local node
func (n *Node) dump() {
	n.mu.RLock()
	defer n.mu.RUnlock()

	fmt.Println()
	fmt.Println("Dump: information about this node")

	// predecessor and successor links
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
