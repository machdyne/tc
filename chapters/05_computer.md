# The Computer

A computer is a machine that follows a list of instructions stored in its own memory. This idea, the **stored program**, distinguishes a computer from a calculator. Because instructions are numbers in memory, a computer can load a new program in the same way as new data, and can also write programs for itself. This chapter describes how the parts from [Digital Logic](#digital-logic) are combined into a computer.

## The Parts of a Computer

Every computer, from a small module to a data centre server, has the same basic parts:

```text
   +-------+        +--------+        +--------------+
   |  CPU  |<======>|  bus   |<======>|    memory    |
   +-------+        +--------+        +--------------+
                       ^  ^
                       |  |
            +----------+  +-----------+
            |                         |
     +-------------+          +---------------+
     |  keyboard,  |          |  display,     |
     |  storage... |          |  network...   |
     +-------------+          +---------------+
          input / output devices (I/O)
```

- The **central processing unit** (CPU), or processor, follows the instructions.
- **Memory** holds the instructions and the data they operate on.
- **Input and output devices** (I/O) connect the computer to people and to other machines.
- The **bus** is the set of wires, and the rules for using them, that connects the other parts.

## Inside the CPU

A CPU contains a few kinds of part, all of which appeared in the previous chapter.

**Registers** are a small set of fast storage locations inside the CPU, each holding one word. A RISC-V processor, the kind used throughout this book and described in the next section, has 32 general-purpose registers, named `x0` to `x31`, each 32 bits wide. Register `x0` always reads as zero, which provides a constant zero wherever an instruction needs one. (The smallest RISC-V variant, used in some microcontrollers, has only 16 registers.) Arithmetic is performed between registers, so a program keeps its working values there.

The **program counter** (PC) is a register that holds the memory address of the next instruction.

The **arithmetic logic unit** (ALU) adds, subtracts, compares and performs bitwise logic on values from the registers.

The **control unit** is a state machine that steps through each instruction and directs the other parts.

## The Instruction Set

The set of instructions a CPU understands, and the exact effect of each, is its **instruction set architecture** (ISA). The ISA is a contract between hardware and software: a program written for an ISA runs on any processor that implements it, whoever built the processor and however it is built inside.

This book uses **RISC-V**, an open ISA first published in 2011 that anyone may implement without a licence. It is the ISA of the processors in Machdyne's computers and of the microcontrollers in its modules. It was designed to be simple and regular, which also makes it easier to learn.

The base RISC-V instruction set, called RV32I, has about forty instructions of a few kinds:

| Kind                | Examples            | Purpose                      |
|---------------------|---------------------|------------------------------|
| arithmetic, logic   | add sub and or addi | compute with registers       |
| shifts, comparisons | sll srl slt         | shift bits; set if less than |
| loads and stores    | lw sw lb sb         | move data to and from memory |
| branches            | beq bne blt         | jump if a condition holds    |
| jumps               | jal jalr            | jump and save return address |
| constants           | lui auipc           | build large numbers          |

Optional **extensions** add further instructions. The M extension adds multiplication and division; others add floating point, compressed 16-bit instructions and other features. A processor's full ISA is written as a name such as RV32IM: 32-bit, base integer set, plus multiply and divide.

Instruction sets are sometimes divided into **CISC** (complex instruction set computer), with many powerful instructions of varying lengths, as in the x86 family, and **RISC** (reduced instruction set computer), with fewer, simpler and more regular instructions, as in ARM and RISC-V. The distinction has become less clear over the years, but simple, regular instruction sets remain easier to build, to fit into an FPGA and to understand.


## Fetch, Decode, Execute

A CPU runs a program by repeating three steps indefinitely:

1. **Fetch.** Read the instruction at the address in the program counter.
2. **Decode.** Determine what the instruction requires: which operation, which registers and which constant.
3. **Execute.** Perform the operation and write the result to a register or to memory. Then advance the program counter to the next instruction, 4 bytes further on, unless the instruction was a jump or a taken branch.

The following RISC-V program adds the numbers from 10 down to 1. The text after each `#` is a comment.

```asm
        addi x5, x0, 10      # x5 = 0 + 10        the counter
        addi x6, x0, 0       # x6 = 0 + 0         the running total
loop:   add  x6, x6, x5      # x6 = x6 + x5
        addi x5, x5, -1      # x5 = x5 - 1
        bne  x5, x0, loop    # if x5 is not 0, go back to loop
```

After the first two instructions, `x5` is 10 and `x6` is 0. The first pass through the loop makes `x6` 10 and `x5` 9; since 9 is not zero, the branch returns to `loop`. The tenth pass makes `x6` 55 and `x5` 0, and the branch is not taken. The processor has run 32 instructions to compute 55.

## Machine Code and Assembly

The program above is written in **assembly language**, which has one line per instruction and readable names. The CPU cannot read text. A program called an **assembler** translates each line into the 32-bit number that the CPU decodes, its **machine code**. The first instruction, `addi x5, x0, 10`, becomes the number `0x00A00293`. Divided into its fields:

```text
  000000001010   00000   000    00101   0010011
  immediate=10   rs1=x0  addi   rd=x5   opcode: arithmetic with a constant
```

`addi` means *add immediate*: one of its operands is a constant, the **immediate**, stored inside the instruction itself. The **opcode** identifies the kind of instruction, `rd` names the destination register, and `rs1` names the source register.

The decoder in the CPU is a combinational circuit that divides the word into these fields and sets the multiplexers and the ALU accordingly. The fields occupy the same positions in most instructions, which keeps the decoder small.

Labels such as `loop` are a convenience of the assembler. In the machine code, the branch holds the distance to its target, here -8 bytes, and the CPU adds this distance to the program counter.

Large programs are now rarely written in assembly. Higher-level languages, the subject of [Thinking in Programs](#thinking-in-programs), are translated into machine code by a compiler or run by an interpreter. Every program, in any language, is finally run as a sequence of instructions like these.

## Memory and Addresses

Memory is a long sequence of bytes, each identified by a number called its **address**. A 32-bit processor can name 2 to the 32nd addresses, which is 4 GiB. A small computer has far less memory than that, and the remaining addresses are used for other purposes, as described below.

RISC-V is a **load-store** architecture. Arithmetic operates only on registers, and separate instructions move data between registers and memory:

```asm
        lw   x7, 0(x10)      # load the word at the address in x10 into x7
        sw   x7, 4(x10)      # store x7 at that address plus 4
```

A 32-bit word occupies four consecutive bytes. RISC-V stores the least significant byte at the lowest address, an arrangement called **little-endian**. The value `0x12345678` stored at address 100 places `0x78` at 100, `0x56` at 101, `0x34` at 102 and `0x12` at 103. Some other processors use the opposite order, **big-endian**, and data moved between the two must have its bytes swapped.

## Subroutines and the Stack

Programs reuse pieces of code by calling them as **subroutines**, also called functions or procedures. The jump-and-link instruction `jal` jumps to a subroutine and saves the address of the following instruction in a register, by convention `x1`, the return address. At its end, the subroutine jumps back to that address with `jalr`.

A subroutine that calls another subroutine would overwrite `x1`, so it must first save the old value. It saves it on the **stack**, an area of memory in which the last item stored is the first removed. A register, by convention `x2`, the stack pointer, holds the address of the top of the stack. A subroutine makes room by lowering the stack pointer and saves the registers it must preserve. Before it returns, it restores them and raises the pointer again. Each active call has its own **frame** on the stack, which also holds its local variables.

The stack allows one function to call another, which calls another, to any depth the memory allows, and gives each call its own copies of its variables. When a program runs out of stack space, usually because a function calls itself without stopping, the result is a **stack overflow**.

## The Bus and the Address Map

The CPU, memory and devices are connected by the **bus**: wires for an address, wires for data, and a few control signals that indicate whether a transfer is a read or a write and when it is complete.

Every device on the bus is assigned a range of addresses. A decoder examines the top bits of each address and enables the one device to which it belongs. The resulting list of which device answers at which address is the computer's **address map**. The following is a simplified map of the Zeitlos system on a chip described in [The Machine](#the-machine):

| Address     | Device                          |
|-------------|---------------------------------|
| 0x0000_0000 | boot program, in on-chip memory |
| 0x1000_0000 | flash memory                    |
| 0x2000_0000 | video memory: the screen        |
| 0x4000_0000 | main memory (RAM)               |
| 0xE000_0000 | general-purpose pins            |
| 0xF000_0000 | serial port                     |

The address alone determines which device is used. A store to `0x4000_0000` changes memory; a store to `0x2000_0000` changes pixels on the screen.

The bus inside Zeitlos follows Wishbone, an open standard. Other systems use other buses, which perform the same function.

## Memory-Mapped I/O

In the map above, the screen, the pins and the serial port are not reached with special instructions; they have addresses in the same way as memory. Storing a value at a device's address sends it to the device, and loading from the address reads from the device. This is **memory-mapped I/O**, and nearly every modern processor communicates with hardware in this way.

The addresses a device answers to are its **registers**, which are distinct from the CPU's registers. A typical device has a few:

- a **data** register, holding a value to send or one just received
- a **status** register, whose bits report conditions such as "a byte has arrived" or "ready to send"
- a **control** register, whose bits turn features on and off

Suppose that storing a word at `0xE000_0000` sets a row of output pins to its lowest bits. (On a real machine, the individual pin registers each have their own address within this range, given in the machine's documentation.) These two RISC-V instructions then place the total computed earlier on the pins:

```asm
        lui  x7, 0xE0000     # x7 = 0xE000_0000, the pins' address
        sw   x6, 0(x7)       # send x6 to the pins
```

Software therefore affects the physical world with a store to the appropriate address. The chapter [Systems on a Chip](#systems-on-a-chip) follows such a register from the hardware design to the program that uses it.

## Interrupts

A program can monitor a device by reading its status register repeatedly until it changes. This is called **polling**. It is simple, but the processor can do nothing else while it waits.

An **interrupt** allows the device to request attention instead. When a key is pressed, for example, the keyboard circuit raises an interrupt signal. The CPU finishes its current instruction, saves the program counter and jumps to a routine called an **interrupt handler**. The handler reads the key, stores it and returns, and the interrupted program continues as if it had not been interrupted.

A **timer** is the most important source of interrupts. It counts clock cycles and raises an interrupt at regular intervals, for example a thousand times a second. These regular interrupts allow an operating system to share one processor between several programs, as described in [Operating Systems](#operating-systems).

## Direct Memory Access

Some tasks involve moving large amounts of data: filling the screen, copying a file into memory or sending a network packet. The CPU can do this one word at a time, but some devices can do it themselves. A device that can read and write memory over the bus without the CPU is a **bus master**, and the technique is called **direct memory access** (DMA). A common example is a graphics engine that copies rectangles of pixels, often called a **blitter**. The CPU configures it with a few register writes and continues with other work while the copy proceeds.

## Caches

Processor speeds have increased much faster than memory speeds. Reading a word from main memory can take many clock cycles, during which a simple CPU waits.

A **cache** is a small, fast memory inside the processor that keeps copies of recently used memory. When the CPU needs a word, it checks the cache first. A **hit** is fast. A **miss** fetches the word from main memory, usually together with its neighbours, and keeps them in the cache.

Caches are effective because programs access memory in two predictable ways. A program that uses a location is likely to use it again soon, as loops do. A program that uses a location is also likely to use its neighbours soon, as when reading through an array or running instructions in sequence. As a result, a small cache can serve most accesses.

Caches have costs. They make timing less predictable, and they must never hold copies of device registers, whose values can change without the CPU's knowledge. Systems therefore mark device address ranges as uncached.

## Speed

A processor's speed depends on two factors: the number of clock cycles it runs per second, and the work it does per cycle, measured as **instructions per cycle** (IPC).

A simple processor takes several cycles per instruction: one to fetch, one to decode, and so on. A **pipelined** processor overlaps these steps, fetching the next instruction while decoding the current one, in the manner of an assembly line, and can approach one instruction per cycle. Large modern processors go much further. At billions of cycles per second, they run several instructions at once, predict the outcome of branches before it is known, and reorder instructions as they run.

A simple 32-bit processor in an FPGA, running at 48 MHz and completing an instruction every four or five cycles, performs roughly ten million instructions per second. This is a thousand or more times slower than a modern desktop computer. It is sufficient to edit text, run a spreadsheet, browse simple web pages, play music and control machinery, provided the software is written with care.
