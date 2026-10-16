# Computing That Lasts

Most people assume that electricity, spare parts, software updates and the Internet will always be available. Usually they are, but they are not guaranteed, and in some parts of the world they are already scarce. Natural disasters, conflicts, economic difficulties, changes in law and the decisions of distant companies can each remove something a computer depends on.

**Survival computing**, introduced in [Timeless Computing](#timeless-computing), considers how computing could continue under those conditions. It is best treated as a design exercise rather than a prediction. The properties that make a computer more likely to survive difficult times also make it cheaper, simpler and easier to own in ordinary times. This chapter collects the practical lessons of the whole book.

## Power Supply

Planning a supply starts from how much power the equipment uses, and therefore how much energy it needs. Energy is power multiplied by time, measured in **watt-hours** (Wh). A computer drawing 3 W for eight hours a day needs 24 Wh a day.

This is a small amount. A common USB power bank, rated at 10,000 to 20,000 mAh at its cells' 3.7 V, stores about 37 to 74 Wh, of which perhaps two thirds can be delivered at 5 V after conversion losses: enough for one to two days of such use. A small solar panel can replace the energy used. A 20 W panel might deliver about 50 to 100 Wh on a sunny day, depending on season, latitude and weather, and much less on an overcast one. A practical system has a generous margin, and enough battery capacity for several cloudy days.

Several practices make the energy last longer:

- **The display often uses the most power.** A small monitor, or a television on composite video, may draw more than the computer.
- **Unused equipment can be switched off.** A module that sleeps between readings uses almost no energy.
- **A slower clock uses less power.** CMOS circuits use power mainly when they switch, as described in [Electricity](#electricity).
- **Conversion wastes energy.** Each step from one voltage to another loses some, so equipment that runs directly from 5 V USB power wastes less.

## The Environment

Electronic components age at a rate determined by their conditions.

**Heat** is the most important cause of ageing. It accelerates nearly every kind of wear: memory loses data sooner, as described in [Memory and Storage](#memory-and-storage), capacitors dry out, and batteries degrade. A rough rule for many components is that every additional ten degrees Celsius halves their life, so equipment and stored media last longest when kept cool.

**Moisture** corrodes contacts and boards. Equipment is best stored dry, and equipment brought in from the cold is allowed to warm up before it is switched on, so that condensation can evaporate.

**Dust** blocks ventilation and can conduct when damp. **Static electricity** destroys chips, as described in [Electricity](#electricity). An enclosure protects against all of these. A case made with a 3D printer can also be replaced or modified freely.

## Spares and Parts

Replacements are hardest to find when they are needed, so they are best obtained in advance:

- Keep **spares of parts that wear out or are easily lost**: storage cards, configuration modules, cables, power supplies and small programmable modules.
- Prefer **standard connectors and voltages**, such as USB power, Pmod sockets and common batteries, which can be replaced with whatever is available.
- Prefer **socketed and modular parts**. A memory module that plugs in can be replaced by hand; one soldered to the board cannot.
- Keep **basic tools**: a multimeter, a soldering iron, small screwdrivers and a magnifier. With these and the schematics, most faults in a small computer can be found, and many repaired.
- Keep **the schematics, data sheets and documentation** for every board in use, in a form that can be read without the board working. The schematic is the most important document for a repair, as described in [Reading a Schematic](#reading-a-schematic).

## Data

Data is kept intact over decades, on the media described in [Memory and Storage](#memory-and-storage), by a few practices:

- Keep **at least three copies** of anything important, on at least two kinds of medium, with one copy in another place.
- Use **plain formats**: text for writing, and simple, widely documented formats for everything else, which remain readable long after any particular program has gone.
- Record a **hash** of each important file, check copies against it periodically, and replace any that have failed.
- **Refresh** copies onto new media before the old media reach the end of their expected life. Flash cards and USB sticks are for moving data, not for keeping it for decades.
- Keep **small, vital data**, such as keys, passwords and essential notes, on media built for longevity, such as F-RAM, and on paper.
- Keep **a list** of what is stored where, so that every copy can be found.

A routine makes these practices reliable. Work in progress is copied daily or after each session, to a second medium; everything is copied weekly or monthly to a medium that is then disconnected and stored apart. A copy that is always connected, or a folder synchronized automatically with another machine, is not a backup in this sense: a file deleted, damaged or encrypted by faulty or hostile software in one place is changed in the other as well. A backup is tested by restoring files from it, at least occasionally, because an unreadable copy is found out only when it is needed.

## Software and the Means to Rebuild It

Software does not wear out, but it can become unusable. The programs that build it stop running on new computers, the websites that hosted it disappear, and the knowledge of how it was put together is lost.

The protection against this is to keep three things together, offline, and in more than one place:

- **the source code** of every program and design in use
- **the tools** needed to build it, ideally as source code themselves, together with the versions known to work
- **written instructions** for building and restoring everything, tested by following them

The most independent arrangement is a machine that can **rebuild itself**: one that can edit and compile its own software, and design and build its own hardware configuration, with no other computer involved. Each step towards this removes a dependency on something that might later be unavailable. Self-rebuilding is useful, but it is not a requirement of timeless computing, and few systems achieve it. Zeitlos does not: its experimental compiler and FPGA tools build simple programs and designs on the machine, but not the system itself. For such a system, the tools that build it, and a computer that runs them, are part of what must be kept.

**Recoverability** is equally important: a known good state that can be restored in minutes. That requires a spare copy of the configuration flash and of the system image, and a restore that has been practised before it is needed.

## Keeping Information

A computer without information has limited use. Collections of reference works, manuals, maps and books can be kept offline and read on small machines, especially in plain text. Such a collection should contain what would be needed if it could not be looked up elsewhere: technical documentation for the equipment in use, references for the owner's work, and the knowledge the owner would want to pass on. It should be updated whenever possible. Machdyne's Ark project prepares collections of this kind for offline computers, in sizes from a single compressed text file of about 2 MB to several gigabytes. Its smallest editions are condensed summaries of knowledge generated with AI, and the larger ones add selected texts. The 8 MB edition is sized to fit on F-RAM.

## Licences

Openness, one of the principles in [Timeless Computing](#timeless-computing), is given legal force by a **licence**: the terms under which the owner of a work's copyright allows others to use, copy, change and share it. Without a licence, a design or program that can be read may still not be legally copied or changed.

Open licences are of two broad kinds:

- **Permissive** licences, such as the MIT, BSD, Apache and Lone Dynamics Open licences, allow nearly any use, including in closed products, provided the original notice is kept. The Lone Dynamics Open License, used for most of Machdyne's designs and software, is similar to the one-clause BSD licence.
- **Copyleft** licences, such as the GNU General Public License (GPL), allow the same, on the condition that changed versions which are distributed are released under the same licence, with their source. The CERN Open Hardware Licence applies the same choice to hardware designs, in permissive and copyleft forms.

A work can also be **dedicated to the public domain**, with no conditions at all, as this book is under CC0, the Creative Commons public domain dedication. Patents and trademarks are separate from copyright: a patent can restrict building an invention whatever its licence, and a trademark protects a product's name rather than its design. For the owner of a timeless computer, the practical test is that the licences of its designs and software must allow it to be repaired, changed and rebuilt by anyone, without permission.

## People

The most durable store of knowledge is people. A machine that only one person understands depends on that person. Knowledge should therefore be taught, written down and shared within a community of people who use and maintain the same kinds of systems. Open designs make this possible: anyone can study them, and no permission is needed to repair, copy or improve them.

This book is intended to contribute to that work, and anyone may copy, print, translate and correct it.

## A Checklist

- Know how much power the equipment needs, and have a way to supply it without the grid.
- Keep equipment cool, dry, clean and in an enclosure.
- Keep spares of the parts that wear out, and the tools and schematics to repair the rest.
- Keep at least three copies of important data, in plain formats, and check them.
- Keep the source, the tools and the instructions needed to rebuild the system, and test them.
- Keep a known good system image and a spare copy of the configuration flash.
- Keep an offline library of the information the work depends on.
- Learn how the machines work, and teach others.

## Where to Begin

Timeless computing is not reached in a single step. Each step towards it is useful on its own, and none requires special equipment.

A reader new to the subject can begin with what is already at hand: write a short program in BASIC or Scheme, keep important writing in plain text files and make a verified copy of them, or study how one familiar device works inside. A reader with more experience can go further: build a small controller that does one job for years, read the source code of a system in daily use, add a peripheral to an FPGA design, or move a design to a different board.

The hardware, software and documentation described in this book are open, and so is the book itself. Each can be studied, corrected and improved by anyone who uses it, and each improvement that is shared helps it last. Corrections and suggestions for future editions are welcome through the Machdyne community and the book's source repository, listed in [Sources](#sources).

A computer lasts when the people who depend on it understand how it works. This book was written to help make that understanding possible.
