# Add the numbers from 10 down to 1 (The Computer). sum.out holds the
# machine code the chapter quotes: 0x00A00293 for the first line, and
# a branch back of -8 bytes.
        addi x5, x0, 10      # x5 = 0 + 10        the counter
        addi x6, x0, 0       # x6 = 0 + 0         the running total
loop:   add  x6, x6, x5      # x6 = x6 + x5
        addi x5, x5, -1      # x5 = x5 - 1
        bne  x5, x0, loop    # if x5 is not 0, go back to loop
