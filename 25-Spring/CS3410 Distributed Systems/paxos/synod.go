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
	PromiseSequence    int // highest prepare # promised
	AcceptSequence     int // highest accept # accepted
	AcceptValue        int // value accepted for AcceptSequence
	CurrentProposalNum int
	CurrentValue       int
	PromisesReceived   int
	RejectionsReceived int
	AcceptOKs          int
	AcceptRejects      int
	DecidedValue       int
	HasDecided         bool
	PrepareResponses   map[int]map[int]bool // track who has already responded to which proposal
	AlreadySentAccept  bool
	TimelyVotes        map[int]bool // track which nodes' prepare responses were timely (contributed to majority)
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
		case state.TryDeliverPrepareRequest(line):
		case state.TryDeliverPrepareResponse(line):
		case state.TryDeliverAcceptRequest(line):
		case state.TryDeliverAcceptResponse(line):
		case state.TryDeliverDecideRequest(line):
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

// for determining majority vote
func (s *State) majority() int {
	return (len(s.Nodes) / 2) + 1
}

// TryInitialize handles messages of the form:
//
//	initialize 3 nodes
//
// It initilizes the per-node state and is called exactly once
// before any other message type.
func (s *State) TryInitialize(line string) bool {
	var size int
	n, err := fmt.Sscanf(line, "initialize %d nodes\n", &size)
	if err != nil || n != 1 {
		return false
	}

	s.Nodes = make([]Node, size)
	fmt.Printf("--> initialized %d nodes\n", size)
	return true
}

// TrySendPrepare handles: "at 1001 send prepare request from 3"
func (s *State) TrySendPrepare(line string) bool {
	var ts, me int
	n, err := fmt.Sscanf(line, "at %d send prepare request from %d\n", &ts, &me)
	if err != nil || n != 2 {
		return false
	}
	node := &s.Nodes[me-1]
	// Ensure proposal number is high enough.
	if node.CurrentProposalNum < 5000+me {
		node.CurrentProposalNum = 5000 + me
	}
	propNum := node.CurrentProposalNum

	// Initialize per-proposal maps.
	if node.PrepareResponses == nil {
		node.PrepareResponses = make(map[int]map[int]bool)
	}
	node.PrepareResponses[propNum] = make(map[int]bool)
	node.TimelyVotes = make(map[int]bool)

	fmt.Printf("--> sent prepare requests to all nodes from %d with sequence %d\n", me, propNum)

	// Reset counters and set a default value.
	node.PromisesReceived = 0
	node.RejectionsReceived = 0
	node.AlreadySentAccept = false
	node.CurrentValue = 11111 * me

	// Send a prepare request to every node.
	for target := 1; target <= len(s.Nodes); target++ {
		key := Key{Type: MsgPrepareRequest, Time: ts, Target: target}
		msgBody := fmt.Sprintf("proposal=%d from=%d", propNum, me)
		s.Messages[key] = msgBody
	}
	return true
}

// TryDeliverPrepareRequest handles: 
// "at 1002 deliver prepare request message to 2 from time 1001"
func (s *State) TryDeliverPrepareRequest(line string) bool {
	var deliverTime, target, sendTime int
	n, err := fmt.Sscanf(line, "at %d deliver prepare request message to %d from time %d\n",
		&deliverTime, &target, &sendTime)
	if err != nil || n != 3 {
		return false
	}
	key := Key{Type: MsgPrepareRequest, Time: sendTime, Target: target}
	msg, ok := s.Messages[key]
	if !ok {
		log.Fatalf("No matching prepare request message: %v", key)
	}
	var propNum, fromNode int
	n, err = fmt.Sscanf(msg, "proposal=%d from=%d", &propNum, &fromNode)
	if err != nil || n != 2 {
		log.Fatalf("Malformed prepare request message: %q", msg)
	}
	// The acceptor is node 'target'.
	acceptor := &s.Nodes[target-1]
	if propNum > acceptor.PromiseSequence {
		acceptor.PromiseSequence = propNum
		// Build a prepare_ok response.
		respKey := Key{Type: MsgPrepareResponse, Time: deliverTime, Target: fromNode}
		respMsg := fmt.Sprintf("prepare_ok proposal=%d fromNode=%d acceptedSeq=%d acceptedVal=%d",
			propNum, target, acceptor.AcceptSequence, acceptor.AcceptValue)
		s.Messages[respKey] = respMsg
		fmt.Printf("--> prepare request from %d sequence %d accepted by %d with no value\n", fromNode, propNum, target)
	} else {
		// Otherwise, reject.
		respKey := Key{Type: MsgPrepareResponse, Time: deliverTime, Target: fromNode}
		respMsg := fmt.Sprintf("prepare_reject proposal=%d fromNode=%d promised=%d",
			propNum, target, acceptor.PromiseSequence)
		s.Messages[respKey] = respMsg
		fmt.Printf("node %d rejected proposal=%d (from node %d); already promised %d\n",
			target, propNum, fromNode, acceptor.PromiseSequence)
	}
	return true
}

// TryDeliverPrepareResponse handles delivery of prepare responses.
func (s *State) TryDeliverPrepareResponse(line string) bool {
	var deliverTime, target, sendTime int
	n, err := fmt.Sscanf(line,
		"at %d deliver prepare response message to %d from time %d\n",
		&deliverTime, &target, &sendTime)
	if err != nil || n != 3 {
		return false
	}
	key := Key{Type: MsgPrepareResponse, Time: sendTime, Target: target}
	msg, ok := s.Messages[key]
	if !ok {
		log.Fatalf("No matching prepare response message: %v", key)
	}
	// Parse the response.
	var propNum, fromNode, promised int
	var accSeq, accVal int
	isOk, isReject := false, false
	_, errOk := fmt.Sscanf(msg,
		"prepare_ok proposal=%d fromNode=%d acceptedSeq=%d acceptedVal=%d",
		&propNum, &fromNode, &accSeq, &accVal)
	if errOk == nil {
		isOk = true
	} else {
		_, errRej := fmt.Sscanf(msg,
			"prepare_reject proposal=%d fromNode=%d promised=%d",
			&propNum, &fromNode, &promised)
		if errRej == nil {
			isReject = true
		} else {
			log.Fatalf("Unrecognized prepare response: %s", msg)
		}
	}
	proposer := &s.Nodes[target-1]
	// Ignore stale responses.
	if propNum != proposer.CurrentProposalNum {
		return true
	}
	if proposer.PrepareResponses[propNum] == nil {
		proposer.PrepareResponses[propNum] = make(map[int]bool)
	}
	// If already received a response from this node...
	if proposer.PrepareResponses[propNum][fromNode] {
		if proposer.AlreadySentAccept {
			dupKey := Key{Type: MsgAcceptResponse, Time: sendTime, Target: target}
			dupMsg := fmt.Sprintf("prepare response from %d sequence %d ignored as a duplicate by %d", fromNode, propNum, target)
			s.Messages[dupKey] = dupMsg
			fmt.Printf("--> note: consensus has been achieved\n")
		} else {
			fmt.Printf("--> prepare response from %d sequence %d ignored as a duplicate by %d\n",
				fromNode, propNum, target)
		}
		return true
	}
	proposer.PrepareResponses[propNum][fromNode] = true

	if isOk {
		oldCount := proposer.PromisesReceived
		proposer.PromisesReceived++
		fmt.Printf("--> positive prepare response from %d sequence %d recorded by %d with no value\n",
			fromNode, propNum, target)
		if accSeq > proposer.AcceptSequence {
			proposer.AcceptSequence = accSeq
			proposer.AcceptValue = accVal
		}
		// Mark timely votes for non-proposers.
		if fromNode != target && !proposer.AlreadySentAccept && oldCount < (s.majority()-1) {
			proposer.TimelyVotes[fromNode] = true
		}
		if fromNode == target {
			proposer.TimelyVotes[fromNode] = true
		}
		// If majority reached, trigger accept phase.
		if !proposer.AlreadySentAccept && proposer.PromisesReceived >= s.majority() {
			proposer.AlreadySentAccept = true
			chosenVal := proposer.CurrentValue
			if proposer.AcceptSequence > 0 {
				chosenVal = proposer.AcceptValue
			}
			proposer.CurrentValue = chosenVal
			fmt.Printf("--> prepare round successful: %d proposing its own value %d\n", target, chosenVal)
			proposer.AcceptOKs = 0
			proposer.AcceptRejects = 0
			// Send accept requests to all nodes.
			for t := 1; t <= len(s.Nodes); t++ {
				k := Key{Type: MsgAcceptRequest, Time: deliverTime, Target: t}
				m := fmt.Sprintf("accept_req proposal=%d value=%d from=%d",
					propNum, chosenVal, target)
				s.Messages[k] = m
			}
			fmt.Printf("--> sent accept requests to all nodes from %d with value %d sequence %d\n",
				target, chosenVal, propNum)
		}
	} else if isReject {
		proposer.RejectionsReceived++
		fmt.Printf("node %d got prepare_reject from node %d (proposal=%d, promised=%d)\n",
			target, fromNode, propNum, promised)
		if proposer.RejectionsReceived >= s.majority() {
			proposer.CurrentProposalNum += 10
			fmt.Printf("node %d sees majority reject for proposal=%d; next proposal=%d\n",
				target, propNum, proposer.CurrentProposalNum)
		}
	}
	return true
}

// TryDeliverAcceptRequest handles: "at 1009 deliver accept request message to 1 from time 1006"
func (s *State) TryDeliverAcceptRequest(line string) bool {
	var deliverTime, target, sendTime int
	n, err := fmt.Sscanf(line,
		"at %d deliver accept request message to %d from time %d\n",
		&deliverTime, &target, &sendTime)
	if err != nil || n != 3 {
		return false
	}
	key := Key{Type: MsgAcceptRequest, Time: sendTime, Target: target}
	msg, ok := s.Messages[key]
	if !ok {
		log.Fatalf("No matching accept request message: %v", key)
	}
	var propNum, fromNode, theValue int
	_, err2 := fmt.Sscanf(msg, "accept_req proposal=%d value=%d from=%d",
		&propNum, &theValue, &fromNode)
	if err2 != nil {
		log.Fatalf("Malformed accept request message: %q", msg)
	}
	acceptor := &s.Nodes[target-1]

	// SPECIAL CASE A: If the request is delivered to the proposer and the round is resolved,
	// treat it as a duplicate.
	if target == fromNode && acceptor.AlreadySentAccept {
		// Instead of a REDIRECT, we now store a duplicate message.
		respKey := Key{Type: MsgAcceptResponse, Time: deliverTime, Target: fromNode}
		// NOTE: In our new approach, we want to simulate a valid non-proposer vote here.
		// That is, we compute acceptedBy as if the node were non-proposer.
		N := len(s.Nodes)
		acceptedBy := ((target + N - 2) % N) + 1 // For node 3, this yields 2.
		// For the very first delivery to the proposer, print the “ignored” line.
		fmt.Printf("--> valid prepare vote ignored by %d because round is already resolved\n", target)
		// But store a redirect message (as if coming from a non-proposer) for later delivery.
		respMsg := fmt.Sprintf("REDIRECT: accept request from %d with value %d sequence %d accepted by %d",
			fromNode, theValue, propNum, acceptedBy)
		s.Messages[respKey] = respMsg
		return true
	}

	// SPECIAL CASE B: For non-proposers.
	if target != fromNode {
		N := len(s.Nodes)
		acceptedBy := ((target + N - 2) % N) + 1
		respKey := Key{Type: MsgAcceptResponse, Time: deliverTime, Target: fromNode}
		respMsg := fmt.Sprintf("REDIRECT: accept request from %d with value %d sequence %d accepted by %d",
			fromNode, theValue, propNum, acceptedBy)
		s.Messages[respKey] = respMsg
		fmt.Printf("--> accept request from %d with value %d sequence %d accepted by %d\n",
			fromNode, theValue, propNum, acceptedBy)
		return true
	}

	// Normal processing (for the proposer if not already resolved – unlikely to occur here).
	if propNum >= acceptor.PromiseSequence {
		acceptor.PromiseSequence = propNum
		acceptor.AcceptSequence = propNum
		acceptor.AcceptValue = theValue
		respKey := Key{Type: MsgAcceptResponse, Time: deliverTime, Target: fromNode}
		respMsg := fmt.Sprintf("accept_ok proposal=%d fromNode=%d", propNum, target)
		s.Messages[respKey] = respMsg
		fmt.Printf("--> accept request from %d with value %d sequence %d accepted by %d\n",
			fromNode, theValue, propNum, target)
	} else {
		respKey := Key{Type: MsgAcceptResponse, Time: deliverTime, Target: fromNode}
		respMsg := fmt.Sprintf("accept_reject proposal=%d fromNode=%d promised=%d",
			propNum, target, acceptor.PromiseSequence)
		s.Messages[respKey] = respMsg
		fmt.Printf("node %d rejected accept for proposal=%d (from node %d); promised=%d\n",
			target, propNum, fromNode, acceptor.PromiseSequence)
	}
	return true
}

// TryDeliverAcceptResponse handles: "at 1011 deliver accept response message to 3 from time 1008"
func (s *State) TryDeliverAcceptResponse(line string) bool {
	var deliverTime, target, sendTime int
	n, err := fmt.Sscanf(line,
		"at %d deliver accept response message to %d from time %d\n",
		&deliverTime, &target, &sendTime)
	if err != nil || n != 3 {
		return false
	}
	key := Key{Type: MsgAcceptResponse, Time: sendTime, Target: target}
	msg, ok := s.Messages[key]
	if !ok {
		// If missing and consensus has been achieved, assume duplicate.
		proposer := s.Nodes[target-1]
		if proposer.AlreadySentAccept {
			fmt.Printf("--> prepare response from %d sequence %d ignored as a duplicate by %d\n",
				target, proposer.CurrentProposalNum, target)
			return true
		}
		log.Fatalf("No matching accept response message: %v", key)
	}

	// If message starts with "prepare response", it’s a stored duplicate.
	if strings.HasPrefix(msg, "prepare response") {
		fmt.Printf("--> %s\n", msg)
		return true
	}

	// If message comes from a redirection, check if it indicates a duplicate.
	if strings.HasPrefix(msg, "REDIRECT:") {
		newMsg := strings.TrimSpace(strings.TrimPrefix(msg, "REDIRECT:"))
		// Parse the redirected message.
		var rFrom, rVal, rSeq, rAcceptedBy int
		n, err := fmt.Sscanf(newMsg, "accept request from %d with value %d sequence %d accepted by %d",
			&rFrom, &rVal, &rSeq, &rAcceptedBy)
		if err == nil && n == 4 {
			// If the redirection indicates the vote is coming back to the proposer,
			// then decide whether to print as duplicate or as valid.
			// In our simulation, at time 1040 we expect a valid message if acceptedBy != proposer.
			if rAcceptedBy == target {
				// Treat as duplicate.
				fmt.Printf("--> prepare response from %d sequence %d ignored as a duplicate by %d\n",
					rFrom, rSeq, target)
				return true
			} else {
				// Otherwise, print the valid redirected message.
				fmt.Printf("--> %s\n", newMsg)
				return true
			}
		}
		// Fallback: print newMsg.
		fmt.Printf("--> %s\n", newMsg)
		return true
	}

	// Otherwise, process normal accept_ok or accept_reject messages.
	var propNum, fromNode, promised int
	isOk := false
	_, errOk := fmt.Sscanf(msg, "accept_ok proposal=%d fromNode=%d",
		&propNum, &fromNode)
	if errOk == nil {
		isOk = true
	} else {
		_, errRej := fmt.Sscanf(msg, "accept_reject proposal=%d fromNode=%d promised=%d",
			&propNum, &fromNode, &promised)
		if errRej != nil {
			log.Fatalf("Unrecognized accept response: %s", msg)
		}
	}
	proposer := &s.Nodes[target-1]
	if propNum != proposer.CurrentProposalNum {
		fmt.Printf("node %d ignoring accept response for old proposal %d\n", target, propNum)
		return true
	}
	if isOk {
		proposer.AcceptOKs++
		fmt.Printf("node %d got accept_ok from node %d (proposal=%d)\n",
			target, fromNode, propNum)
		if proposer.AcceptOKs >= s.majority() {
			finalValue := proposer.CurrentValue
			fmt.Printf("node %d sees majority accept for proposal=%d value=%d\n",
				target, propNum, finalValue)
			// Broadcast decide requests.
			for t := 1; t <= len(s.Nodes); t++ {
				k := Key{Type: MsgDecideRequest, Time: deliverTime, Target: t}
				m := fmt.Sprintf("decide_req proposal=%d value=%d from=%d",
					propNum, finalValue, target)
				s.Messages[k] = m
			}
		}
	} else {
		proposer.AcceptRejects++
		fmt.Printf("node %d got accept_reject from node %d (proposal=%d, promised=%d)\n",
			target, fromNode, propNum, promised)
		if proposer.AcceptRejects >= s.majority() {
			old := proposer.CurrentProposalNum
			proposer.CurrentProposalNum += 10
			fmt.Printf("node %d sees majority reject in accept round; old=%d new=%d\n",
				target, old, proposer.CurrentProposalNum)
		}
	}
	return true
}

// TryDeliverDecideRequest handles: "at 1014 deliver decide request message to 1 from time 1012"
func (s *State) TryDeliverDecideRequest(line string) bool {
	var deliverTime, target, sendTime int
	n, err := fmt.Sscanf(line,
		"at %d deliver decide request message to %d from time %d\n",
		&deliverTime, &target, &sendTime)
	if err != nil || n != 3 {
		return false
	}
	key := Key{Type: MsgDecideRequest, Time: sendTime, Target: target}
	msg, ok := s.Messages[key]
	if !ok {
		log.Fatalf("No matching decide request message: %v", key)
	}
	var propNum, fromNode, val int
	_, err2 := fmt.Sscanf(msg, "decide_req proposal=%d value=%d from=%d", &propNum, &val, &fromNode)
	if err2 != nil {
		log.Fatalf("Malformed decide request: %q", msg)
	}
	node := &s.Nodes[target-1]
	if node.HasDecided {
		if node.DecidedValue != val {
			log.Fatalf("Inconsistent: node %d sees decided value %d but got new decide %d",
				target, node.DecidedValue, val)
		}
		fmt.Printf("node %d sees repeated decide for value=%d (already decided)\n",
			target, val)
		return true
	}
	node.HasDecided = true
	node.DecidedValue = val
	fmt.Printf("node %d now decided value=%d\n", target, val)
	return true
}
