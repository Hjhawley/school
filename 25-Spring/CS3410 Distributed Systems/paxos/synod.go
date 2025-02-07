package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
)

// State capures all program state over the entire simulation.
// Nodes capture per-node state, while Messages captures messages
// that have been transmitted by any node (it is basically the network).
type State struct {
	Nodes    []Node
	Messages map[Key]string
}

// Node holds all state that a single node needs to remember across the
// simulation. If each node was actually running on its own machine, this
// would be all of its state.
type Node struct {
	PromiseSequence int
	AcceptSequence  int
	AcceptValue     int

	// other per-node data should be added here
}

// The different message types that are transmitted across the network.
const (
	MsgPrepareRequest = iota
	MsgPrepareResponse
	MsgAcceptRequest
	MsgAcceptResponse
	MsgDecideRequest
)

// Key uniquely identifies a message on the network. The type of message,
// when it was sent, and its target node are enough to identify a
// specific message.
type Key struct {
	Type   int
	Time   int
	Target int
}

func main() {
	// show the line of source where a log message was generated.
	// use log.Printf, etc., to print debugging messages and this
	// will prefix them with info about where they were generated.
	//
	// log.Fatalf, etc., will print the message and then quit
	// the program.
	log.SetFlags(log.Lshortfile)

	// initialize the simulator state
	state := &State{Messages: make(map[Key]string)}

	// read input messages a line at a time from stdin
	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		line := scanner.Text()

		// trim comments
		if i := strings.Index(line, "//"); i >= 0 {
			line = line[:i]
		}

		// ignore empty/comment-only lines
		if len(strings.TrimSpace(line)) == 0 {
			continue
		}
		line += "\n"

		// try handling each message type. if a handler is
		// successful it returns true and processing stops,
		// but if it does not recognize the message it returns
		// false and this switch tries the next handler.
		//
		// uncomment these as you implement them
		switch {
		case state.TryInitialize(line):
		case state.TrySendPrepare(line):
		//case state.TryDeliverPrepareRequest(line):
		//case state.TryDeliverPrepareResponse(line):
		//case state.TryDeliverAcceptRequest(line):
		//case state.TryDeliverAcceptResponse(line):
		//case state.TryDeliverDecideRequest(line):
		default:
			log.Fatalf("unknown line: %s", line)
		}
	}

	// the scanner could have ended because input ended, or there
	// could have been an error so we always check which it was
	if err := scanner.Err(); err != nil {
		log.Fatalf("scanner failure: %v", err)
	}
}

// TryInitialize handles messages of the form:
//
//     initialize 3 nodes
//
// It initilizes the per-node state and is called exactly once
// before any other message type.
func (s *State) TryInitialize(line string) bool {
	var size int
	n, err := fmt.Sscanf(line, "initialize %d nodes\n", &size)
	if err != nil || n != 1 {
		return false
	}

	// rest of implementation for this input goes here...
}

// TrySendPrepare handles message of the form:
//
//     at 1001 send prepare request from 3
//
// It kicks off a proposer sequence at the given time and
// from the given node.
func (s *State) TrySendPrepare(line string) bool {
	var ts, me int
	n, err := fmt.Sscanf(line, "at %d send prepare request from %d\n", &ts, &me)
	if err != nil || n != 2 {
		return false
	}

	// rest of implementation for this input goes here...
}

// additional message handlers continue here...
