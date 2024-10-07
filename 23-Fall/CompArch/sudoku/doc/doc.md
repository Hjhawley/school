Calculate naked sets for a single group
---------------------------------------

In this step you will compute naked sets for a single group (a row,
column, or box) using the functions you wrote in earlier steps:

    single_pass(board, group) ->
        0: nothing changed
        1: something changed

The challenge in this step is to identify every possible subset of
size *n* from 1 to 8 (a subset of size 0 is empty, and a subset of
size 9 would just be all of the cells in the group and there would
be no cells left to optimize).

There is a nice trick to enumerating all possible subsets of every
size: count using a binary number. Consider 4-bit binary numbers.
There are 14 possible values if we just count from 1 to 14 in
binary:

    0001, 0010, 0011, 0100, 0101, 0110, 0111,
    1000, 1001, 1010, 1011, 1100, 1101, 1110

If you consider the 1s as identifying positions to include and 0s as
identifying positions to ignore, this list contains every possible
set of *n* values for every possible value of *n* from 1 to 3. Every
value with a single bit set is included, every combination of two
bits set is includes, and every combination of three bits is
included, with no duplicates. After all, counting enumerates every
possible bit pattern in the given range.

We can extend this to 9-bit values by counting from 1 to 510
inclusive (511 would have all 9 bits set). This will give us every
possible bit pattern with between 1 and 8 bits set.

The `single_pass` function should iterate over those 510 possible
key values (counting from 1 to 510) and try to identify a naked
set for each one. For each key:

*   Call `count_bits` on the key to see how big the subset is
*   Call `gather_set` to gather the candidates present in the pencil
    marks for those cells
*   Call `count_bits` on the set that you gathered to see the
    combined number of candidate values used by that subset
*   If the size of the subset matches the size of the candidate set,
    you have found a naked set of that size, so call `clear_others`
    to cross those values off any other cells

Track if any changes were made (as reported by calls to
`clear_others`) and return that value when finished.
