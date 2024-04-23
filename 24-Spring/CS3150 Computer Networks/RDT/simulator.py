import logging
import random
import string
import time

import rdt

# possible events:
TIMER_INTERRUPT = 0
FROM_LAYER5 = 1
FROM_LAYER3 = 2

# helpful consts
A = 0
B = 1
ENTITIES = {A: "A", B: "B"}
EVENTS = {TIMER_INTERRUPT: "TIMER_INTERRUPT", FROM_LAYER5: "FROM_LAYER5", FROM_LAYER3: "FROM_LAYER3"}

class Event:

    def __init__(self):
        self.time = None    # event time
        self.type = None    # event type code
        self.entity = None  # entity where event occurs
        self.pkt = None     # packet (if any) assoc w/ this event

    def __str__(self):
        s = "Event("
        s += "entity=" + ENTITIES[self.entity]
        s += ", time={:.03f}".format(self.time if self.time else -1)
        s += ", type=" + EVENTS[self.type]
        if self.pkt is not None:
            s += ", packet=" + str(self.pkt)
        return s + ")"

class Simulator:

    def __init__(self, n_sim_msgs, msg_freq, loss_prob, corrupt_prob, pause):
        self.n_sim_msgs = n_sim_msgs        # number of msgs to simulate
        self.msg_freq = msg_freq            # avg msg send rate (lambda_) TODO: is it really?
        self.loss_prob = loss_prob          # probability msgs will be lost
        self.corrupt_prob = corrupt_prob    # probability msgs will be corrupted
        self.pause = pause                  # time to wait between events

        self.events = []    # the event log
        self.sent = []      # the msgs sent
        self.received = []  # the msgs received

        self.msg_count = 0        # number of messages from 5 to 4 so far
        self.tolayer3_count = 0   # number sent into layer 3
        self.lost_count = 0       # number lost in media
        self.corrupt_count = 0    # number corrupted by media
        self.t = 0.0              # time

    def get_params(self):
        return (f'\tnmsgs       = {self.n_sim_msgs}\n' +
                f'\tfreq        = {self.msg_freq}\n' +
                f'\tlossprob    = {self.loss_prob}\n' +
                f'\tcorruptprob = {self.corrupt_prob}\n' +
                f'\tpause       = {self.pause}\n')

    def generate_next_arrival(self):
        logging.debug("GENERATE NEXT ARRIVAL: creating new arrival")

        # time x is uniform on [0,2*lambda_], having mean of lambda_
        x = random.uniform(0, 2*self.msg_freq)

        newevent = Event()
        newevent.time = self.t+x
        newevent.type = FROM_LAYER5
        newevent.entity = A
        self.insert_event(newevent)

    def insert_event(self, event):
        """insert event into event list according to its time"""
        logging.debug(f"INSERT EVENT: time is {self.t:.03f}")
        logging.debug(f"INSERT EVENT: future time will be {event.time:.03f}")

        # list is empty or packet belongs at end (time-wise)
        if len(self.events) == 0 or event.time > self.events[-1].time:
            self.events.append(event)
            return

        # find where packet goes
        for i in range(len(self.events)):
            if event.time < self.events[i].time:
                self.events.insert(i, event)
                break

    def get_next_event(self):
        # get next event to simulate, removing from event list
        event = self.events.pop(0)
        logging.debug(f"NEXT EVENT: {event}")
        self.t = event.time # update time to next event time
        return event

    def print_events(self):
        print("-"*15)
        for event in self.events:
            print(event)
        print("-"*15)

    def check_end(self):
        return len(self.events) == 0 or self.n_sim_msgs == self.msg_count

    def stop_timer(self, AorB):
        """AorB: is A or B trying to stop the timer"""
        logging.debug(f"STOP TIMER: {ENTITIES[AorB]} stopping timer at {self.t:.03f}")

        for event in self.events:
            if event.type == TIMER_INTERRUPT and event.entity == AorB:
                # remove this event
                self.events.remove(event)
                return
        logging.warning("unable to cancel your timer. It wasn't running.")

    def start_timer(self, AorB, increment):
        """AorB: A or B is trying to start timer"""
        logging.debug(f"START TIMER: {ENTITIES[AorB]} starting timer at {self.t:.03f}")

        # be nice: check to see if timer is already started, if so, then  warn
        for event in self.events:
            if event.type == TIMER_INTERRUPT and event.entity == AorB:
                logging.warning("attempt to start a timer that is already started")
                return

        # create future event for when timer goes off
        newevent = Event()
        newevent.time = self.t + increment
        newevent.type = TIMER_INTERRUPT
        newevent.entity = AorB

        self.insert_event(newevent)

    def tolayer3(self, AorB, packet):
        """AorB: A or B is sending a packet"""
        self.tolayer3_count += 1

        # simulate losses:
        if random.random() < self.loss_prob:
            self.lost_count += 1
            print("TOLAYER3: packet lost:", packet)
            return

        # make a copy of the packet student just gave me since they may decide
        # to do something with the packet after we return back to them
        mypkt = rdt.Pkt()
        mypkt.seqnum = packet.seqnum
        mypkt.checksum = packet.checksum
        mypkt.payload = packet.payload
        logging.debug(f"TOLAYER3: seq: {mypkt.seqnum} "
               f"check: {mypkt.checksum} {mypkt.payload}")

        # create future event for arrival of packet at the other side
        newevent = Event()
        newevent.type = FROM_LAYER3    # packet will pop out from layer3
        newevent.entity = (AorB+1) % 2 # event occurs at other entity
        newevent.pkt = mypkt           # save my copy of packet
        # finally, compute the arrival time of packet at the other end.
        # medium can not reorder, so make sure packet arrives between 1 and 10
        # time units after the latest arrival time of packets
        # currently in the medium on their way to the destination
        last_time = self.t

        for event in self.events:
            if event.type == FROM_LAYER3 and event.entity == newevent.entity:
                last_time = event.time
        newevent.time = last_time + random.uniform(1, 10)

        # simulate corruption:
        if random.random() < self.corrupt_prob:
            self.corrupt_count += 1
            x = random.random()
            if x < .75:
                mypkt.payload = '0' + mypkt.payload[1:]   # corrupt payload
            elif x < .875:
                mypkt.seqnum = 999999 # corrupt sequence number
            print("TOLAYER3: packet corrupted:", mypkt)

        logging.debug("TOLAYER3: scheduling arrival on other side: " +
                str(newevent) + " " + str(newevent.type)+ " " + EVENTS[newevent.type])
        self.insert_event(newevent)

    def tolayer5(self, AorB, msg):
        if msg[0] == msg[-1]:
            print(f"TOLAYER5: {ENTITIES[AorB]} received data: " + msg)
            self.received.append(msg[-1])
        else:
            print(f"TOLAYER5: FAIL - {ENTITIES[AorB]} received corrupted msg: " + msg)

    def run(self, rdt_):
        self.generate_next_arrival()     # initialize event list

        while not self.check_end():
            time.sleep(self.pause)
            event = self.get_next_event()

            if event.type == FROM_LAYER5:
                self.generate_next_arrival()   # set up future arrival
                # fill in msg to give with string of same letter
                msg2give = string.ascii_lowercase[self.msg_count%26] * 20
                print("MAIN: data sent: " + msg2give)
                self.sent.append(msg2give[-1])

                self.msg_count += 1
                if event.entity == A:
                   rdt_.rdt_sendA(msg2give)
                else:
                   rdt_.B_output(msg2give)

            elif event.type == FROM_LAYER3:
                pkt2give = rdt.Pkt()
                pkt2give.seqnum = event.pkt.seqnum
                pkt2give.checksum = event.pkt.checksum
                for i in range(20):
                    pkt2give.payload = event.pkt.payload

                # deliver packet by calling the appropriate entity
                if event.entity == A:
                    rdt_.rdt_rcvA(pkt2give)
                else:
                    print("MAIN: data received:", pkt2give)
                    rdt_.rdt_rcvB(pkt2give)

            elif event.type == TIMER_INTERRUPT:
                if event.entity == A:
                    rdt_.timer_interruptA()
                else:
                    rdt_.B_timerinterrupt()
            else:
                print("INTERNAL PANIC: unknown event type")

        print(f"\n\nSimulator terminated at time {self.t:.03f} after "
              f"sending {self.msg_count}/{self.n_sim_msgs} msgs from layer 5.")
        print("Sent    :", len(self.sent), self.sent)
        print("Received:", len(self.received), self.received)
