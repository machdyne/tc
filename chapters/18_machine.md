# The Machine

The previous chapters described computers in general. This chapter describes a particular computer: a Machdyne FPGA computer running Zeitlos. It does not assume that the reader has one. It explains how the ideas of this book appear in a real machine, how it can be adapted, and how it can be returned to a working state when an experiment goes wrong.

Zeitlos changes quickly, and the system's own documentation describes it in exact detail. This chapter gives an overview that makes that documentation easier to read.

## What It Is

With a keyboard, mouse, monitor and USB power supply connected, the machine starts to a graphical desktop. The screen is 640 by 480 pixels in a single colour, in the manner of early workstations: white, amber or green on black, or black on white like paper. A dock along the bottom starts programs, and windows can be moved, resized and stacked.

The programs supplied with it cover the timeless applications listed in [Timeless Computing](#timeless-computing): a text editor, a file browser, a document reader, a spreadsheet, a calculator, a calendar and clock, a terminal, an image viewer, music and sound players, a web browser for simple pages, Gopher and Gemini, and a chat client, along with games and educational programs. This book is among the documents it carries.

The core of the system, consisting of the kernel, the drivers, the window manager, the terminal, the editor, the file browser and the Scheme language, is stored in the computer's flash memory, so the machine works with no storage card at all. A microSD card adds further programs and space for files.

## The Hardware

Machdyne makes several FPGA computers, and Zeitlos also runs on some boards from other manufacturers, so details vary. The common parts are:

- an **FPGA**, usually a Lattice ECP5, which becomes the whole computer
- **external RAM**, from 1 MB of SRAM to tens of megabytes of SDRAM, with larger DDR3 memory on boards still being brought up
- **configuration flash**, often on a removable MMOD module, holding the FPGA's design and the core of the operating system
- **USB host ports** for a keyboard, a mouse, storage sticks and network adapters
- **video output**: DVI through an HDMI connector, VGA, or composite for a television
- a **microSD** slot
- **Pmod** sockets for expansion
- power from a USB supply, a few watts

## The System on the Chip

Each part of the Zeitlos SOC was described in an earlier chapter:

| In this book         | In the Zeitlos SOC                                 |
|----------------------|----------------------------------------------------|
| The Computer         | RISC-V CPU (RV32IM), 48 MHz, PicoRV32 core         |
| The Computer         | Wishbone bus, address map, caches                  |
| Operating Systems    | address translation per program, memory protection |
| Talking to the World | framebuffer, blitter and line drawing              |
| Talking to the World | 8-channel audio mixer, USB host, serial ports      |
| Talking to the World | pins on the Pmod sockets, I2C and SPI              |
| Communication        | Ethernet, random number generator                  |
| Systems on a Chip    | multiplier and hash accelerators for cryptography  |

**One address space, translated per program.** There is no full memory management unit. Each program is loaded somewhere in main memory, but always sees itself at the same address, `0x8000_0000`; the hardware adds an offset when it switches programs. Programs therefore need no adjustment for where they are loaded, and the kernel can pass data between programs by passing addresses.

**Protection for containment, not secrecy.** A memory protection unit prevents a program from writing outside its own memory or to devices it is not permitted to use. A faulty program is stopped with a report, and everything else continues. Zeitlos is a single-user system, and this protection exists to contain errors, not to defend against a hostile program the owner chose to run.

There is also a **game mode**, in which a 320 by 240 region of the screen is doubled in size to fill the display and, on boards built with colour, can use up to sixteen colours. It is used by games and by the BASIC computer described below.

## Starting Up

The start-up sequence closely follows [Operating Systems](#operating-systems):

1. The FPGA loads the Zeitlos design from its configuration flash and becomes the computer. Some boards first run a small bootloader that waits a few seconds for an update over USB.
2. A boot program, built into the design in block RAM, copies the kernel from flash into main memory and starts it.
3. The kernel starts the filesystem driver, then the USB driver, reads the configuration file, and starts the window manager, the network driver and any other services the configuration specifies.
4. The desktop appears.

A program is looked for first in the `/apps` folder of the SD card, then in flash; only the kernel and the filesystem driver always come from flash. As a result, a newer version of a program can be tried by copying it onto the card, and the original is restored as soon as the copy is deleted.

## The Operating System

Zeitlos is a **microkernel**, as described in [Operating Systems](#operating-systems). The kernel schedules programs, manages memory, passes messages, routes interrupts and enforces protection. The filesystem, USB and network are driver programs that run like any other. If one crashes, the kernel restarts it a moment later, and most programs using it recover, although open files may need to be opened again.

Scheduling is preemptive, driven by a timer several hundred times a second. When a program sends a message and waits for the answer, the processor switches directly to the program that will answer it. As a result, the desktop responds immediately on a 48 MHz processor: work passes directly to where it is needed, and programs waiting for an event use no time.

Programs communicate through messages and through **ports**: named services that other programs can connect to. A terminal window can connect in the same way to the Scheme interpreter, to a shell modelled on Unix (following POSIX, the standard that describes Unix-like systems), to the BASIC computer, to a serial line, or to another machine across the network.

Files are arranged in one tree:

| Path  | Contents                                  |
|-------|-------------------------------------------|
| /     | the SD card, with the flash underneath    |
| /apps | programs                                  |
| /data | each program's own files, one folder each |
| /docs | documentation, including this book        |
| /sys  | the system configuration                  |
| /ram  | a RAM disk, fast and lost at power-off    |
| /usb  | a USB stick, when one is plugged in       |
| /home | the owner's files                         |

Settings are kept in a plain text configuration file, which can be read and edited like any other. A few settings that belong to the machine rather than to a card, such as the password, are kept in a small, power-safe area of flash.

## The Languages

All three languages from the programming chapters are on the machine.

**Scheme** is always available, from flash, through a terminal window. Besides standard Scheme, it has procedures for files, windows and drawing, starting and stopping programs, simple network transfers, and the pins and buses on the expansion sockets, each with built-in help. It is the quickest way to automate a task or to explore the system.

**BASIC** runs as a separate small computer, in the tradition of the 1980s. It has a 320 by 240 screen, shown in a window or full screen, graphics statements and its own files in one folder, but no access to the rest of the system, which makes it a safe environment for learning. Programs for Machdyne's modules can be written and tried here, or on a virtual module that imitates the limits of a real one exactly, before being sent to a real module.

**C** programs are usually compiled on another computer with the standard open tools, as Zeitlos itself is. An experimental compiler that runs on the machine itself is being brought up. On machines with enough memory, the Unix-style shell provides familiar commands, pipes and the vi editor.

## Adapting the Machine

The machine can be adapted at several levels, each deeper than the one before.

**1. Settings.** Screen mode and colour, keyboard layout, time zone, the services that start, and many other settings are lines in the configuration file. Most can be changed with the settings program.

**2. Scripts and schedules.** A few lines of Scheme can rename files, process text, fetch data from the network or open a small window with buttons. A built-in scheduler runs programs at given times or intervals, or at start-up.

**3. Programs.** A program written in C, compiled and placed in `/apps` becomes an application like the others, with its own window if it needs one.

**4. Hardware.** The Pmod sockets give direct access to pins from Scheme and C, with I2C and SPI built on top. Sensors, displays and relays connect here, as do Sechs modules: a command in the Unix-style shell can find modules on the bus, read their registers and send them BASIC programs. A virtual workbench can simulate parts such as pin expanders, LEDs and buttons on screen, so that a program's logic can be tested before anything is wired.

**5. The gateware.** The SOC itself is open Verilog. With the open FPGA tools on another computer, it can be modified, extended with a peripheral as described in [Systems on a Chip](#systems-on-a-chip), and rebuilt. For small designs, an experimental set of tools on the machine can synthesize, place and route a design and generate its bitstream, without any other computer.

**6. The system.** The source of every program and of the kernel is available. Any program can be rebuilt and tried by placing the new version in the card's `/apps` folder while the original remains in flash. The kernel, the filesystem driver and the gateware are changed by rewriting the flash, which is best done on a spare MMOD.

## Getting Back to Safety

The machine is designed so that a failed experiment can always be undone:

- **The core system is in flash**, and the machine starts without a card. A card with a faulty program on it can be removed.
- **Card copies override flash copies** for programs. Deleting the copy in `/apps` restores the original.
- **A rescue console** appears if the desktop cannot start, and can be called up by holding Escape during start-up. From it, programs can be started by hand and problems investigated.
- **Crashes are contained.** A faulty program is stopped and reported; a faulty driver is restarted, up to a few times a minute.
- **Trial gateware is not kept.** A design sent from another computer for a trial lasts only until the power is turned off. The region of flash holding the bootloader is protected from any action Zeitlos can take.
- **A second MMOD** is the safest place to try a new design. It can be fitted for an experiment and the original refitted afterwards. The machine can also copy its own configuration module to a spare as a backup.
- **Release images** restore the whole machine to its original state, and are written to the flash with the open tools from another computer.

With a spare MMOD holding a known good system, and a copy of the release image, almost any change to the machine can be undone in a few minutes.

## Where to Go Next

The system's own documentation is in the `/docs` folder and can be read in the document reader. It begins with an index and a welcome page that covers the desktop and every keyboard shortcut, and has a page for most programs, each language and each part of the hardware. In the Scheme interpreter, `help` followed by a name explains any procedure.

Zeitlos is under active development. Some features described in its documentation are marked experimental, and some boards are better supported than others. Its documentation states which, and is always more current than a book.
