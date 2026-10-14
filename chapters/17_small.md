# Small Computers

Not every part of a system needs hardware that can be redesigned. Most computers in the world have no screen and no keyboard. They are built into keyboards, chargers, washing machines, cars and storage devices, and each runs one program for its whole life. These are **microcontrollers**, and they are well suited to many timeless applications, especially automation. This chapter describes them, and explains how small programmable modules can be combined with a larger computer to build systems that last.

## Microcontrollers

A **microcontroller** is a complete computer on one inexpensive chip, with a processor, flash memory for its program, a small amount of RAM and a set of built-in peripherals. Typical peripherals are:

- general-purpose pins
- timers, for measuring time and producing PWM signals
- analog-to-digital converters
- UART, SPI and I2C controllers

A small RISC-V microcontroller might have 16 KB of flash and 2 KB of RAM. This is enough for reading sensors, switching outputs and making decisions many thousands of times a second.

Unlike an FPGA computer, a microcontroller is fixed. Its processor and peripherals are set by the manufacturer; only the program can be changed. In return, a microcontroller is cheap, small, easy to use and economical with power. Many can sleep on a few microamps and wake on a timer or a pin change, so they can run for years from a small battery.

The program in a microcontroller is called its **firmware**. It is usually written in C, compiled on another computer, and written into the chip's flash through a programming interface: either a debug connection of one or two wires, or a small resident program called a **bootloader** that accepts new firmware over a serial port or USB.

## An Interpreter on the Chip

Alternatively, an interpreter can be written into a microcontroller's firmware once, and programs sent to it afterwards as text. Machdyne's modules work this way, with Machdyne BASIC as their firmware.

This approach has several advantages for timeless computing:

- **No toolchain is needed** to change a program. Any computer, or any device that can send text over a serial line or a bus, can program the module.
- **Programs are readable.** The program inside the module is plain text that can be listed, read and changed in place years later, by someone who has never seen it before.
- **Programs are portable.** A BASIC program does not depend on the chip that runs it, so it can be moved to a different module when the old chip is no longer made.

The disadvantage is speed. An interpreted program runs many times more slowly than compiled firmware. For a controller that checks a temperature once a second, this does not matter.

## Modules

A **module**, in this sense, is a microcontroller on a small circuit board, with enough around it to be useful on its own and a standard set of contacts for connecting it to a larger system.

Machdyne's modules are designed to last. Each combines a RISC-V microcontroller with long-lived non-volatile memory, either F-RAM or EEPROM, which holds its programs and data as files. The first of them, the LS10, has a microcontroller with 16 KB of flash and 2 KB of RAM, and 8 KB of F-RAM. The modules fit a 12-pin footprint that can be soldered to a board, pushed into a socket or plugged into a six-pin Pmod connector. The first six pins follow a standard called **Sechs**.

## The Sechs Interface

Sechs, German for "six", defines six contacts:

| Pin | Name | Use                   |
|-----|------|-----------------------|
| 1   | A    | shared I2C bus: clock |
| 2   | B    | shared I2C bus: data  |
| 3   | C    | the module's own I/O  |
| 4   | D    | the module's own I/O  |
| 5   | GND  | ground                |
| 6   | 3V3  | 3.3 V power           |

Pins A and B form an I2C bus, as described in [Talking to the World](#talking-to-the-world), which is shared by every module connected to it. Pins C and D belong to each module, for its sensor, its output, a local I2C device or a serial console.

Sechs describes three roles:

- a **module**, which runs programs
- a **carrier**, the board a module plugs into, which supplies power and determines the use of pins C and D
- a **master**, usually a host computer, which controls modules over the shared bus

Over the bus, a host can find every module by scanning addresses and ask each one what it is. It can stop and start a module's program, read and write its sixteen program registers, send it a new program, and open a console to type commands into it directly. A new module answers at a default address, and the host can assign each module its own address so that several can share a bus.

The safety rules described in [Talking to the World](#talking-to-the-world) make this robust. Sechs is still a draft standard, and the details of its registers may change, but these rules are its foundation. A module keeps its pins inactive at power-on. It always gives the host a short period after power-on in which to stop it, so that no program, however faulty, can make the module unreachable. A new program replaces the old one only after it has arrived complete and been checked.

## Building Systems from Modules

Modules allow a larger system to be built by giving each task its own small computer.

```text
                    +------------------------+
                    |   host computer        |
                    |   (logs, displays,     |
                    |    sets thresholds)    |
                    +-----------+------------+
                                |  two-wire bus (A, B)
          +---------------------+---------------------+
          |                     |                     |
   +------+------+       +------+------+       +------+------+
   | module:     |       | module:     |       | module:     |
   | heater      |       | soil sensor |       | water pump  |
   +------+------+       +------+------+       +------+------+
          | C, D                | C, D                | C, D
    sensor, relay         moisture probe         pump relay
```

In this greenhouse, each module runs its own `BOOT` program, like the heater controller in [BASIC](#basic). Each module continues to work if the host is switched off or fails. The host reads each module's registers to log and display its state, and writes registers to change settings. A failed module can be replaced with a spare and reprogrammed in minutes, while the rest of the system continues to run.

This design follows the principles in [Timeless Computing](#timeless-computing). Each part is simple enough to be understood completely, and each can be replaced. A failure affects one part rather than the whole system. The programs are stored as text in long-lived memory, so whoever maintains the system in future can read and change them.

## Portability: Machines and Languages

There are two general ways to make programs outlive the hardware they were written for. The first is a common **instruction set**, or virtual machine: every device runs the same machine code, either directly or through a small interpreter. The second is a common **language**: every device accepts the same source programs and runs them in whatever way suits its chip.

Machdyne's modules have used both. Their predecessor, the Zwölf platform, defined a small 8-bit processor with a stack and a few instructions, which every module was to implement regardless of the chip it was built from. Sechs keeps the six-pin interface but does not define a common instruction set. Portability comes instead from Machdyne BASIC, which can be interpreted on some chips and could be compiled on others.

A common instruction set makes compiled programs portable, and many systems have used one, from early educational computers to modern bytecode languages. A common language is simpler to build, and leaves each device free to run programs in its own way. In either case, what matters is a stable, documented layer between the programs and the hardware, so that either can change without the other.

## Module Lifetime

Two measures describe the life of a small device. **Data retention** is how long its memory keeps what was written to it. For F-RAM, as described in [Memory and Storage](#memory-and-storage), it is rated in centuries. The **functional life** of the device as a whole depends on its other parts: the microcontroller, the solder joints, the connectors, the capacitors and its operating conditions, and it is generally shorter.

Modules address this in the same way as the rest of the book. The important information is kept in the most durable form, the parts are cheap and replaceable, and the design and documentation are open, so that a replacement can always be made.

The next part combines this material in one complete machine.
