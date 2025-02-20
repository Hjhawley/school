This problem will let you test and submit your Paxos synod protocol
simulator.

Put your code as a single file in `synod.go`. The test input scripts
are all in the `inputs/` directory. A file with the extension
`.input` is the test input, and corresponding file with extension
`.expected` has the expected output.

To test your code, just type "make", which is short for "make step".
"make step" will compile and run your code, feeding each of the
input files in turn. It monitors your output line-by-line and
compares it with the expected output. As soon as it detects a
mismatch, it stops and shows you what it expected and what it found.

Note that the input lines will also be echoed to the screen, but
your program should not print them out.

To pass these tests, your output must be identical to the expected
output. You may have to revise your printed messages to conform.

This assignment has two steps. In the first step you need to build
the parser and the basic project structure as well as the ability to
process the prepare round. Your simulator will need to accept
messages of the following forms from the input script:

*   initialize 3 nodes
*   at 1001 send prepare request from 3
*   at 1002 deliver preapre request message to 2 from time 1001

You should also generate appropriate responses (see the expected
output for details).
