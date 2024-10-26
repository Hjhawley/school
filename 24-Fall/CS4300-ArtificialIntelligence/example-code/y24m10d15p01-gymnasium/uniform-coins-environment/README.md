Uniform Coins
-------------

This is a simple environment to demonstrate creation of a
[gymnasium](https://gymnasium.farama.org/) environment that
has a model to support classic search as well as being used
for reinforcement learning (the primary purpose of most 
gymnasium environments).

Farama has a [turtorial](https://gymnasium.farama.org/tutorials/gymnasium_basics/environment_creation/)
on creating your own custom environment. Those instructions
were used, along with the requirements of having an 
environment model that can be plugged into classical
tree search.

The gymnasium environment is contained completely in [uniform-coins](uniform-coins/). 
Use the `Makefile` in that directory to install the module in your local
pip. Note that this does not copy the module, it sets a link to this
location. This is convenient for making updates after installing it.

[uniform-coins-demo-agents](uniform-coins-demo-agents/) has a random agent 
and a iterative deepening search agent, to demonstrate the use of the 
environment and the model side-by-side in running the environment and 
searching for solutions.



