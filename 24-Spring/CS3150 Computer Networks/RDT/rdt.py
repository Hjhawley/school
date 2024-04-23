import logging # you may want to log stuff as you go
from simulator import A, B # use these to identify between hosts A and B

class Pkt:

    def __init__(self):
        # do not change these attrs or the simulator will break
        self.seqnum = None
        self.checksum = None
        self.payload = ""

    def make_checksum(self):
        pass

    def verify_checksum(self):
        pass

    def __str__(self):
        return ""

class RDT:

    def __init__(self, sim):
        self.sim = sim # you'll need this to interact with the simulator
        # TODO: You'll want to add other data attrs

    def rdt_sendA(self, msg):
        """Called from layer 5 at A, it should transport the msg to B."""

    def rdt_rcvA(self, pkt):
        """Called from layer 3 when a packet arrives for layer 4 at A."""

    def timer_interruptA(self):
        """Called when A's timer goes off."""

    def rdt_rcvB(self, pkt):
        """Called from layer 3 when a packet arrives for layer 4 at B."""
