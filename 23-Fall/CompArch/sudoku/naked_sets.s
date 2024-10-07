                .global naked_sets, single_pass, gather_set, clear_others
                .text

# gather_set(board, group, key) ->
#   set of pencil marks for cells identified by key
gather_set:
                addi sp, sp, -32
                sd ra, 24(sp)
                sd s0, 16(sp)
                sd s1, 8(sp)
                sd s2, 0(sp)

                mv s0, a0           # Move board base address to s0
                mv s1, a1           # Move group base address to s1
                mv s2, a2           # Move key to s2
                li a3, 0            # Initialize set to 0 (a3 will hold the union of pencil marks)

                li t0, 0            # Initialize index to 0
            1:  li t1, 9
                bge t0, t1, 2f      # If index >= 9, exit loop

                li t5, 1
                sll t2, t5, t0      # t2 = 1 << index (calculate bitmask for the current index)
                and t3, s2, t2      # t3 = key & (1 << index)
                beqz t3, 3f         # If t3 == 0, skip to next index (bit not set in key)

                add t4, s1, t0      # Calculate address of the group element (assuming each group element is a byte)
                lbu t4, 0(t4)       # Load the board index from group array
                slli t4, t4, 1      # Multiply board index by 2 to get actual index (assuming each board element is 2 bytes)
                add t4, s0, t4      # Calculate address of the board element
                lh t6, 0(t4)        # Load the board element (pencil marks)
                or a3, a3, t6       # Include the pencil marks in the union set

            3:  addi t0, t0, 1      # Increment index
                j 1b                # Jump back to start of loop

            2:  mv a0, a3           # Move the result to a0 for return

                ld ra, 24(sp)
                ld s0, 16(sp)
                ld s1, 8(sp)
                ld s2, 0(sp)
                addi sp, sp, 32
                ret

# clear_others(board, group, key, set) ->
#    0: nothing changed
#    1: something changed
clear_others:
                addi sp, sp, -32
                sd ra, 24(sp)
                sd s0, 16(sp)
                sd s1, 8(sp)
                sd s2, 0(sp)

                mv s0, a0           # Move board base address to s0
                mv s1, a1           # Move group base address to s1
                mv s2, a2           # Move key to s2
                mv t0, a3           # Move set to t0
                li a3, 0            # Initialize changed to 0
                not t1, t0          # notset = ~set (flip all the bits)

                li t2, 0            # Initialize index to 0
            1:  li t3, 9
                bge t2, t3, 2f      # If index >= 9, exit loop

                li t5, 1
                sll t6, t5, t2      # t6 = 1 << index (calculate bitmask for the current index)
                and t3, s2, t6      # Check if the bit at index is set in key
                bnez t3, 3f         # If bit is set, skip to next index

                add t4, s1, t2      # Calculate address of the group element
                lbu t4, 0(t4)       # Load the board index from group array
                slli t4, t4, 1      # Multiply board index by 2 to get actual index (an element is 2 bytes)
                add t4, s0, t4      # Calculate address of the board element
                lh t3, 0(t4)        # Load original board element (pencil marks)
                and t5, t3, t1      # Clear bits in set from the element
                bne t5, t3, 4f      # If the element has changed, update board and set changed to 1


            3:  addi t2, t2, 1      # Increment index
                j 1b                # Jump back to start of loop

            4:  sh t5, 0(t4)        # Update the board element with the new value
                li a3, 1            # Set changed to 1
                j 3b                # Jump back to increment index and continue loop

            2:  mv a0, a3           # Move the result to a0 for return

                ld ra, 24(sp)
                ld s0, 16(sp)
                ld s1, 8(sp)
                ld s2, 0(sp)
                addi sp, sp, 32
                ret

# single_pass(board, group) ->
#   0: nothing changed
#   1: something changed
single_pass:
    addi sp, sp, -40    # Allocate stack space for local variables
    sd ra, 32(sp)       # Save the return address
    sd s0, 24(sp)       # Save s0 register (board pointer)
    sd s1, 16(sp)       # Save s1 register (key)
    sd s2, 8(sp)        # Save s2 register (upper limit 510)
    sd s3, 0(sp)        # Save s3 register (temporary storage for subset size)

    li s1, 1            # Initialize key to 1 (start of the range for keys)
    li s2, 510          # Set the upper limit for the key value
    li a4, 0            # Initialize changed to 0 (no changes yet)

1:  bgt s1, s2, 3f      # If key is greater than 510, exit loop

    mv a0, s1           # Set key as the first argument for count_bits
    call count_bits     # Call count_bits to get the size of the subset
    mv s3, a0           # Save subset size to s3

    mv a0, s0           # Restore the board pointer from s0
    mv a1, a2           # Group pointer is already in a2 (second argument)
    mv a2, s1           # Set key as the third argument for gather_set
    call gather_set     # Call gather_set to get the set of pencil marks
    mv s4, a0           # Save the result of gather_set to s4

    mv a0, s4           # Set the gathered set as the argument for count_bits
    call count_bits     # Call count_bits to get the size of the candidate set
    mv s5, a0           # Save candidate set size to s5

    beq s3, s5, 2f      # If subset size equals candidate set size, process naked set

    addi s1, s1, 1      # Increment key and continue loop
    j 1b

2:  mv a0, s0           # Restore the board pointer from s0
    mv a1, a2           # Group pointer is in a2
    mv a2, s1           # Key for clear_others is in s1
    mv a3, s4           # Gathered set for clear_others is in s4
    call clear_others   # Call clear_others to eliminate candidates

    bnez a0, 4f         # If clear_others made a change, set changed flag

    addi s1, s1, 1      # Increment key and continue loop
    j 1b

4:  li a4, 1            # Set changed to 1

    addi s1, s1, 1      # Increment key and continue loop
    j 1b

3:  mv a0, a4           # Move changed status to a0 for return
    ld ra, 32(sp)       # Restore the return address
    ld s0, 24(sp)       # Restore s0 register
    ld s1, 16(sp)       # Restore s1 register
    ld s2, 8(sp)        # Restore s2 register
    ld s3, 0(sp)        # Restore s3 register
    addi sp, sp, 40     # Deallocate stack space
    ret                 # Return

# naked_sets(board, table) ->
#   0: nothing changed
#   1: something changed
naked_sets:
                ret
