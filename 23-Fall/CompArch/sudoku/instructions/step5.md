Naked sets
==========

The next five steps are devoted to implementing a puzzle solving
technique called *naked sets*. Consider this 3×3 box:

    +-----------------------+
    | 1 . . | . 2 . | 1 2 . |
    | . . . | . . . | . . . |
    | . . 9 | . 8 9 | 7 8 . |
    | - - - + - - - + - - - |
    |       | . 2 . | 1 2 . |
    |   4   | . . . | . . . |
    |       | . . 9 | . . . |
    | - - - + - - - + - - - |
    |       | . 2 . |       |
    |   3   | . 5 . |   6   |
    |       | . . 9 |       |
    +-----------------------+

Three of the squares (numbers 0, 4, and 5 within the box) have
pencil marks for {1,9}, {2,9}, and {1,2}, respectively. Taken as a
group, these three squares must “use up” the three values {1,2,9}.
There is not enough information to know which of the three squares
is 1, which is 2, and which is 9, but we can infer that no other
squares in the box could possibly be one of those three values.
Crossing them off the remaining squares we are left with:

    +-----------------------+
    | 1 . . | . . . | . . . |
    | . . . | . . . | . . . |
    | . . 9 | . 8 . | 7 8 . |
    | - - - + - - - + - - - |
    |       | . 2 . | 1 2 . |
    |   4   | . . . | . . . |
    |       | . . 9 | . . . |
    | - - - + - - - + - - - |
    |       | . . . |       |
    |   3   | . 5 . |   6   |
    |       | . . . |       |
    +-----------------------+

which effectively solved two more squares:

    +-----------------------+
    | 1 . . |       | . . . |
    | . . . |   8   | . . . |
    | . . 9 |       | 7 8 . |
    | - - - + - - - + - - - |
    |       | . 2 . | 1 2 . |
    |   4   | . . . | . . . |
    |       | . . 9 | . . . |
    | - - - + - - - + - - - |
    |       |       |       |
    |   3   |   5   |   6   |
    |       |       |       |
    +-----------------------+

This process generalizes as follows: within a single group, if there
are *n* squares whose combined pencil marks include exactly *n*
candidate values, then those *n* values can be crossed off from any
other square in the group. So two squares that share the same two
pencil mark values, four squares that share the same four pencil
mark values, etc.

There are some interesting special cases. Consider the example above
where a square was solved with the value 8. Note that the square
next to it has {7,8} as its pencil marks, but has the solved square
with 8 next to it. If we apply another round of naked sets
detection, we will find a naked set of size one with the square
containing the 8, leading us to cross 8 off all other pencil mark
lists, which in turn solves another square:

    +-----------------------+
    | 1 . . |       |       |
    | . . . |   8   |   7   |
    | . . 9 |       |       |
    | - - - + - - - + - - - |
    |       | . 2 . | 1 2 . |
    |   4   | . . . | . . . |
    |       | . . 9 | . . . |
    | - - - + - - - + - - - |
    |       |       |       |
    |   3   |   5   |   6   |
    |       |       |       |
    +-----------------------+

At this point there are no further naked sets to exploit in this
group, though this may have created new naked sets in the rows and
columns that intersect this box.

Here is another example using a row:

    +-------+-------+-------+-------+-------+-------+-------+-------+-------+
    | . . . | . . . |       | . . 3 |       |       | . . . | . . 3 |       |
    | 4 . . | . 5 . |   2   | . 5 . |   6   |   1   | 4 . . | 4 5 . |   7   |
    | . . 9 | . . 9 |       | . 8 9 |       |       | . . 9 | . . 9 |       |
    +-------+-------+-------+-------+-------+-------+-------+-------+-------+

In this row there are two squares (0 and 6) that between them can
only be marked with 4 and 9. This implies that one of those squares
must be a 4 and the other 9 (though we do not know which), but those
two values will be “used up” in those two squares, so 4 and 9 can be
crossed off in all the other squares, yielding:

    +-------+-------+-------+-------+-------+-------+-------+-------+-------+
    | . . . |       |       | . . 3 |       |       | . . . | . . 3 |       |
    | 4 . . |   5   |   2   | . 5 . |   6   |   1   | 4 . . | . 5 . |   7   |
    | . . 9 |       |       | . 8 . |       |       | . . 9 | . . . |       |
    +-------+-------+-------+-------+-------+-------+-------+-------+-------+

This in turn exposes a naked set of size 1 in cell 1 (the number 5).
Once we identify the naked set of size one with the 5, we eliminate
5s from all other squares giving:

    +-------+-------+-------+-------+-------+-------+-------+-------+-------+
    | . . . |       |       | . . 3 |       |       | . . . |       |       |
    | 4 . . |   5   |   2   | . . . |   6   |   1   | 4 . . |   3   |   7   |
    | . . 9 |       |       | . 8 . |       |       | . . 9 |       |       |
    +-------+-------+-------+-------+-------+-------+-------+-------+-------+

This in turn exposes a new naked set of size one in square 7 (the
number 3). Crossing off 3s in other cells yields:

    +-------+-------+-------+-------+-------+-------+-------+-------+-------+
    | . . . |       |       |       |       |       | . . . |       |       |
    | 4 . . |   5   |   2   |   8   |   6   |   1   | 4 . . |   3   |   7   |
    | . . 9 |       |       |       |       |       | . . 9 |       |       |
    +-------+-------+-------+-------+-------+-------+-------+-------+-------+

At this point there are no more naked sets that can be exploited.
This example only showed naked sets of small sizes, but any size is
possible. The requirement is just that there be *n* cells with a
combined total of *n* possible values.


Gather the union of some cells
------------------------------

Consider the following row of Sudoku cells:

    index 0     1       2       3       4       5       6       7       8
    +-------+-------+-------+-------+-------+-------+-------+-------+-------+
    |       | . . . | . 2 . |       | 1 . . | . . . | . . . | 1 . . | 1 . . |
    |   3   | . . 6 | . . 6 |   4   | . . 6 | . . 6 | . 5 6 | . . 6 | . . . |
    |       | 7 . . | . . . |       | . . . | . . 9 | 7 8 9 | . . 9 | . 8 . |
    +-------+-------+-------+-------+-------+-------+-------+-------+-------+
    value 8    192      68      16      66     576     992     578     258

Your task in this step is to union together the pencil marks in a
specific set of cells. The function has the following signature:

    gather_set(board, group, key) ->
        set of pencil marks for cells identified by key

and should be implemented in `naked_sets.s`.

Each cell contains a set of bits indicating the values that could
possibly be used to solve that cell. `gather_set` will gather the
set of bits indicating the values that could possibly be used to
solve a group of cells.

`board` is the address of the board (an array of 81 elements, each
16 bits in size), and `group` is an array of 9 lookup table elements
for the nine elements of the group (as in previous steps).

The bits of `key` indicate which cells you should consider. For
example, if `key` is the value 176, which is binary 010110000, then
your task is to gather the union of all pencil marks at index
locations 4, 5, and 7 (because bit numbers 4, 5, and 7 are set in
the key). Those values are 66, 576, and 578, respectively,
representing the pencil marks displayed in the diagram above.
Unioning these pencil marks together (using the OR operation on the
cell values) yields 578.

To review those steps, here is the key of 176, with its bits
numbered:

    876543210
    010110000

There are 1s in columns 4, 5, and 7, so the task is to gather the
union of the pencil marks for cells 4, 5, and 7. Here is the diagram
again with all cells blanked out except for 4, 5, and 7:

    index                               4       5               7
    +-------+-------+-------+-------+-------+-------+-------+-------+-------+
    |       |       |       |       | 1 . . | . . . |       | 1 . . |       |
    |       |       |       |       | . . 6 | . . 6 |       | . . 6 |       |
    |       |       |       |       | . . . | . . 9 |       | . . 9 |       |
    +-------+-------+-------+-------+-------+-------+-------+-------+-------+
    value                               66     576             578

Note that 66 is binary 1000010, 576 is binary 1001000000, and 578 is
binary 1001000010.

Unioning these three cells together is an OR operation on those
three values:

    0001000010
    1001000000
    1001000010
    ----------
    1001000010

giving 1001000010 which is 578 in decimal.

Be sure you understand the task at hand before continuing. If you
are uncertain, contact your instructor.

To restate the problem, the task is to gather the union of some
cells of a Sudoku row and return it. A key value has a bit set for
each cell that should be gathered, and a bit clear for each cell
that should be ignored.

Here is pseudocode to accomplish this:

    gather_set(board, group, key)
        set = 0
        for index = 0; index < 9; index++
            if key & (1<<index) != 0
                board_index = group[index]
                elt = board[board_index]
                set = set | elt
        return set
