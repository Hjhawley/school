import logging # you may want to log stuff as you go
from simulator import A, B # use these to identify between hosts A and B

class Pkt:

    def __init__(self):
        # do not change these attrs or the simulator will break
        self.seqnum = None
        self.checksum = None
        self.payload = ""

    def make_checksum(self):
        self.checksum = sum(ord(c) for c in self.payload) + self.seqnum

    def verify_checksum(self, received_checksum):
        return self.checksum == received_checksum

    def __str__(self):
        return f"Packet(seqnum={self.seqnum}, checksum={self.checksum}, payload='{self.payload}')"

class RDT:

    def __init__(self, sim):
        self.sim = sim
        self.last_packet = None  # Properly initialize to store the packet object
        self.seqnum = 0  # Track the current sequence number for A

    def rdt_sendA(self, msg):
        """Called from layer 5 at A, it should transport the msg to B."""
        if not self.last_packet:  # Check if there's no packet currently in transit
            packet = Pkt()
            packet.payload = msg
            packet.seqnum = self.seqnum
            packet.make_checksum()
            logging.info(f"Sending: {packet}")
            self.sim.tolayer3(A, packet)
            self.sim.start_timer(A, 100)  # Adjust timer as needed
            self.last_packet = packet  # Update to store the current packet as the last packet

    def rdt_rcvA(self, pkt):
        """Called from layer 3 when a packet arrives for layer 4 at A."""
        if pkt.verify_checksum(pkt.checksum):
            logging.info(f"Received at A: {pkt}")
            self.sim.stop_timer(A)
            self.last_packet = None  # Reset since the packet was successfully acknowledged
            self.seqnum = (self.seqnum + 1) % 2  # Update the sequence number

    def timer_interruptA(self):
        """Re-send the last packet if the timer goes off, indicating a timeout."""
        if self.last_packet:
            logging.warning("Timer interrupt at A, retransmitting packet")
            self.sim.tolayer3(A, self.last_packet)  # Retransmit the last packet
            self.sim.start_timer(A, 100)  # Restart the timer

    def rdt_rcvB(self, pkt):
        """Called from layer 3 when a packet arrives for layer 4 at B."""
        if pkt.verify_checksum(pkt.checksum):
            logging.info(f"Received at B: {pkt}")
            self.sim.tolayer5(B, pkt.payload)  # Pass payload to application layer

""" # Setup logging
logging.basicConfig(level=logging.DEBUG)
 """