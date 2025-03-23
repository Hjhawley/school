package main

import (
	"bufio"
	"context"
	"crypto/rand"
	"encoding/hex"
	"flag"
	"fmt"
	"io"
	"log"
	"net"
	"os"
	"strconv"
	"strings"
	"time"

	pb "chord/protocol"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

var localaddress string

// init finds the local IP address.
func init() {
	log.SetFlags(log.Lshortfile | log.Ltime)
	conn, err := net.Dial("udp", "8.8.8.8:80")
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()

	localAddr := conn.LocalAddr().(*net.UDPAddr)
	localaddress = localAddr.IP.String()

	if localaddress == "" {
		panic("init: failed to find non-loopback interface with valid address on this node")
	}
	log.Printf("found local address %s\n", localaddress)
}

// resolveAddress handles shorthand address formats.
func resolveAddress(address string) string {
	if strings.HasPrefix(address, ":") {
		return net.JoinHostPort(localaddress, address[1:])
	} else if !strings.Contains(address, ":") {
		return net.JoinHostPort(address, defaultPort)
	}
	return address
}

// StartServer initializes the node and RPC server.
// If joining an existing ring, it also attempts to fetch key-value pairs.
func StartServer(address string, nprime string) (*Node, error) {
	address = resolveAddress(address)

	node := &Node{
		Address:     address,
		FingerTable: make([]string, keySize+1),
		Predecessor: "",
		Successors:  nil,
		Bucket:      make(map[string]string),
	}

	if nprime == "" {
		log.Print("StartServer: creating new ring")
		node.Successors = []string{node.Address}
	} else {
		log.Print("StartServer: joining existing ring using ", nprime)
		nprime = resolveAddress(nprime)
		node.Successors = []string{nprime}
		// Migrate keys from the successor (a simple approach).
		conn, err := grpc.Dial(nprime, grpc.WithTransportCredentials(insecure.NewCredentials()))
		if err == nil {
			client := pb.NewChordClient(conn)
			ctx, cancel := context.WithTimeout(context.Background(), time.Second)
			defer cancel()
			resp, err := client.GetAll(ctx, &pb.GetAllRequest{})
			if err == nil {
				for k, v := range resp.KeyValues {
					node.Bucket[k] = v
				}
			}
			conn.Close()
		}
	}

	grpcServer := grpc.NewServer()
	pb.RegisterChordServer(grpcServer, node)

	lis, err := net.Listen("tcp", node.Address)
	if err != nil {
		return nil, fmt.Errorf("failed to listen: %v", err)
	}

	log.Printf("Starting Chord node server on %s", node.Address)
	go func() {
		if err := grpcServer.Serve(lis); err != nil {
			log.Fatalf("failed to serve: %v", err)
		}
	}()

	// Start background maintenance tasks.
	go func() {
		nextFinger := 0
		for {
			time.Sleep(time.Second / 3)
			node.stabilize()
			time.Sleep(time.Second / 3)
			nextFinger = node.fixFingers(nextFinger)
			time.Sleep(time.Second / 3)
			node.checkPredecessor()
		}
	}()

	return node, nil
}

// lookupResponsibleNode iteratively locates the node responsible for a given key.
func lookupResponsibleNode(startAddress, key string) (string, error) {
	id := hash(key)
	current := resolveAddress(startAddress)
	for i := 0; i < maxLookupSteps; i++ {
		conn, err := grpc.Dial(current, grpc.WithTransportCredentials(insecure.NewCredentials()))
		if err != nil {
			return "", fmt.Errorf("lookup: failed to dial %s: %v", current, err)
		}
		client := pb.NewChordClient(conn)
		ctx, cancel := context.WithTimeout(context.Background(), time.Second)
		resp, err := client.FindSuccessor(ctx, &pb.FindSuccessorRequest{Id: id.String()})
		cancel()
		conn.Close()
		if err != nil {
			return "", fmt.Errorf("lookup: error calling FindSuccessor on %s: %v", current, err)
		}
		// If the returned address equals the current node, we assume it is responsible.
		if resp.Address == current {
			return current, nil
		}
		current = resp.Address
	}
	return "", fmt.Errorf("lookup: exceeded maximum steps")
}

// PingNode sends a ping RPC to the given address.
func PingNode(ctx context.Context, address string) error {
	address = resolveAddress(address)
	conn, err := grpc.Dial(address, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		return err
	}
	defer conn.Close()
	client := pb.NewChordClient(conn)
	_, err = client.Ping(ctx, &pb.PingRequest{})
	return err
}

// PutKeyValue uses iterative lookup to find the responsible node and then puts the key-value pair.
func PutKeyValue(ctx context.Context, key, value, address string) error {
	responsible, err := lookupResponsibleNode(address, key)
	if err != nil {
		return err
	}
	conn, err := grpc.Dial(responsible, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		return err
	}
	defer conn.Close()
	client := pb.NewChordClient(conn)
	_, err = client.Put(ctx, &pb.PutRequest{Key: key, Value: value})
	return err
}

// GetValue locates the responsible node and retrieves the value.
func GetValue(ctx context.Context, key, address string) (string, error) {
	responsible, err := lookupResponsibleNode(address, key)
	if err != nil {
		return "", err
	}
	conn, err := grpc.Dial(responsible, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		return "", err
	}
	defer conn.Close()
	client := pb.NewChordClient(conn)
	resp, err := client.Get(ctx, &pb.GetRequest{Key: key})
	if err != nil {
		return "", err
	}
	return resp.Value, nil
}

// DeleteKey finds the responsible node and deletes the key.
func DeleteKey(ctx context.Context, key, address string) error {
	responsible, err := lookupResponsibleNode(address, key)
	if err != nil {
		return err
	}
	conn, err := grpc.Dial(responsible, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		return err
	}
	defer conn.Close()
	client := pb.NewChordClient(conn)
	_, err = client.Delete(ctx, &pb.DeleteRequest{Key: key})
	return err
}

// GetAllKeyValues retrieves all key-value pairs from a node.
func GetAllKeyValues(ctx context.Context, address string) (map[string]string, error) {
	address = resolveAddress(address)
	conn, err := grpc.Dial(address, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		return nil, err
	}
	defer conn.Close()
	client := pb.NewChordClient(conn)
	resp, err := client.GetAll(ctx, &pb.GetAllRequest{})
	if err != nil {
		return nil, err
	}
	return resp.KeyValues, nil
}

// ShutdownNode migrates all local keys to the immediate successor before quitting.
func ShutdownNode(node *Node) {
	node.mu.Lock()
	defer node.mu.Unlock()
	if len(node.Successors) > 0 && node.Successors[0] != node.Address {
		successor := node.Successors[0]
		conn, err := grpc.Dial(successor, grpc.WithTransportCredentials(insecure.NewCredentials()))
		if err != nil {
			log.Printf("Shutdown: failed to dial successor %s: %v", successor, err)
			return
		}
		client := pb.NewChordClient(conn)
		for k, v := range node.Bucket {
			ctx, cancel := context.WithTimeout(context.Background(), time.Second)
			_, err := client.Put(ctx, &pb.PutRequest{Key: k, Value: v})
			cancel()
			if err != nil {
				log.Printf("Shutdown: failed to migrate key %s: %v", k, err)
			}
		}
		conn.Close()
	}
}

// generateRandomKeyValue creates random key-value pairs for testing.
func generateRandomKeyValue() (string, string) {
	// Generate 4 random bytes for both key and value.
	keyBytes := make([]byte, 4)
	valueBytes := make([]byte, 4)
	rand.Read(keyBytes)
	rand.Read(valueBytes)
	return hex.EncodeToString(keyBytes), hex.EncodeToString(valueBytes)
}

// RunShell provides an interactive command shell.
func RunShell(node *Node) {
	reader := bufio.NewReader(os.Stdin)
	for {
		fmt.Print("> ")
		input, err := reader.ReadString('\n')
		if err != nil {
			if err == io.EOF {
				fmt.Println("\nExiting...")
				return
			}
			fmt.Println("Error reading input:", err)
			continue
		}
		parts := strings.Fields(input)
		if len(parts) == 0 {
			continue
		}
		ctx, cancel := context.WithTimeout(context.Background(), time.Second)
		defer cancel()
		switch parts[0] {
		case "help":
			fmt.Println("Available commands:")
			fmt.Println("  help                     - Show this help message")
			fmt.Println("  ping <address>           - Ping another node")
			fmt.Println("  put <key> <value> <address>    - Store a key-value pair in the ring")
			fmt.Println("  putrandom <n> <address>  - Insert n random key-value pairs")
			fmt.Println("  get <key> <address>      - Get a value for a key from the ring")
			fmt.Println("  delete <key> <address>   - Delete a key from the ring")
			fmt.Println("  getall <address>         - Get all key-value pairs from a node")
			fmt.Println("  dump                     - Display info about the current node")
			fmt.Println("  quit                     - Exit the program (migrates data if necessary)")

		case "ping":
			if len(parts) < 2 {
				fmt.Println("Usage: ping <address>")
				continue
			}
			err := PingNode(ctx, parts[1])
			if err != nil {
				fmt.Printf("Ping failed: %v\n", err)
			} else {
				fmt.Println("Ping successful")
			}

		case "put":
			if len(parts) < 4 {
				fmt.Println("Usage: put <key> <value> <address>")
				continue
			}
			err := PutKeyValue(ctx, parts[1], parts[2], parts[3])
			if err != nil {
				fmt.Printf("Put failed: %v\n", err)
			} else {
				fmt.Printf("Put successful: %s -> %s\n", parts[1], parts[2])
			}

		case "putrandom":
			if len(parts) < 3 {
				fmt.Println("Usage: putrandom <n> <address>")
				continue
			}
			n, err := strconv.Atoi(parts[1])
			if err != nil {
				fmt.Println("Invalid number for putrandom")
				continue
			}
			for i := 0; i < n; i++ {
				key, value := generateRandomKeyValue()
				err := PutKeyValue(ctx, key, value, parts[2])
				if err != nil {
					fmt.Printf("putrandom: failed to insert %s: %v\n", key, err)
				} else {
					fmt.Printf("putrandom: inserted %s -> %s\n", key, value)
				}
			}

		case "get":
			if len(parts) < 3 {
				fmt.Println("Usage: get <key> <address>")
				continue
			}
			value, err := GetValue(ctx, parts[1], parts[2])
			if err != nil {
				fmt.Printf("Get failed: %v\n", err)
			} else if value == "" {
				fmt.Printf("Key '%s' not found\n", parts[1])
			} else {
				fmt.Printf("%s -> %s\n", parts[1], value)
			}

		case "delete":
			if len(parts) < 3 {
				fmt.Println("Usage: delete <key> <address>")
				continue
			}
			err := DeleteKey(ctx, parts[1], parts[2])
			if err != nil {
				fmt.Printf("Delete failed: %v\n", err)
			} else {
				fmt.Printf("Delete request for key '%s' completed\n", parts[1])
			}

		case "getall":
			if len(parts) < 2 {
				fmt.Println("Usage: getall <address>")
				continue
			}
			keyValues, err := GetAllKeyValues(ctx, parts[1])
			if err != nil {
				fmt.Printf("GetAll failed: %v\n", err)
			} else {
				if len(keyValues) == 0 {
					fmt.Println("No key-value pairs found")
				} else {
					fmt.Println("Key-value pairs:")
					for k, v := range keyValues {
						fmt.Printf("  %s -> %s\n", k, v)
					}
				}
			}

		case "dump":
			node.dump()

		case "quit":
			fmt.Println("Shutting down node and migrating data...")
			ShutdownNode(node)
			fmt.Println("Exiting...")
			return

		default:
			fmt.Println("Unknown command. Type 'help' for available commands.")
		}
	}
}

func main() {
	createCmd := flag.NewFlagSet("create", flag.ExitOnError)
	createPort := createCmd.Int("port", 3410, "Port to listen on")

	joinCmd := flag.NewFlagSet("join", flag.ExitOnError)
	joinPort := joinCmd.Int("port", 3410, "Port to listen on")
	joinAddr := joinCmd.String("addr", "", "Address of existing node")

	if len(os.Args) < 2 {
		fmt.Println("Expected 'create' or 'join' subcommand")
		os.Exit(1)
	}

	var node *Node
	var address string

	switch os.Args[1] {
	case "create":
		err := createCmd.Parse(os.Args[2:])
		if err != nil {
			log.Fatal(err)
		}
		address = fmt.Sprintf(":%d", *createPort)
		node, err = StartServer(address, "")
		if err != nil {
			log.Fatalf("Failed to create node: %v", err)
		}
		log.Printf("Created new ring with node at %s", node.Address)

	case "join":
		err := joinCmd.Parse(os.Args[2:])
		if err != nil {
			log.Fatal(err)
		}
		if *joinAddr == "" {
			log.Fatal("Join requires an address of an existing node")
		}
		address = fmt.Sprintf(":%d", *joinPort)
		node, err = StartServer(address, *joinAddr)
		if err != nil {
			log.Fatalf("Failed to join ring: %v", err)
		}
		log.Printf("Joined ring with node at %s", node.Address)

	default:
		fmt.Println("Expected 'create' or 'join' subcommand")
		os.Exit(1)
	}

	RunShell(node)
}
