# Reliable Data Transport (RDT) Protocol

The procedures you will write are for the sending entity (A) and the receiving
entity (B). Only unidirectional transfer of data (from A to B) is required. Of
course, the B side will have to send packets to A to acknowledge (positively or
negatively) receipt of data. Your routines are to be implemented in the form of
the procedures described below. These procedures will be called by (and will
call) procedures that I have written which simulate a network environment. The
overall structure of the simulated environment is shown below.

<object data="diagram.pdf" type="application/pdf" width="700px" height="700px">
    <embed src="diagram.pdf">
        This browser does not support PDFs. Please download the PDF to view it: <a href="diagram.pdf">Download PDF</a>.</p>
    </embed>
</object>

The unit of data passed between the upper layers and your protocols is a
*message*, which is simply a 20-byte string. Your sending entity will thus
receive data in 20-byte chunks from layer5; your receiving entity should deliver
20-byte chunks of correctly received data to layer5 at the receiving side. You
will not have to worry about the encoding of this string, just use it as you
would normally use a string.

The unit of data passed between your routines and the network layer is a
*packet*, which is declared as:

```
class Pkt:
    seqnum (int)
    checksum (int)
    payload (str)
```

Your routines will fill in the payload field from the message data passed down
from layer5. The other packet fields will be used by your protocols to ensure
reliable delivery, as we've seen in class.

The routines you will write are detailed below. As noted above, such procedures
in real-life would be part of the operating system, and would be called by other
procedures in the operating system.

- **`rdt_sendA(msg)`**, where `msg` is a 20-byte string, containing data to be
  sent to host B. This routine will be called whenever the upper layer at
  the sending side (host A) has a message to send. It is the job of your
  protocol to ensure that the data in such a message is delivered in order, and
  correctly, to the receiving side upper layer. Also, since this protocol is a
  stop-and-wait protocol, you should only send a message if there is currently
  no other message in transit. Just ignore the incoming message if that is the
  case (this is why we use a large frequency
- **`rdt_rcvA(pkt)`**, where `pkt` is an object of type `Pkt`. This routine will
  be called whenever a packet sent from host B (i.e., as a result of a
  `tolayer3()` being done by a B-side procedure) arrives at host A. `pkt` is the
  (possibly corrupted) packet sent from the B-side.
- **`timer_interruptA()`**. This routine will be called when host A's timer
  expires (thus generating a timer interrupt). You'll probably want to use this
  routine to control the retransmission of packets. See `start_timer()` and
  `stop_timer()` below for how the timer is started and stopped.
- **`rdt_rcvB(packet)`**, where `packet` is a structure of type `pkt. `This
  routine will be called whenever a packet sent from the A-side (i.e., as a
  result of a `tolayer3()` being done by a A-side procedure) arrives at the
  B-side. `packet` is the (possibly corrupted) packet sent from the A-side.

## The Simulator

### Interface

The procedures described above are the ones that you will write. I have
written the following routines which can be called by your routines:

- **`start_timer(calling_entity, increment)`**, where `calling_entity` is either
  `0`/`A` (for starting the A-side timer) or `1`/`B` (for starting the B side
  timer), and `increment` is a *float* value indicating the amount of time that
  will pass before the timer interrupts. A's timer should only be started (or
  stopped) by A-side routines, and similarly for the B-side timer. To give you
  an idea of the appropriate increment value to use, a packet sent into the
  network takes an average of 5 time units to arrive at the other side when
  there are no other messages in the medium. Note: you shouldn't need the timer
  for B since we will only be sending data one way (and we won't worry about
      resending ACKs/NACKs).
- **`stop_timer(calling_entity)`**, where `calling_entity` is either `0`/`A` (for
  stopping the A-side timer) or `1`/`B` (for stopping the B side timer).
- **`tolayer3(calling_entity, packet)`**, where `calling_entity` is either
  `0`/`A` (for the A-side send) or `1`/`B` (for the B side send), and `packet`
  is a structure of type `pkt. `Calling this routine will cause the packet to be
  sent into the network, destined for the other entity.
- **`tolayer5(calling_entity, message)`**, where `calling_entity` is either
  `0`/`A` (for A-side delivery to layer 5) or `1`/`B` (for B-side delivery to
  layer 5), and `message` is a 20-byte string. With unidirectional data
  transfer, you will only be calling this with `calling_entity` equal to `1`/`B`
  (delivery to the B-side). Calling this routine will cause data to be passed up
  to layer 5.

### Environment

A call to procedure `tolayer3()` sends packets into the medium (i.e., into the
network layer). Your procedures `A_input()` and `B_input()` are called when a
packet is to be delivered from the medium to your protocol layer.

The medium is capable of corrupting and losing packets. It will not reorder
packets. When you run the program, you will be asked to specify values regarding
the simulated network environment:

- **nmsgs**: The number of messages to simulate. My simulator (and your
  routines) will stop as soon as this number of messages have been passed down
  from layer 5, regardless of whether or not all of the messages have been
  correctly delivered. Thus, you need **not** worry about undelivered or
  unACK'ed messages still in your sender when the simulator stops. Note that if
  you set this value to 1, your program will terminate immediately, before the
  message is delivered to the other side. Thus, this value should always be
  greater than 1. I recommend using a value of N+1. So for example, 11 to send
  (and hopefully receive) 10 packets.
- **freq:** The average time between messages from sender's layer5. You can set
  this value to any non-zero, positive value. Note that the smaller the value
  you choose, the faster events will occur in the simulator. I would recommend a
  really high number at first, even as high as 1000.
- **lossprob:** The probability of packet loss. A value of 0.1 would mean that
  one in ten packets (on average) are lost.
- **corruptprob:** The probability of bit errors. A value of 0.2 would mean that
  one in five packets (on average) are corrupted. Note that the contents of
  payload, sequence, or checksum fields can be corrupted. Your checksum should
  thus include the data and sequence fields.
- **verbose:** The level of chattiness. I have set up the program to use
  Python's `logging` package. Various log messages are already set up for either
  the `debug` or `warning` levels. You might find it useful to add your own log
  messages for the `info` log level. You might want to reference
  [the documentation](https://docs.python.org/3.7/library/logging.html#logging-levels)
  to review the log levels. You should also keep in mind that *real*
  protocols do not have underlying networks that provide such nice information
  about what is going to happen to their packets!

## Helpful Hints

- **Checksumming.** You can use whatever approach for checksumming you want
  (implement it as a method on the `Pkt` class). Remember that the sequence
  number and ack field can also be corrupted. I suggest a TCP-like checksum,
  which consists of the sum of the (integer) sequence field value added to a
  character-by-character sum of the payload field of the packet. I recommend
  using the Python builtin function
  [`ord()`](https://docs.python.org/3/library/functions.html#ord) for this.
- Note that any shared "state" among your routines needs to be in the form of a
  data attribute on your class. Note also that any information that your
  procedures need to save from one invocation to the next must also be
  similarly maintained. For example, your routines will need to keep a copy of a
  packet for possible retransmission. It would probably be a good idea for such
  a data structure to also be saved as an attribute of your class. Note,
  however, that if one of your data attributes is used by your sender side, that
  variable should **NOT** be accessed by the receiving side entity, since in
  real life, communicating entities connected only by a communication channel
  can not share state by some other means. In my solution I prefixed my
  attribute variable names with `A_` or `B_`, respectively, to help
  differentiate.
- There is an attribute on the simulator object called `t` that you can access from
  within your code to help you out with your diagnostics msgs.
- **START SIMPLE.** First design and implement your procedures for the case
  of no loss and no corruption (set the probabilities of loss and corruption
  to zero), and get them working first. Then handle the case of one of these
  probabilities being non-zero, and then finally both being non-zero.
- **Debugging.** Use the logs excessively. The beauty of the logging module
  is that you can turn it off with a single configuration change (at the top
  of the program). Also, slowing down the execution with the `pause`
  variable is really helpful.
