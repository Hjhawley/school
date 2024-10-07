                .global _start
                .equ    sys_exit, 93

                .data
msg_pencil:     .asciz  "\nBoard with up-to-date pencil marks:\n"
test_row_msg:   .asciz  "\nTesting single_pass on row "
test_col_msg:   .asciz  "\nTesting single_pass on column "
test_group_msg: .asciz  "\nTesting single_pass on 3x3 group "
return_val_msg: .asciz  "The return value is: "
newline:        .asciz  "\n"
new_board_msg:  .asciz  "After calling single_pass the board is:\n\n"

                .text
_start:
				.option	push
				.option norelax
				la		gp, __global_pointer$
				.option pop

                # s0: board
                # s1: table

                # reserve stack space for a board
                # 81*2 = 162 so reserve 176
                addi    sp, sp, -176
                mv      s0, sp

                # reserve stack space for the table
                # 27*9 = 243 so reserve 256
                addi    sp, sp, -256
                mv      s1, sp

                # read a board from stdin
1:              mv      a0, s0
                call    read_board
                bnez    a0, 1b

                # generate the lookup table
                mv      a0, s1
                call    make_group_table

                # call pencil_marks
2:              mv      a0, s0
                mv      a1, s1
                call    pencil_marks

                # repeat until no changes made
                bnez    a0, 2b

                # print the board
                la      a0, msg_pencil
                call    puts
                mv      a0, s0
                call    print_board

                # s2: i
                # for i from [0, 27] step 11 mod 27
                li      s2, 0

3:              li      t0, 9
                bge     s2, t0, 4f
                la      a0, test_row_msg
                call    puts
                mv      a0, s2
                call    print_n
                j       6f

4:              li      t0, 18
                bge     s2, t0, 5f
                la      a0, test_col_msg
                call    puts
                addi    a0, s2, -9
                call    print_n
                j       6f

5:              la      a0, test_group_msg
                call    puts
                addi    a0, s2, -18
                call    print_n

6:              la      a0, newline
                call    puts

                # call single_pass
                mv      a0, s0
                li      t0, 9
                mul     t1, s2, t0
                add     a1, s1, t1
                la      a4, single_pass
                call    call_function
                mv      s4, a0

                la      a0, return_val_msg
                call    puts
                mv      a0, s4
                call    print_n
                la      a0, newline
                call    puts

                # print the updated board
                la      a0, new_board_msg
                call    puts
                mv      a0, s0
                call    print_board

                # next
                addi    s2, s2, 11
                li      t0, 27
                rem     s2, s2, t0
                bnez    s2, 3b

                # clean up stack
                addi    sp, sp, 256
                addi    sp, sp, 176

                # exit
                li      a0, 0
                li      a7, sys_exit
                ecall
