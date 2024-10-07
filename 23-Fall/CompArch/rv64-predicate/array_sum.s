                .global array_sum
                .text

# int array_sum(int *array, int count)
array_sum:
                addi   sp, sp, -80  # allocate stack space (80 bytes)
                sd     ra, 72(sp)   # save return address
                sd     s0, 64(sp)   # save s0
                sd     s1, 56(sp)   # save s1
                sd     s2, 48(sp)   # save s2
                sd     s3, 40(sp)   # save s3
                sd     s4, 32(sp)   # save s4
                add    s0, sp, 80   # s0 points to the old sp (frame pointer)

                mv     s1, a0       # s1 <- base address of the array
                mv     s2, a1       # s2 <- count

                li     s3, 0        # s3 holds the sum, initialize to 0
                li     s4, 0        # s4 is the loop counter, initialize to 0

            loop_start:
                beq    s4, s2, loop_end  # if counter == count, exit loop

                # Load array element into t0
                slli   t1, s4, 3          # calculate offset (count * 8)
                add    t1, s1, t1         # calculate address
                ld     t0, 0(t1)          # load array element

                # Call predicate function
                mv     a0, t0             # move element to a0 for function argument
                call   predicate          # call function

                # Add to sum if predicate returns 1
                bnez   a0, add_to_sum

            skip_addition:
                j      increment_and_continue

            add_to_sum:
                add    s3, s3, t0         # add element to sum

            increment_and_continue:
                addi   s4, s4, 1          # increment loop counter
                j      loop_start         # go back to the start of the loop

            loop_end:
                mv     a0, s3             # move sum to a0 (return value)
                        
                ld     ra, 72(sp)         # restore ra
                ld     s0, 64(sp)         # restore s0
                ld     s1, 56(sp)         # restore s1
                ld     s2, 48(sp)         # restore s2
                ld     s3, 40(sp)         # restore s3
                ld     s4, 32(sp)         # restore s4
                
                addi   sp, sp, 80         # deallocate stack space
                ret
