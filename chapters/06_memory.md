# Memory and Storage

A computer needs memory for the program it is running and the data it is working on, and storage that keeps information while it is switched off. No single technology serves both purposes well. This chapter describes the kinds of memory in use, the purposes each suits, and how long each can be relied on to retain its contents. The last question is central to timeless computing.

## The Memory Hierarchy

Every memory technology trades speed against size, cost and permanence. Computers therefore use several kinds at once, arranged from small and fast to large and slow:

| Level                       | Typical size | Speed     | Keeps data |
|-----------------------------|--------------|-----------|------------|
| CPU registers               | 100 bytes    | fastest   | no         |
| cache                       | kilobytes    | very fast | no         |
| main memory (RAM)           | megabytes    | fast      | no         |
| storage: flash, F-RAM, disk | KB to TB     | slower    | yes        |
| archive: offline copies     | any          | slowest   | yes        |

Main memory is **random-access memory** (RAM): any address can be read or written as quickly as any other. Memory that loses its contents when power is removed is **volatile**. Memory that retains them is **non-volatile**. A computer runs from volatile memory, because it is fast and can be rewritten without limit, and keeps everything of lasting value in non-volatile storage.

## Static RAM

**Static RAM** (SRAM) stores each bit in a small loop of transistors, similar to the latch in [Digital Logic](#digital-logic). It holds its value while powered, needs no maintenance, and is fast and simple to use: when an address is placed on its pins, the data appears. Its disadvantage is size. Each bit needs about six transistors, so SRAM is expensive per bit.

Caches, and often a processor's register file, are made of SRAM, as is the **block RAM** inside an FPGA. Some small computers use an external SRAM chip of one or two megabytes as their main memory, which makes the memory controller trivial.

## Dynamic RAM

**Dynamic RAM** (DRAM) stores each bit as a small charge on a capacitor, with one transistor to reach it. This makes it dense and cheap, so it is used for main memory in nearly every computer. The charge leaks away within tens of milliseconds, however, so every row of the memory must be read and written back, or **refreshed**, typically every 64 milliseconds. DRAM also has a more complicated interface, organized in rows and columns that must be opened and closed in the correct order.

A **memory controller**, a circuit between the bus and the memory chips, handles these tasks. In an FPGA computer, the memory controller is part of the design loaded into the FPGA. Common varieties are:

- **SDRAM** (synchronous DRAM) transfers data in step with a clock.
- **DDR** SDRAM, in generations such as DDR3, transfers data on both edges of the clock, doubling the rate, at the cost of a much more demanding controller.
- **PSRAM** (pseudo-static RAM) is DRAM with its own refresh circuit built in, so that it can be used almost like SRAM.

## Read-Only Memory and Its Descendants

A computer needs some instructions to run as soon as it is switched on, before anything has been loaded. Early computers kept them in **read-only memory** (ROM), written once at the factory. Later came programmable ROMs that the user could write once, then ones that could be erased with ultraviolet light, and then **EEPROM**, which can be erased and rewritten electrically one byte at a time, though slowly and a limited number of times.

EEPROM is still common for small amounts of data, such as settings and calibration values, and retains data for a century or more.

## Flash Memory

**Flash memory** is a descendant of EEPROM that is erased in large blocks rather than byte by byte, which makes it much denser and cheaper. It is now the most common form of non-volatile storage. Each bit is a charge trapped on an insulated piece of silicon inside a transistor, where it can remain for years without power.

Three properties of flash determine how it is used:

- **It must be erased before it is written.** An erased bit reads as 1, and writing can only change 1s to 0s. To change a single byte back, the whole block containing it, often 4 KB or more, must be erased and rewritten.
- **It wears out.** Each block survives a limited number of erase cycles, often around 100,000 for the kind used to hold programs and far fewer for the densest kinds. After that it begins to fail.
- **It gradually loses data.** The trapped charge leaks. Typical retention is ten to twenty years, and less at high temperatures or in a worn block.

There are two main kinds. **NOR flash** can be read one byte at a time at any address, which makes it suitable for holding programs that run directly from it. A small NOR flash chip, connected over four wires using SPI, a serial connection described in [Talking to the World](#talking-to-the-world), holds the configuration of nearly every FPGA board. **NAND flash** is denser and is read in pages. It is used in SD cards, USB sticks and solid-state drives. Each of these contains a small controller that hides the erasing, spreads writes across the whole chip to even out the wear (**wear levelling**), and replaces bad blocks as they appear.

The controller also introduces a risk: if it fails, all the data behind it can become unreachable at once, without warning. For this reason, SD cards and USB sticks are suitable for moving data but not for keeping it for decades.

## Ferroelectric RAM

**Ferroelectric RAM** (F-RAM, or FRAM) stores each bit in the electric polarization of a small crystal, which switches one way or the other when a voltage is applied and keeps that state when the voltage is removed. It combines the main advantages of RAM and flash:

- It is non-volatile.
- It is written one byte at a time, at full speed, with no erase step.
- It can be rewritten a very large number of times, typically a trillion (10 to the 12th) or more, so that in practice it does not wear out.
- It retains data for a long time. Manufacturers typically specify around 95 years at 55 degrees Celsius and more than 200 years at 35 degrees.

Its disadvantages are capacity and cost. F-RAM chips hold from kilobytes to a few megabytes, and cost far more per bit than flash. For text, programs, keys, settings and logs that must survive for generations, the trade is worthwhile. A text document of a few pages fits in 8 KB.

**Magnetoresistive RAM** (MRAM) stores bits magnetically and has similar properties: it is non-volatile, fast, byte-writable and durable.

Two cautions apply to every retention figure. First, they are manufacturers' estimates from accelerated testing, not observations of chips that have been stored for two centuries. Second, they depend strongly on temperature: memory kept cool lasts much longer than memory kept warm.

## Other Long-Term Media

Not all storage is electronic. **Hard disks** store data magnetically on spinning platters. They are cheap and large, but their motors and bearings wear out. **Magnetic tape** is still used for archives, because it is cheap and stable when stored well, but it needs a working tape drive to read it. **Optical discs** can last decades if they are of good quality and kept dark and cool.

Paper is also a storage medium. A printout of a short program, a key or a set of instructions, kept dry, can be read in a century without any machine. For the most important information, it is a serious option.

## Errors and How to Catch Them

Storage is not perfect. A worn flash cell, a cosmic ray striking a memory chip, an interrupted write or a failing cable can each change a bit. The defence is to store a little extra information that allows errors to be detected and sometimes corrected.

- A **parity bit** records whether the number of 1s in a group of bits is odd or even. A single changed bit changes the parity and is detected.
- A **checksum** is the sum of all the bytes of a block. If the sum no longer matches, the block has changed.
- A **cyclic redundancy check** (CRC) is a more thorough kind of checksum that detects almost all accidental damage. Disks, network packets and many file formats use one.
- A **cryptographic hash**, such as SHA-256, produces a fingerprint that changes completely if even one bit of the data changes, and that cannot practically be forged. It is used to check that a file has not been altered, whether accidentally or deliberately.
- An **error-correcting code** (ECC) stores enough extra bits not only to detect a changed bit but also to identify which bit it was and correct it.

The most important practice is to read back anything important after writing it and compare it with the original. A copy that has not been verified cannot be relied on as a backup.

## Filesystems

A storage device is a long sequence of blocks. A **filesystem** is the set of rules that organizes those blocks into named files and folders. It records which blocks belong to which file and in what order, which blocks are free, and the names, sizes and dates of the files.

**FAT**, originally designed for floppy disks in the late 1970s, is the most widely understood filesystem in the world. Nearly every computer, camera and operating system can read it. For this reason it is the usual choice for SD cards and USB sticks, and a sensible choice for data that should outlast the computer that wrote it.

## Surviving Power Loss

The most difficult problem for a filesystem is a power failure in the middle of a write. Changing a file usually means changing several blocks: the data, the list of blocks and the directory entry. If power fails after some of those writes but not others, the filesystem can be left inconsistent, with a file pointing at the wrong data, or with space marked as used that belongs to no file.

Careful designs follow a few rules:

- **Never overwrite in place.** Write the new version of a file to an unused area.
- **Commit with a single write.** Once the new version is complete and checked, make it current by changing one small value, ideally one byte, that a power cut cannot leave half-written.
- **Spread the writes.** On memory that wears, use free blocks in rotation instead of always reusing the same ones.

The small filesystem used by Machdyne BASIC on its modules follows these rules. Whenever the power is cut, every file is either as it was before the operation or as it is after it; at worst, a line being appended is lost.

Large filesystems use a **journal**, a log in which each change is recorded before it is carried out, so that an interrupted change can be completed or undone at the next start.

Users should likewise let the computer finish writing before removing a card or switching off. Systems provide a command or menu item for this, often called sync, eject or unmount.

## Choosing Storage That Lasts

The following practices keep data intact for a long time:

- **Keep more than one copy**, on more than one kind of medium, in more than one place. A common rule is three copies, on two kinds of media, with one kept at another location.
- **Use plain formats.** Text files and widely documented formats will remain readable long after any particular program has gone.
- **Verify.** Check copies against each other, or against a recorded hash, at intervals, and replace any that have failed.
- **Refresh.** Copy data from ageing media to new media before the old media reaches the end of its expected life.
- **Write-protect** data that should not change. Many memory chips and devices have a write-protect pin or switch.
- **Keep the means to read it.** Storage is useful only while something can still read its interface. Prefer simple, well-documented interfaces, and keep the documentation with the data.
