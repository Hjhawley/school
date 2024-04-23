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

    def verify_checksum(self):
        """Verify the checksum of the packet."""
        calculated_checksum = sum(ord(c) for c in self.payload) + self.seqnum
        return self.checksum == calculated_checksum

    def is_ack(self):
        return self.payload == "ACK"
    
    def __str__(self):
        return f"Packet(seqnum={self.seqnum}, checksum={self.checksum}, payload='{self.payload}')"

class RDT:

    def __init__(self, sim):
        self.sim = sim
        self.last_packet = None  # Store the last packet for potential retransmission
        self.seqnum = 0  # Sequence number for host A

    def rdt_sendA(self, msg):
        """Send a message from A to B if there is no message currently in transit."""
        if not self.last_packet:
            packet = Pkt()
            packet.payload = msg
            packet.seqnum = self.seqnum
            packet.make_checksum()
            logging.info(f"Sending: {packet}")
            self.sim.tolayer3(A, packet)
            self.sim.start_timer(A, 100)  # Adjust timer as needed
            self.last_packet = packet

    def rdt_rcvA(self, pkt):
        """Handle incoming ACK packets at A, verify the checksum, and update state."""
        if pkt.is_ack() and pkt.verify_checksum() and pkt.seqnum == self.seqnum:
            logging.info(f"ACK received at A: {pkt}")
            self.sim.stop_timer(A)
            self.last_packet = None
            self.seqnum = (self.seqnum + 1) % 2  # Cycle sequence numbers

    def timer_interruptA(self):
        """Handle timer interrupts at A by retransmitting the last packet if necessary."""
        if self.last_packet:
            logging.warning("Timer interrupt at A, retransmitting packet")
            self.sim.tolayer3(A, self.last_packet)
            self.sim.start_timer(A, 100)  # Restart the timer

    def send_ack(self, seqnum):
        """Send an acknowledgment packet back to A from B."""
        ack_packet = Pkt()
        ack_packet.payload = "ACK"  # Designate the packet as an ACK
        ack_packet.seqnum = seqnum
        ack_packet.make_checksum()
        self.sim.tolayer3(B, ack_packet)

    def rdt_rcvB(self, pkt):
        """Handle received packets at B, verify checksum, send ACK, and pass valid packets to the application layer."""
        if pkt.verify_checksum():
            logging.info(f"Received at B: {pkt}")
            # Send an ACK packet back to A
            self.send_ack(pkt.seqnum)
            self.sim.tolayer5(B, pkt.payload)