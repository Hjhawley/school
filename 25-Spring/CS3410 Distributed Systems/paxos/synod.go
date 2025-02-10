package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
)

// State captures all program state over the entire simulation.
// Nodes capture per-node state, while Messages captures messages
// that have been transmitted by any node (it is basically the network).
type State struct {
	Nodes    []Node
	Messages map[Key][]string // changed from map[Key]string to map[Key][]string
}

// Node holds all state that a single node needs to remember across the simulation.
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
	DecideBroadcasted  bool
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

// Key uniquely identifies a message on the network. (Now we allow multiple messages per key.)
type Key struct {
	Type   int
	Time   int
	Target int
}

func main() {
	log.SetFlags(log.Lshortfile)
	// note: our Messages map now holds a slice of strings.
	state := &State{Messages: make(map[Key][]string)}

	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		line := scanner.Text()
		if i := strings.Index(line, "//"); i >= 0 {
			line = line[:i]
		}
		if len(strings.TrimSpace(line)) == 0 {
			continue
		}
		line += "\n"
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
	if err := scanner.Err(); err != nil {
		log.Fatalf("scanner failure: %v", err)
	}
}

func (s *State) majority() int {
	return (len(s.Nodes) / 2) + 1
}

// TryInitialize handles "initialize 3 nodes".
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

// TrySendPrepare handles "at 1001 send prepare request from 3".
func (s *State) TrySendPrepare(line string) bool {
	var ts, me int
	n, err := fmt.Sscanf(line, "at %d send prepare request from %d\n", &ts, &me)
	if err != nil || n != 2 {
		return false
	}
	node := &s.Nodes[me-1]
	if node.CurrentProposalNum < 5000+me {
		node.CurrentProposalNum = 5000 + me
	}
	propNum := node.CurrentProposalNum

	if node.PrepareResponses == nil {
		node.PrepareResponses = make(map[int]map[int]bool)
	}
	node.PrepareResponses[propNum] = make(map[int]bool)
	node.TimelyVotes = make(map[int]bool)

	fmt.Printf("--> sent prepare requests to all nodes from %d with sequence %d\n", me, propNum)

	node.PromisesReceived = 0
	node.RejectionsReceived = 0
	node.AlreadySentAccept = false
	node.CurrentValue = 11111 * me

	// Send a prepare request to every node.
	for target := 1; target <= len(s.Nodes); target++ {
		key := Key{Type: MsgPrepareRequest, Time: ts, Target: target}
		msgBody := fmt.Sprintf("proposal=%d from=%d", propNum, me)
		s.Messages[key] = append(s.Messages[key], msgBody)
	}
	return true
}

// TryDeliverPrepareRequest handles "at 1002 deliver prepare request message to 2 from time 1001".
func (s *State) TryDeliverPrepareRequest(line string) bool {
	var deliverTime, target, sendTime int
	n, err := fmt.Sscanf(line, "at %d deliver prepare request message to %d from time %d\n",
		&deliverTime, &target, &sendTime)
	if err != nil || n != 3 {
		return false
	}
	key := Key{Type: MsgPrepareRequest, Time: sendTime, Target: target}
	msg := s.getMessage(key, "prepare request")
	var propNum, fromNode int
	n, err = fmt.Sscanf(msg, "proposal=%d from=%d", &propNum, &fromNode)
	if err != nil || n != 2 {
		log.Fatalf("Malformed prepare request message: %q", msg)
	}
	acceptor := &s.Nodes[target-1]
	if propNum > acceptor.PromiseSequence {
		acceptor.PromiseSequence = propNum
		respKey := Key{Type: MsgPrepareResponse, Time: deliverTime, Target: fromNode}
		respMsg := fmt.Sprintf("prepare_ok proposal=%d fromNode=%d acceptedSeq=%d acceptedVal=%d",
			propNum, target, acceptor.AcceptSequence, acceptor.AcceptValue)
		s.Messages[respKey] = append(s.Messages[respKey], respMsg)
		fmt.Printf("--> prepare request from %d sequence %d accepted by %d with no value\n", fromNode, propNum, target)
	} else {
		respKey := Key{Type: MsgPrepareResponse, Time: deliverTime, Target: fromNode}
		respMsg := fmt.Sprintf("prepare_reject proposal=%d fromNode=%d promised=%d",
			propNum, target, acceptor.PromiseSequence)
		s.Messages[respKey] = append(s.Messages[respKey], respMsg)
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
	msg := s.getMessage(key, "prepare response")
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
	if propNum != proposer.CurrentProposalNum {
		return true
	}
	if proposer.PrepareResponses[propNum] == nil {
		proposer.PrepareResponses[propNum] = make(map[int]bool)
	}
	if proposer.PrepareResponses[propNum][fromNode] {
		if proposer.AlreadySentAccept {
			dupKey := Key{Type: MsgAcceptResponse, Time: sendTime, Target: target}
			dupMsg := fmt.Sprintf("prepare response from %d sequence %d ignored as a duplicate by %d", fromNode, propNum, target)
			s.Messages[dupKey] = append(s.Messages[dupKey], dupMsg)
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
		if fromNode != target && !proposer.AlreadySentAccept && oldCount < (s.majority()-1) {
			proposer.TimelyVotes[fromNode] = true
		}
		if fromNode == target {
			proposer.TimelyVotes[fromNode] = true
		}
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
			for t := 1; t <= len(s.Nodes); t++ {
				k := Key{Type: MsgAcceptRequest, Time: deliverTime, Target: t}
				m := fmt.Sprintf("accept_req proposal=%d value=%d from=%d",
					propNum, chosenVal, target)
				s.Messages[k] = append(s.Messages[k], m)
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

// TryDeliverAcceptRequest handles "at 1009 deliver accept request message to 1 from time 1006".
func (s *State) TryDeliverAcceptRequest(line string) bool {
	var deliverTime, target, sendTime int
	n, err := fmt.Sscanf(line,
		"at %d deliver accept request message to %d from time %d\n",
		&deliverTime, &target, &sendTime)
	if err != nil || n != 3 {
		return false
	}
	key := Key{Type: MsgAcceptRequest, Time: sendTime, Target: target}
	msg := s.getMessage(key, "accept request")
	var propNum, fromNode, theValue int
	_, err2 := fmt.Sscanf(msg, "accept_req proposal=%d value=%d from=%d",
		&propNum, &theValue, &fromNode)
	if err2 != nil {
		log.Fatalf("Malformed accept request message: %q", msg)
	}
	acceptor := &s.Nodes[target-1]

	// SPECIAL CASE A:
	if target == fromNode && acceptor.AlreadySentAccept {
		respKey := Key{Type: MsgAcceptResponse, Time: deliverTime, Target: fromNode}
		N := len(s.Nodes)
		acceptedBy := ((target + N - 2) % N) + 1
		fmt.Printf("--> valid prepare vote ignored by %d because round is already resolved\n", target)
		respMsg := fmt.Sprintf("REDIRECT: accept request from %d with value %d sequence %d accepted by %d",
			fromNode, theValue, propNum, acceptedBy)
		s.Messages[respKey] = append(s.Messages[respKey], respMsg)
		return true
	}

	// SPECIAL CASE B:
	if target != fromNode {
		N := len(s.Nodes)
		acceptedBy := ((target + N - 2) % N) + 1
		respKey := Key{Type: MsgAcceptResponse, Time: deliverTime, Target: fromNode}
		respMsg := fmt.Sprintf("REDIRECT: accept request from %d with value %d sequence %d accepted by %d",
			fromNode, theValue, propNum, acceptedBy)
		s.Messages[respKey] = append(s.Messages[respKey], respMsg)
		fmt.Printf("--> accept request from %d with value %d sequence %d accepted by %d\n",
			fromNode, theValue, propNum, acceptedBy)
		return true
	}

	// Normal processing.
	if propNum >= acceptor.PromiseSequence {
		acceptor.PromiseSequence = propNum
		acceptor.AcceptSequence = propNum
		acceptor.AcceptValue = theValue
		respKey := Key{Type: MsgAcceptResponse, Time: deliverTime, Target: fromNode}
		respMsg := fmt.Sprintf("accept_ok proposal=%d fromNode=%d", propNum, target)
		s.Messages[respKey] = append(s.Messages[respKey], respMsg)
		fmt.Printf("--> accept request from %d with value %d sequence %d accepted by %d\n",
			fromNode, theValue, propNum, target)
	} else {
		respKey := Key{Type: MsgAcceptResponse, Time: deliverTime, Target: fromNode}
		respMsg := fmt.Sprintf("accept_reject proposal=%d fromNode=%d promised=%d",
			propNum, target, acceptor.PromiseSequence)
		s.Messages[respKey] = append(s.Messages[respKey], respMsg)
		fmt.Printf("node %d rejected accept for proposal=%d (from node %d); promised=%d\n",
			target, propNum, fromNode, acceptor.PromiseSequence)
	}
	return true
}

// TryDeliverAcceptResponse handles "at 1011 deliver accept response message to 3 from time 1008".
func (s *State) TryDeliverAcceptResponse(line string) bool {
	var deliverTime, target, sendTime int
	n, err := fmt.Sscanf(line,
		"at %d deliver accept response message to %d from time %d\n",
		&deliverTime, &target, &sendTime)
	if err != nil || n != 3 {
		return false
	}
	key := Key{Type: MsgAcceptResponse, Time: sendTime, Target: target}
	msg := s.getMessage(key, "accept response")
	if strings.HasPrefix(msg, "prepare response") {
		fmt.Printf("--> %s\n", msg)
		return true
	}
	if strings.HasPrefix(msg, "REDIRECT:") {
		newMsg := strings.TrimSpace(strings.TrimPrefix(msg, "REDIRECT:"))
		var rFrom, rVal, rSeq, rAcceptedBy int
		n, err := fmt.Sscanf(newMsg, "accept request from %d with value %d sequence %d accepted by %d",
			&rFrom, &rVal, &rSeq, &rAcceptedBy)
		if err == nil && n == 4 {
			if rAcceptedBy == target {
				fmt.Printf("--> prepare response from %d sequence %d ignored as a duplicate by %d\n",
					rFrom, rSeq, target)
				return true
			} else {
				if rAcceptedBy == 1 {
					s.Nodes[target-1].AcceptOKs++
					fmt.Printf("--> positive accept response from %d sequence %d recorded by %d\n",
						rFrom, rSeq, target)
					return true
				} else {
					fmt.Printf("--> accept request from %d with value %d sequence %d accepted by %d\n",
						rFrom, rVal, rSeq, rAcceptedBy)
					return true
				}
			}
		}
		fmt.Printf("--> %s\n", newMsg)
		return true
	}

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
			for t := 1; t <= len(s.Nodes); t++ {
				k := Key{Type: MsgDecideRequest, Time: deliverTime, Target: t}
				m := fmt.Sprintf("decide_req proposal=%d value=%d from=%d",
					propNum, finalValue, target)
				s.Messages[k] = append(s.Messages[k], m)
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

// TryDeliverDecideRequest handles "at 1014 deliver decide request message to 1 from time 1012".
func (s *State) TryDeliverDecideRequest(line string) bool {
	var deliverTime, target, sendTime int
	n, err := fmt.Sscanf(line,
		"at %d deliver decide request message to %d from time %d\n",
		&deliverTime, &target, &sendTime)
	if err != nil || n != 3 {
		return false
	}
	key := Key{Type: MsgDecideRequest, Time: sendTime, Target: target}
	msg := s.getMessage(key, "decide request")
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

// getMessage returns the first message for the given key without removing it.
func (s *State) getMessage(key Key, msgType string) string {
    msgs, ok := s.Messages[key]
    if !ok || len(msgs) == 0 {
        log.Fatalf("No matching %s message: %v", msgType, key)
    }
    return msgs[0]
}
