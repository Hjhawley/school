import argparse
import logging
import sys

import rdt
import simulator

parser = argparse.ArgumentParser(description='Stop-and-wait protocol simulator')
parser.add_argument('-n', '--nmsgs', default=20, type=int, help="number of messages to simulate")
parser.add_argument('-f', '--freq', default=1000, type=float, help="average time between messages from sender's layer5 [>0.0]")
parser.add_argument('-l', '--lossprob', default=0.0, type=float, help="packet loss probability [0.0,1.0), 0 means no loss")
parser.add_argument('-c', '--corruptprob', default=0.0, type=float, help="packet corruption probability [0.0,1.0), 0 means no corruption")
parser.add_argument('-p', '--pause', default=1, type=float, help="the time in seconds to wait between events, controls simulator speed")
parser.add_argument('-v', '--verbose', action='count', default=0, help="how chatty is the simulator, the log level")

args = parser.parse_args()

level=50-args.verbose*10
if level < 0:
    level = 0
logging.basicConfig(level=level)

if args.lossprob >= 1.0:
    print("Invalid packet loss probability")
    sys.exit(1)

if args.corruptprob >= 1.0:
    print("Invalid packet corruption probability")
    sys.exit(1)

sim = simulator.Simulator(args.nmsgs, args.freq, args.lossprob, args.corruptprob, args.pause)

print("Running simulator with the following parameters:\n")
print(f'\tverbose     = {args.verbose}')
print(sim.get_params())
print('\n','*'*10,'GO','*'*10,'\n')

rdt_ = rdt.RDT(sim)
sim.run(rdt_)
