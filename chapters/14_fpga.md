# Inside an FPGA

A field-programmable gate array is a chip containing many identical, uncommitted logic blocks, with programmable wiring between them. A configuration file sets up and connects those blocks to form the circuit it describes, such as a blinking light, a serial port or a complete computer. This chapter describes what is inside an FPGA and how a design becomes a configuration.

## The Big Picture

An FPGA has four main kinds of component, arranged in a regular grid:

```text
   +-----+-----+-----+-----+-----+-----+
   | I/O | I/O | I/O | I/O | I/O | I/O |      I/O blocks around the edge
   +-----+-----+-----+-----+-----+-----+
   | I/O | LB  | LB  | RAM | LB  | I/O |
   +-----+-----+-----+-----+-----+-----+      LB:  logic blocks
   | I/O | LB  | LB  | RAM | LB  | I/O |      RAM: block RAM
   +-----+-----+-----+-----+-----+-----+      DSP: multipliers
   | I/O | LB  | DSP | LB  | LB  | I/O |
   +-----+-----+-----+-----+-----+-----+      all joined by programmable
   | I/O | I/O | I/O | I/O | I/O | I/O |      routing between the blocks
   +-----+-----+-----+-----+-----+-----+
```

- **Logic blocks** implement the gates and flip-flops of a design.
- **Routing** connects the blocks to each other, through a mesh of wires and programmable switches.
- **Memory and arithmetic blocks** provide dedicated RAM and multipliers, which would be wasteful to build from logic blocks.
- **I/O blocks** connect the inside of the chip to its pins.

An FPGA has thousands or tens of thousands of logic blocks. Which blocks are used, how each is set up and how they are connected is held in **configuration memory** distributed throughout the chip. In most FPGAs, including all of those in Machdyne's computers, this memory is SRAM. Its contents are lost when power is removed, so the configuration must be loaded again at every start.

## Look-Up Tables

The main element of a logic block is the **look-up table**, or LUT. A 4-input LUT is a memory of sixteen bits. Its four inputs form an address from 0 to 15, and its output is the bit stored at that address.

As described in [Digital Logic](#digital-logic), any function of four inputs is completely described by a truth table of sixteen rows. A LUT stores that truth table. With the appropriate sixteen bits loaded, it acts as an AND gate, an XOR gate, a multiplexer or any other function of up to four inputs, with the same delay whatever the function. For this reason an FPGA can implement any logic design: it contains no fixed gates, only small memories that can take the place of any gate.

The sixteen bits are part of the FPGA's configuration. Design tools usually write them as one 16-bit number, often called `INIT`, whose bit 0 is the output for address 0, bit 1 the output for address 1, and so on. To make a LUT compute the XOR of inputs 0 and 1, the required output is listed for each address. For addresses 0, 1, 2 and 3, the two low bits are 00, 01, 10 and 11, so the outputs are 0, 1, 1, 0, which is binary `0110`, hex 6. The two upper inputs do not affect the result, so the same pattern repeats four times: `INIT = 16'h6666`. For an AND of all four inputs, only address 15 gives 1: `16'h8000`.

Functions of more than four inputs are divided among several LUTs. A full adder from [Digital Logic](#digital-logic), with three inputs and two outputs, requires two: one for the sum and one for the carry.

Different FPGA families use LUTs with 4 to 6 inputs, but the principle is the same.

## Flip-Flops and Carry Chains

Each LUT in a logic block is paired with a **flip-flop**, so that its output can be stored at a clock edge. Together they form a small piece of combinational logic followed by a register, which is the basic unit of synchronous design.

Logic blocks also contain **carry chains**: dedicated, fast connections that pass the carry from one block to the next. Adders and counters are common enough that FPGAs provide this special path rather than sending the carry through general routing. A 24-bit counter on an ECP5 FPGA, for example, uses 24 flip-flops and 12 carry cells, each of which adds two bits.

## Routing

Most of an FPGA's area is occupied by **routing** rather than logic: wires of various lengths running between the blocks, and programmable switches where they cross. Each switch is controlled by one bit of configuration memory.

Much of the delay in an FPGA is caused by routing. A signal that crosses the chip through many switches takes longer than one that travels to a neighbouring block. For this reason the same design can reach different clock speeds depending on how its parts are placed, and an FPGA runs a given circuit several times more slowly than a custom chip, in which the connections are direct metal wires.

## Block RAM and DSP Blocks

Memory built from LUTs and flip-flops would use them up quickly. FPGAs therefore include **block RAM**: dedicated SRAM blocks of a few kilobits each, distributed across the chip. A design uses them wherever it needs fast on-chip memory, such as a processor's caches and boot program, a screen font or buffers for incoming data. An FPGA with fifty-six 18-kilobit blocks has about 126 KB of block RAM, which is small compared with external memory but much faster.

**DSP blocks** are dedicated multipliers, often with adders attached, used for arithmetic in signal processing, graphics and cryptography. A multiplier built from LUTs would be large and slow; a DSP block performs a multiplication in one clock cycle.

## I/O Blocks

Each pin of an FPGA has an **I/O block** that can be configured as an input, an output or both. The configuration sets its voltage standard, its drive strength, whether it has a pull-up resistor, and whether it captures data on a clock edge at the pin itself. Pairs of pins can be used together for **differential** signals, which carry fast data on two wires with opposite polarity and are used for HDMI and other high-speed links. Some FPGAs have dedicated high-speed serializers at their pins for this purpose.

Every I/O block belongs to a **bank** of pins that share a supply voltage. The board designer chooses that voltage, commonly 3.3 V, and every pin in the bank must use it.

## Clocks

FPGAs contain **global clock networks**: routing designed to deliver a clock signal to every flip-flop on the chip at very nearly the same time. Ordinary routing cannot do this.

They also contain one or more **phase-locked loops** (PLLs), circuits that take a clock from an external crystal and produce clocks at other frequencies. A board with a 12 MHz crystal can use a PLL to produce a 48 MHz clock for its processor and a 25 MHz clock for its video output.

## Configuration

The file that sets every LUT, flip-flop, switch and pin is called a **bitstream**. It is produced by the tools described in [Describing Hardware](#describing-hardware) and is typically between a few hundred kilobytes and a few megabytes in size.

At power-on, an FPGA reads its bitstream from a small SPI flash chip beside it, which takes a fraction of a second. The circuit it describes starts to run only after this. For testing, a bitstream can also be sent directly from another computer over a USB cable, in which case it remains until the power is turned off.

On some boards, including many of Machdyne's, the flash chip is on a small removable module. Replacing the module replaces the whole design of the computer, so the same board can be one kind of computer with one module and an entirely different one with another. The flash can hold more than one bitstream, and some FPGAs can be instructed to reload themselves from a different address, so that a running design can pass control to another.

## FPGA Capacity

FPGA capacity is usually stated in LUTs. Boards for hobbyists and small computers, including Machdyne's, use chips with a few thousand to tens of thousands of LUTs. Typical sizes of designs are:

| Design                          | LUTs, roughly  |
|---------------------------------|----------------|
| blinking an LED                 | a dozen or two |
| a serial port                   | a few hundred  |
| a small 32-bit RISC-V processor | 1,000 to 3,000 |
| the complete Zeitlos computer   | about 19,000   |

The full Zeitlos system, with its processor, caches, memory controller, graphics, USB, audio and cryptographic accelerators, fills about three quarters of a 25,000-LUT FPGA and less than half of a 45,000-LUT one, which leaves room for additions.

## FPGA Families and Open Tools

Several companies make FPGAs. Several families have open-source tools, written by people who studied the chips and documented their configuration formats:

- **Lattice iCE40**: small, simple, low-power FPGAs, the first to have a complete open toolchain.
- **Lattice ECP5**: larger FPGAs with DSP blocks and ample block RAM, the main family in Machdyne's computers.
- **Xilinx (AMD) 7-series**: large, fast FPGAs such as the Artix-7, with growing open support.
- **Cologne Chip GateMate**: FPGAs designed and made in Germany, with open-source synthesis from the start and now a fully open toolchain.

Open tools are important for timeless computing. A design that can be built only with one company's licensed software can be maintained only while that software is available and runs on current computers. A design built with open tools, whose own source code can be rebuilt, can be maintained indefinitely.

## FPGAs, Processors and Custom Chips

An FPGA can be compared with a microcontroller (MCU), which is a small processor chip with built-in devices, and with a custom chip, or ASIC (application-specific integrated circuit):

|               | MCU                | FPGA               | ASIC           |
|---------------|--------------------|--------------------|----------------|
| What it is    | fixed CPU, devices | programmable logic | fixed logic    |
| Changed by    | new software       | new bitstream      | a new chip     |
| Speed         | modest             | modest             | highest        |
| Power         | lowest             | low to moderate    | lowest per job |
| Cost each     | lowest             | moderate           | lowest in bulk |
| Start-up cost | very low           | low                | enormous       |

A microcontroller is suitable when its built-in processor and devices fit the task; most small controllers, including Machdyne's modules, are microcontrollers. A custom chip is suitable when millions will be made and the design will not change. An FPGA is suitable when the hardware itself must be designed, studied or changed: for parallel processing, unusual interfaces, recreations of old machines, and computers whose owners can inspect and improve the processor.

An FPGA also protects a design against obsolescence. A processor design written in a hardware description language is not tied to any one chip. When a particular FPGA goes out of production, the design can be moved to another, with the adjustments described in [Moving a Design to Another Board](#moving-a-design-to-another-board). In this way the computer can outlast the chip it was first built on.
