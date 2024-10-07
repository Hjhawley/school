                .global pencil_marks, get_used, clear_used, count_bits
                .text

# count_bits(n) -> # of bits set in n (only counting bits 0-9 inclusive)
count_bits:
                li a3, 0            # count = 0
                li a1, 0            # i = 0
                li a2, 10
            1:  bge a1, a2, 3f      # while i < 10
                li t0, 1
                sll t0, t0, a1      # create mask by shifting 1 'i' times
                and t1, a0, t0      # AND 'n' with mask and store in temp
                beqz t1, 2f         # skip count if temp = 0
                addi a3, a3, 1      # count += 1 if the bit was set
            2:  addi a1, a1, 1      # increment i
                j 1b
            3:  mv a0, a3
                ret

# get_used(board, group) -> used
get_used:
                # Prelude
                addi sp, sp, -64    # Make space on the stack
                sd ra, 56(sp)       # Return address
                sd s0, 48(sp)       # board saved in s0
                sd s1, 40(sp)       # group saved in s1
                sd s2, 32(sp)       # used saved in s2
                sd s3, 24(sp)       # group_index saved in s3
                sd s4, 16(sp)       # element saved in s4

                # get_used
                mv s0, a0           # board = a0 (argument)
                mv s1, a1           # group = a1 (argument)
                li s2, 0            # used = 0
                li s3, 0            # group_index = 0

            1:  li t6, 9
                bge s3, t6, 4f      # while group_index < 9
                add t0, s1, s3      # group_element_address = group + group_index
                lb t1, 0(t0)        # board_index = lb(group_element_address)
                slli t2, t1, 1      # scaled_board_index = board_index << 1
                add t3, s0, t2      # board_element_address = board + scaled_board_index
                lh t4, 0(t3)        # element = lh(board_element_address)
                mv a0, t4           # copy to a0
                call count_bits     # count the bits in element
                mv t5, a0           # t5 = count
                li t6, 1
                beq t5, t6, 2f      # check if t5 == 1
                j 3f

            2:  or s2, s2, t4       # used = used | element

            3:  addi s3, s3, 1      # group_index += 1
                j 1b
            4:  mv a0, s2           # return used

                # Postlude
                ld ra, 56(sp)
                ld s0, 48(sp)
                ld s1, 40(sp)
                ld s2, 32(sp)
                ld s3, 24(sp)
                ld s4, 16(sp)
                addi sp, sp, 64
                ret

# clear_used(board, group, used)
clear_used:
                # Prelude
                addi sp, sp, -64    # Make space on the stack
                sd ra, 56(sp)       # Save return address
                sd s0, 48(sp)       # Save board
                sd s1, 40(sp)       # Save group
                sd s2, 32(sp)       # Save used
                sd s3, 24(sp)       # Save group_index
                sd s4, 16(sp)       # Save element address

                mv s0, a0           # board = a0
                mv s1, a1           # group = a1
                mv s2, a2           # used = a2
                li a3, 0            # change_made = 0
                li s3, 0            # group_index = 0
                not s2, s2          # notused = ~used

            1:  li t6, 9
                bge s3, t6, 4f      # if group_index >= 9, exit loop
                add t0, s1, s3      # group_element_address = group + group_index
                lb t1, 0(t0)        # board_index = lb(group_element_address)
                slli t2, t1, 1      # scaled_board_index = board_index << 1
                add t3, s0, t2      # board_element_address = board + scaled_board_index
                lh t4, 0(t3)        # element = lh(board_element_address)
                mv s4, t3           # save element address
                mv a0, t4           # copy to a0
                sd a3, 8(sp)        # Save change_made
                call count_bits     # call count_bits
                ld a3, 8(sp)        # Restore change_made
                mv t5, a0           # t5 = count
                li t6, 1
                beq t5, t6, 2f      # if count == 1, skip

                and t0, t4, s2      # new_elt = element & notused
                bne t0, t4, 3f      # if new_elt != element, flag change_made

            2:  addi s3, s3, 1      # group_index += 1
                j 1b

            3:  sh t0, 0(s4)        # board[board_index] = new_elt
                li a3, 1            # change_made = 1
                addi s3, s3, 1      # group_index += 1
                j 1b

            4:  mv a0, a3           # return change_made

                # Postlude
                ld ra, 56(sp)
                ld s0, 48(sp)
                ld s1, 40(sp)
                ld s2, 32(sp)
                ld s3, 24(sp)
                ld s4, 16(sp)
                addi sp, sp, 64
                ret

# pencil_marks(board, table) -> 0: no changes, 1: something changed
pencil_marks:
                addi sp, sp, -40
                sd ra, 32(sp)
                sd s0, 24(sp)
                sd s1, 16(sp)
                sd s2, 8(sp)
                sd s3, 0(sp)

                mv s0, a0           # Save board pointer in s0
                mv s1, a1           # Save table pointer in s1
                li s2, 0            # Initialize changed to 0
                li s3, 0            # Initialize group_start to 0

            1:  li t1, 243          # Set upper bound for group_start (27*9)
                bge s3, t1, 4f      # Break the loop if group_start >= 243

                add t2, s1, s3      # Calculate the address of the current group
                mv a0, s0           # Prepare board argument for get_used
                mv a1, t2           # Prepare group argument for get_used
                call get_used       # Call get_used
                mv t3, a0           # Save used set in t3

                add t2, s1, s3      # Calculate the address of the current group
                mv a0, s0           # Prepare board argument for clear_used
                mv a1, t2           # Prepare group argument for clear_used
                mv a2, t3           # Prepare used set for clear_used
                call clear_used     # Call clear_used
                bnez a0, 3f         # If clear_used returned non-zero, update changed

            2:  addi s3, s3, 9      # Increment group_start by 9
                j 1b                # Jump back to the beginning of the loop

            3:  li s2, 1            # Set changed to 1
                j 2b                # Jump to continue the loop

            4:  mv a0, s2           # Move the changed flag into return register

                ld ra, 32(sp)
                ld s0, 24(sp)
                ld s1, 16(sp)
                ld s2, 8(sp)
                ld s3, 0(sp)
                addi sp, sp, 40
                ret
