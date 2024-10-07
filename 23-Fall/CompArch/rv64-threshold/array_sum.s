                .global array_sum
                .text

# int array_sum(int *array, int count, int threshold)
array_sum:
                li t0, 0        # sum = 0
                li t1, 0        # i = 0

            1:  bge t1, a1, 3f  # Check if i < count

                # Load array[i] into t2
                slli t3, t1, 3  # i * 8 (since each int is 8 bytes)
                add t3, a0, t3  # array + i * 8
                ld t2, 0(t3)    # load array[i] into t2
                blt t2, a2, 2f  # Check if array[i] >= threshold
                add t0, t0, t2  # Add array[i] to sum

            2:  addi t1, t1, 1  # i += 1
                j 1b

            3:  mv a0, t0 # Return sum
                ret
