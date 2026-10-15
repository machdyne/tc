# Systems on a Chip

A **system on a chip** (SOC) places a complete computer, with its processor, memory controller, graphics and peripherals, on a single chip. The processors in phones and tablets are SOCs: each is designed once, made in millions, and cannot be changed once made. In an FPGA, an SOC is a design like any other, often called **gateware** by analogy with software. Every part of it can be read and changed. This chapter describes how an SOC is organized, and follows one small addition from hardware to software.

## Soft Processors

A processor described in an HDL and built in FPGA logic is a **soft processor**, or softcore. Some FPGAs also contain a fixed **hard processor** beside their logic, which is faster but cannot be changed.

There are many open softcores for RISC-V. Some are small and simple, completing an instruction every few cycles and using one or two thousand LUTs. Others are pipelined and add caches and memory management, at several times the size. The Zeitlos SOC uses PicoRV32, a small, well-tested RISC-V core, and also has an experimental core of its own, Zeitlos32.

A soft processor runs much more slowly than a hard one, typically at tens of megahertz. Its advantages are:

- **It can be read.** Every gate of the processor is visible in its source, so it can be audited, studied and trusted to a degree that no commercial chip allows.
- **It can be fixed.** A processor bug is corrected by changing the source and rebuilding the bitstream.
- **It can be extended.** New instructions or features can be added for a particular need.
- **It can be replaced.** A machine built with one instruction set can later be given another, by loading a different design into the same hardware.

## The Shape of an SOC

A typical FPGA computer is organized as follows:

```text
  +-------+   +--------+   +-----+          (bus masters)
  |  CPU  |   | video  |   | DMA |
  +---+---+   +---+----+   +--+--+
      |           |           |
  +---+-----------+-----------+---------------------------+
  |        bus, with an arbiter and an address decoder    |
  +---+--------+--------+--------+--------+--------+------+
      |        |        |        |        |        |
  +---+---+ +--+---+ +--+---+ +--+---+ +--+---+ +--+---+
  | boot  | |memory| | UART | | USB  | | pins | | audio|
  | ROM   | | ctrl | |      | |      | |      | |      |
  +-------+ +--+---+ +------+ +------+ +------+ +------+
               |
          external RAM
```

- The **CPU** fetches instructions and moves data over the bus.
- Other **bus masters**, such as the video circuit that reads the framebuffer and the DMA engines described in [The Computer](#the-computer), use the bus as well. An **arbiter** decides which master uses the bus when two request it at once.
- An **address decoder** turns each address into a select signal for one device.
- The **boot ROM** is a small program held in block RAM, built into the bitstream itself, so that the processor has a program to run as soon as the FPGA is configured. It is the system's firmware and its bootloader: it loads the operating system from flash.
- The **memory controller** connects the bus to external SDRAM or DDR memory.
- The **peripherals** each present a few registers on the bus.

## Adding a Device, End to End

This section traces how a program affects the physical world, using the smallest useful peripheral: one register that the processor can write and read back, whose bits drive eight LEDs. It is the simplest form of the general-purpose pins in the address map of [The Computer](#the-computer), at `0xE000_0000`.

A transfer on the bus has a few signals. The master places the **address** on the bus and, for a write, the data on **wdata** with **we** (write enable) set. The address decoder raises **sel** for the one device the address belongs to. For a read, the device answers with its data on **rdata**. Most buses, Wishbone among them, also have an **acknowledge** signal, with which the device says that the transfer is complete, so that a slow device can take several cycles. The device below always answers at once, so its acknowledge is left out.

```verilog
// A peripheral with one register: a byte the CPU can write and
// read back, whose bits drive eight LEDs.
module led_reg (
    input  wire        clk,
    input  wire        reset,
    input  wire        sel,        // the bus selects this device
    input  wire        we,         // and it is a write
    input  wire [31:0] wdata,      // the data the CPU is writing
    output wire [31:0] rdata,      // the data the CPU reads
    output wire [7:0]  leds
);
    reg [7:0] value;

    always @(posedge clk)
        if (reset)
            value <= 8'd0;
        else if (sel && we)
            value <= wdata[7:0];

    assign rdata = {24'd0, value};
    assign leds  = value;
endmodule
```

The register `value` loads the bottom byte of the bus data at a clock edge when this device is selected and the bus is writing. Its contents can be read back at any time and always drive the `leds` output.

The device is selected by the address decoder. In a system with only a few devices, the decoder can look at the top four bits alone:

```verilog
    // the address decoder: the top four bits pick the device
    wire sel = (addr[31:28] == 4'hE);
```

With this decoder the device answers at every address from `0xE000_0000` to `0xEFFF_FFFF`. A fuller decoder checks more bits, so that several devices can share the range, as the pins and their related devices do in a real system.

The `leds` output is connected to eight pins of the FPGA, and the board's constraints file says which ones. After synthesis, place and route and packing, the new bitstream contains the device.

On the software side, the function `led_on` from the chapter [C](#c) is a single line, `PINS |= 1u`, where `PINS` names the 32-bit value at address `0xE000_0000`.

A call to `led_on` proceeds as follows:

1. The compiler turns `PINS |= 1u` into an instruction that puts the address `0xE000_0000` in a register, then three more: a load from that address, an OR with 1, and a store back.
2. The load puts the address on the bus. The decoder sees `E` in the top four bits and selects `led_reg`, which places its register on `rdata`. The value comes back into a CPU register.
3. The ALU sets bit 0.
4. The store puts the address and the new value on the bus with write enable set. At the next clock edge, `value` loads the new byte.
5. The `leds` output changes, the pin goes to 3.3 V, current flows through the resistor and LED from [Electricity](#electricity), and the light comes on.

These five steps involve every layer of this book. Larger peripherals, such as a serial port, a sound mixer or a USB controller, work in the same way, with more registers and more logic behind them.

## Hardware and Software Together

Because its hardware can be changed, an FPGA computer allows a choice that ordinary computers do not: whether a task is done in software or in hardware.

Software is easier to write and change. Hardware can be much faster for some tasks, because it can perform many operations at once and does not spend cycles fetching and decoding instructions. Suitable tasks are small, regular and frequently repeated:

- copying and filling rectangles of pixels, done by a **blitter**
- drawing lines
- mixing several streams of sound
- the multiplications of large numbers on which public-key cryptography depends
- hash functions such as SHA-256

The Zeitlos SOC can include hardware for each of these, and each makes practical on a 48 MHz processor a task that would otherwise be too slow. The usual approach is to write everything in software first, measure where the time is spent, and move only the slowest part into hardware, behind a few registers.

## Moving a Design to Another Board

A design written in an HDL is not tied to one board, and moving it to another is the most common way of adapting an FPGA computer. Most of the design is unchanged: the processor, the bus, the peripherals, the address map and every program that runs on them. The changes concern the physical board:

- **Pins.** The constraints file is rewritten for the new board: which FPGA pin carries each signal, and with what voltage standard. Every pin must suit the voltage of its bank.
- **Clocks.** The new board's crystal may run at a different frequency, so the PLL settings change. A slower or fuller chip may not meet timing at the old clock speed, and the design may need to run slower.
- **Memory.** SRAM, SDRAM, DDR and PSRAM each need a different memory controller, with timings for the particular chip. The memory size changes what software can do.
- **Chip-specific blocks.** PLLs, block RAM, special I/O cells and differential outputs differ between FPGA families. A well-organized design keeps each of them in a small wrapper module, so that only the wrapper changes.
- **Capacity.** A smaller chip may not hold everything. Optional parts, such as accelerators or a second serial port, are left out with a configuration switch.
- **Outputs.** VGA, HDMI and composite video, USB and audio each depend on what the board has.

The usual practice is to keep everything board-specific in one place: a top-level module, a constraints file and a short list of configuration settings for each board. A new board is then brought up in small steps: first a blinking LED, to confirm the clock, the pins and the programming method; then a serial port, for messages; then a memory test; and finally the full system. One SOC design can thus support a whole family of boards, including boards from other makers.

## Linux on an FPGA

Linux can also run on an FPGA computer. It needs a softcore with a memory management unit, as described in [Operating Systems](#operating-systems), and at least tens of megabytes of memory. LiteX, an open framework for building SOCs, can generate a Linux-capable system for many FPGA boards.

Kakao Linux, a small distribution for Machdyne's larger computers, is built this way. Linux provides thousands of existing programs, at the cost of size, complexity and start-up time. A system designed for the hardware can be small enough to be understood completely. With the configuration flash on a removable module, the same computer can run either.

## Recreating Old Machines

An FPGA can also be configured as a computer from the past. Projects have recreated, closely and sometimes down to individual gates, the processors and custom chips of the Apple II, the Commodore 64, the Amiga, early game consoles and many more, from documentation, from careful measurement and sometimes from microscope photographs of the original chips.

This differs from ordinary emulation, in which a program on a modern processor imitates the old one instruction by instruction. The FPGA becomes hardware that behaves like the original, clock cycle by clock cycle, so software that depended on precise timing also runs correctly. It is one of the most reliable ways to preserve old software, and shows that a computer's design can outlive the chips it was first made from, which is a central aim of timeless computing.
