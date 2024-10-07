Clear some pencil marks from other cells
----------------------------------------

This step has a similar structure to the previous one. Instead of
gathering a set of pencil marks that are used by a selected group of
cells, this step crosses off a set of pencil marks from a selected
group of cells. You will implement the function:

    clear_others(board, group, key, set) ->
       0: nothing changed
       1: something changed

in the file `naked_sets.s`.

As in the previous step, `board` contains the address of the entire
board and `group` is an array of nine index values representing a
single group on the board. Similar to the previous step, `key`
identifies some of the cells in the list. However, this time the
*zeros* identify the cells of interest, while the *ones* identify
the cells to ignore.

`used` contains a set of pencil marks that should be crossed off in
the identified cells, i.e., the ones whose positions in `key` are
marked by zeros.

Consider this pseudcode and compare it with the previous step:

    clear_others(board, group, key, set)
        changed = 0
        notset = ~set (flip all the bits)
        for index = 0; index < 9; index++
            if key & (1<<index) == 0
                board_index = group[index]
                elt = board[board_index]
                new_elt = elt & notset
                if elt != new_elt
                    board[board_index] = new_elt
                    changed = 1
        return changed

To clear a set of bits we flip the bits in the set and the AND the
result with the board element (similar to a previous step).

Where the previous step collected all pencil marks from a set of
cells, this step crosses off pencils marks from the complementary
set of cells. It must also return 1 to indicate that anything
actually changed, or 0 to indicate that the operation did not change
anything.
