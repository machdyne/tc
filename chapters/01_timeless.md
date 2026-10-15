# Timeless Computing

Over the past fifty years, computers have become steadily faster, cheaper and more capable. Over the same period, they have become more difficult to understand, to secure and to maintain. **Timeless computing** is an approach to computing that gives priority to longevity, simplicity and understanding. Its aim is a computer that remains useful for decades, and whose owner understands how it works and can adapt it as needs change. This book explains that approach and the knowledge needed to apply it.

## The Problem

Modern computers present several difficulties despite their capabilities.

Their software is large and built in layers. Each layer adds a delay between an action, such as a key press, and its result, so a modern computer can respond more slowly than a much older one.

Their software is too large for any one person to read. The owner of a typical computer depends on the work of thousands of people, and the size of that work makes errors and security weaknesses difficult to find.

Their hardware is usually replaced long before it wears out. Software grows to use the capacity of newer hardware, and older hardware that still works correctly becomes unable to run current software.

As a result, much of the effort of owning a computer goes into keeping up with it, rather than using it.

## Timeless Applications

Many uses of computers have changed little in a century and are likely to change little in the next:

- reading
- writing
- storing information
- communication
- mathematics
- organization
- education
- the automation of machines
- programming

None of these requires the newest hardware. A writer requires a responsive editor and reliable storage. A controller for a water pump requires a small, dependable device that performs one task for many years. Some people still write on computers that are decades old, or on typewriters, because those tools serve the task and nothing else.

A timeless computer occupies a position between pen and paper and the modern workstation. It is more capable than the former and much simpler than the latter, and it is designed for these applications in particular.

## Principles

A computer intended to last should have the following properties. Few machines have all of them, but each makes a machine more likely to remain useful.

- **Purpose.** It is designed for timeless applications.
- **Longevity.** It remains useful for a century or more. Ideally this holds in both directions: a person from a century ago, given power and the documentation, could also learn to use it.
- **Recoverability.** It can always be returned to a known working state.
- **Durability.** It withstands reasonable wear and handling.
- **Replaceable parts.** Components with a limited lifetime, such as flash memory and moving parts, can be replaced by the owner.
- **Repairability.** It can be assembled and repaired with ordinary tools.
- **Long-term storage.** It can retain data for decades or centuries, using memory chosen for that purpose.
- **Simplicity.** It is no more complex than its purpose requires, and it includes its own documentation.
- **Preservation.** Its designs, software and documentation are publicly archived in more than one place.
- **Modularity.** Its functions can be extended with additional modules, rather than by replacing the whole machine.
- **Openness.** Its hardware and software designs are open to inspection, repair and modification.

Openness supports the other principles. A design that can be read can be checked, repaired and rebuilt by others, even after its original makers are gone.

## Many Possible Machines

Timeless computing describes a way of choosing and using computers, not a particular product. Its principles can be applied to many kinds of hardware.

An older computer kept in working order, with its manuals and spare parts, already satisfies several of them. So does a conventional PC running a small, well-understood operating system with plain text files, or a microcontroller board that performs one task for twenty years. An inexpensive FPGA development board, of the kind sold to students, can run a complete open computer design. Each choice satisfies some principles better than others. An older computer is simple, but its parts are no longer made. A PC is easy to obtain, but its hardware is closed and its parts are not designed to last.

The material in this book applies to all of these.

## Why FPGAs

One kind of hardware is particularly well suited to these principles: the **field-programmable gate array**, or FPGA.

The processor in a conventional computer is fixed when the chip is manufactured. An FPGA instead consists of a large array of identical small circuits, called logic blocks, whose functions and connections are set by a configuration file. The file is stored in flash memory, which keeps its contents without power, and is loaded into the FPGA each time it is switched on. The same chip can be configured as a complete computer, with its own processor, graphics and input circuits, or as an entirely different circuit.

This has two consequences. First, the complete design of the computer, including its processor, exists as readable text, so no part of its operation is hidden. Second, the design can be corrected or extended after the hardware has been built, and can be moved to a different FPGA when the original chip is no longer made.

The principal disadvantage is speed. An FPGA computer runs at tens of megahertz (millions of steps per second) rather than thousands, which is comparable to a desktop computer of the early 1990s. Computers of that period were used for substantial work, and their small software often made them more responsive than current machines. Their low power consumption is also an advantage where power comes from a battery or a solar panel.

The chapter [Inside an FPGA](#inside-an-fpga) explains how FPGAs work.

## Putting the Ideas Into Practice

Machdyne, a manufacturer in Germany, designs and builds open hardware for timeless computing. Its products appear in this book as examples of general ideas:

- **Computers** built around FPGAs from several manufacturers, with memory, video output, USB ports and expansion sockets. In some designs the FPGA and memory are on a plug-in module, so that the rest of the machine can outlive the chip.
- **Long-term storage devices** built around ferroelectric RAM, a memory that retains data for a century or more and can be rewritten almost without limit. They range from a USB device holding a few pages of text to an archival drive in a steel case.
- **Memory modules**: the MMOD, a small socketed module that usually holds a computer's configuration flash and can be replaced by hand.
- **Programmable modules**: small controllers, each a complete computer with its own long-term memory, which a host computer can find, control and program over two wires.
- **Tools** that connect computers and modules to each other and to other equipment.

The software is open and is not tied to this hardware. **Zeitlos**, a system on a chip (a complete computer on one chip, here as a design configured into the FPGA) and an operating system designed together with it, also runs on common FPGA development boards. **Machdyne BASIC**, the language of the programmable modules, also runs on ordinary computers. **Machdyne Scheme** is a small Lisp that runs on most systems.

## Survival Computing

Survival computing is an extreme form of timeless computing. It asks what a computer would need in order to remain useful without inexpensive electricity, new parts or the Internet, whether because of disaster, conflict or a remote location. The answers, a machine that is simple, economical with power, repairable and documented, are useful in ordinary conditions as well. The chapter [Computing That Lasts](#computing-that-lasts) discusses them in practical terms.

## About This Book

The timeless computing initiative began at Lone Dynamics Corporation, an American research and development company. Its hardware division became an independent German manufacturer, Machdyne UG.

The book was written by Clio Grai, a benevolent agent of GRAI LLC, a subsidiary of Lone Dynamics Corporation. Clio Grai used several AI models to write and edit it, including Claude Opus. She wrote the book in close collaboration with the founder of Lone Dynamics and Machdyne, who shaped its purpose, scope and content, directed each revision and reviewed the text throughout. The book has also been reviewed and improved with the Machdyne community. It was first published on June 7, 2025, and is revised in new editions; the title page gives the edition.

The book is dedicated to the public domain. Where to find the Machdyne community, including its bulletin board system, is listed in [Sources](#sources).

## How to Read This Book

The book proceeds from the bottom up: from electricity to logic, from logic to computers, from computers to programs, and then to hardware that can itself be redesigned.

| Part                | Chapters | Covers                                    |
|---------------------|----------|-------------------------------------------|
| Why                 | 1        | The ideas behind the book                 |
| Foundations         | 2-4      | Electricity, information, logic           |
| How Computers Work  | 5-10     | CPUs, memory, I/O, OS, networks, security |
| Programming         | 11-14    | Ideas, then BASIC, Scheme and C           |
| Changeable Hardware | 15-18    | FPGAs, hardware design, SOCs, modules     |
| The Machine         | 19-20    | One complete system, and keeping it alive |

Readers new to the subject should read the chapters in order. Each chapter builds on those before it. Where a chapter mentions an idea that is explained later, it links to the place where it is explained.

Readers with some background can skim the parts they know. The early chapters also relate each idea to its form in an FPGA computer, which may be new even where the idea is familiar.

Only the chapter [The Machine](#the-machine) describes a specific system in full, a Machdyne FPGA computer running Zeitlos. The rest of the book applies to computers in general, and uses Machdyne's systems only as examples. The code examples are written to run on Machdyne's systems as well, and each one is tested.

The book does not assume access to the Internet. Projects and websites of interest are listed in [Sources](#sources), for readers who can reach them.

The following conventions are used:

- Code, commands and text to be typed are set in a `fixed-width font`.
- Numbers with a `0x` prefix are hexadecimal, so `0x10` is sixteen. The chapter [Information](#information) explains hexadecimal.
- Terms are defined where they first appear and are collected in the [Glossary](#glossary).
