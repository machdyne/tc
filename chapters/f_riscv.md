# RISC-V Reference

This appendix lists the RV32I base instruction set and the M extension, which together form RV32IM, the instruction set of the processors described in this book. The RISC-V specifications are frozen: an instruction, once ratified, keeps its meaning.

## Registers

RV32I has 32 registers of 32 bits, `x0` to `x31`, and the program counter, `pc`. Register `x0` always reads as zero, and writes to it are discarded. The other registers are alike to the hardware; their roles come from the **calling convention**, the agreement that lets separately compiled code call each other. Assemblers accept both the plain names and the convention's names.

| Register | Name   | Role                          | Kept by callee |
|----------|--------|-------------------------------|----------------|
| x0       | zero   | always zero                   | -              |
| x1       | ra     | return address                | no             |
| x2       | sp     | stack pointer                 | yes            |
| x3       | gp     | global pointer                | -              |
| x4       | tp     | thread pointer                | -              |
| x5-x7    | t0-t2  | temporaries                   | no             |
| x8       | s0, fp | saved register, frame pointer | yes            |
| x9       | s1     | saved register                | yes            |
| x10-x11  | a0-a1  | arguments, return values      | no             |
| x12-x17  | a2-a7  | arguments                     | no             |
| x18-x27  | s2-s11 | saved registers               | yes            |
| x28-x31  | t3-t6  | temporaries                   | no             |

A function receives its first eight arguments in `a0` to `a7` and returns its result in `a0`. It may change the temporaries and argument registers freely, but must restore the saved registers and `sp` before it returns. The stack grows downward, towards lower addresses, and `sp` is kept a multiple of 16.

## Instruction Formats

Every instruction is 32 bits. The six formats place the registers in the same positions wherever they occur, and the immediate is scattered in the B and J formats so that its bits, too, stay in fixed places:

```text
     31        25 24    20 19    15 14  12 11       7 6       0
R    funct7       rs2      rs1      funct3 rd          opcode
I    imm[11:0]             rs1      funct3 rd          opcode
S    imm[11:5]    rs2      rs1      funct3 imm[4:0]    opcode
B    imm[12,10:5] rs2      rs1      funct3 imm[4:1,11] opcode
U    imm[31:12]                            rd          opcode
J    imm[20,10:1,11,19:12]                 rd          opcode
```

Immediates are sign-extended: the highest bit of the immediate is copied into all the bits above it, so a 12-bit immediate holds -2048 to 2047. Branch and jump offsets count in bytes and are always even.

## RV32I

In the descriptions, `rd` is the destination register, `rs1` and `rs2` the source registers, and `imm` the immediate. "Unsigned" means the values are compared as numbers from 0 to 4,294,967,295 instead of signed numbers.

### Arithmetic and Logic

| Instruction       | Format | Effect                              |
|-------------------|--------|-------------------------------------|
| add rd, rs1, rs2  | R      | rd = rs1 + rs2                      |
| sub rd, rs1, rs2  | R      | rd = rs1 - rs2                      |
| and rd, rs1, rs2  | R      | rd = rs1 AND rs2, bit by bit        |
| or rd, rs1, rs2   | R      | rd = rs1 OR rs2                     |
| xor rd, rs1, rs2  | R      | rd = rs1 XOR rs2                    |
| sll rd, rs1, rs2  | R      | shift left by the low 5 bits of rs2 |
| srl rd, rs1, rs2  | R      | shift right, filling with zeros     |
| sra rd, rs1, rs2  | R      | shift right, copying the sign bit   |
| slt rd, rs1, rs2  | R      | rd = 1 if rs1 < rs2, else 0         |
| sltu rd, rs1, rs2 | R      | as slt, unsigned                    |
| addi rd, rs1, imm | I      | rd = rs1 + imm                      |
| andi, ori, xori   | I      | and, or, xor with imm               |
| slli, srli, srai  | I      | shift by a constant, 0 to 31        |
| slti, sltiu       | I      | set if less than imm                |
| lui rd, imm       | U      | rd = imm shifted left by 12         |
| auipc rd, imm     | U      | rd = pc + (imm shifted left by 12)  |

There is no subtract-immediate instruction: `addi` with a negative immediate does the same. Arithmetic wraps around on overflow and sets no flags; a program that needs to detect overflow compares the result.

### Loads and Stores

| Instruction          | Format | Effect                               |
|----------------------|--------|--------------------------------------|
| lw rd, imm(rs1)      | I      | load the 32-bit word at rs1 + imm    |
| lh, lhu rd, imm(rs1) | I      | load 16 bits, sign- or zero-extended |
| lb, lbu rd, imm(rs1) | I      | load 8 bits, sign- or zero-extended  |
| sw rs2, imm(rs1)     | S      | store the word in rs2 at rs1 + imm   |
| sh rs2, imm(rs1)     | S      | store the low 16 bits of rs2         |
| sb rs2, imm(rs1)     | S      | store the low 8 bits of rs2          |

Memory is addressed in bytes and is little-endian: the lowest byte of a word is stored at the lowest address. A word should be at an address that is a multiple of 4, and a halfword at a multiple of 2; a processor may refuse other accesses or perform them slowly.

### Branches and Jumps

| Instruction         | Format | Effect                              |
|---------------------|--------|-------------------------------------|
| beq rs1, rs2, label | B      | branch if rs1 = rs2                 |
| bne rs1, rs2, label | B      | branch if rs1 is not rs2            |
| blt, bge            | B      | branch if less, or greater or equal |
| bltu, bgeu          | B      | as blt and bge, unsigned            |
| jal rd, label       | J      | rd = pc + 4, then jump to label     |
| jalr rd, imm(rs1)   | I      | rd = pc + 4, then jump to rs1 + imm |

A branch reaches 4 KiB in either direction, `jal` 1 MiB. `jalr` with an address built by `lui` or `auipc` reaches anywhere.

### System

| Instruction | Effect                                         |
|-------------|------------------------------------------------|
| fence       | order memory accesses as seen by other devices |
| ecall       | call the operating system or other environment |
| ebreak      | stop for a debugger                            |

The instructions that read and write the control and status registers, which hold the processor's interrupt and trap settings, form a separate extension, Zicsr. Their use depends on the processor.

## The M Extension

| Instruction         | Effect                                        |
|---------------------|-----------------------------------------------|
| mul rd, rs1, rs2    | the low 32 bits of rs1 x rs2                  |
| mulh rd, rs1, rs2   | the high 32 bits, both signed                 |
| mulhu rd, rs1, rs2  | the high 32 bits, both unsigned               |
| mulhsu rd, rs1, rs2 | the high 32 bits, rs1 signed and rs2 unsigned |
| div rd, rs1, rs2    | rs1 / rs2, signed, rounded towards zero       |
| divu rd, rs1, rs2   | rs1 / rs2, unsigned                           |
| rem rd, rs1, rs2    | the remainder of div, with the sign of rs1    |
| remu rd, rs1, rs2   | the remainder of divu                         |

Division by zero does not stop the program: `div` and `divu` give -1 (all bits set), and `rem` and `remu` give rs1.

## Pseudo-instructions

Assemblers accept these common forms and translate them into one or two real instructions.

| Pseudo-instruction     | Meaning                  | Real instructions     |
|------------------------|--------------------------|-----------------------|
| nop                    | do nothing               | addi x0, x0, 0        |
| li rd, value           | load any 32-bit constant | lui and addi, or addi |
| la rd, label           | load an address          | auipc and addi        |
| mv rd, rs              | copy a register          | addi rd, rs, 0        |
| not rd, rs             | invert the bits          | xori rd, rs, -1       |
| neg rd, rs             | negate                   | sub rd, x0, rs        |
| seqz rd, rs            | rd = 1 if rs is 0        | sltiu rd, rs, 1       |
| beqz, bnez rs, label   | branch if zero, not zero | beq, bne with x0      |
| bgt, ble rs, rt, label | the other comparisons    | blt, bge swapped      |
| j label                | jump                     | jal x0, label         |
| call label             | call a function          | auipc and jalr ra     |
| ret                    | return from a function   | jalr x0, 0(ra)        |
