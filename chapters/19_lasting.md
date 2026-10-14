# Computing That Lasts

Most people assume that electricity, spare parts, software updates and the Internet will always be available. Usually they are, but they are not guaranteed, and in some parts of the world they are already scarce. Natural disasters, conflicts, economic difficulties, changes in law and the decisions of distant companies can each remove something a computer depends on.

**Survival computing** considers how computing could continue under those conditions. It is best treated as a design exercise rather than a prediction. The properties that make a computer more likely to survive difficult times also make it cheaper, simpler and easier to own in ordinary times. This chapter collects the practical lessons of the whole book.

## Power Supply

Know how much power the equipment uses, and therefore how much energy it needs. Energy is power multiplied by time, measured in **watt-hours** (Wh). A computer drawing 3 W for eight hours a day needs 24 Wh a day.

This is a small amount. A common USB power bank stores 40 to 100 Wh, enough for one to four days of such use. A small solar panel can replace the energy used. A 20 W panel might deliver about 50 to 100 Wh on a sunny day, depending on season, latitude and weather, and much less on an overcast one. Allow a generous margin, and enough battery capacity for several cloudy days.

Several practices make the energy last longer:

- **The display often uses the most power.** A small monitor, or a television on composite video, may draw more than the computer.
- **Unused equipment can be switched off.** A module that sleeps between readings uses almost no energy.
- **A slower clock uses less power.** CMOS circuits use power mainly when they switch, as described in [Electricity](#electricity).
- **Conversion wastes energy.** Each step from one voltage to another loses some, so equipment that runs directly from 5 V USB power wastes less.

## The Environment

Electronic components age at a rate determined by their conditions.

**Heat** is the most important cause of ageing. It accelerates nearly every kind of wear: memory loses data sooner, as described in [Memory and Storage](#memory-and-storage), capacitors dry out, and batteries degrade. A rough rule for many components is that every additional ten degrees Celsius halves their life. Keep equipment and stored media cool.

**Moisture** corrodes contacts and boards. Store equipment dry, and allow equipment brought in from the cold to warm up before switching it on, so that condensation can evaporate.

**Dust** blocks ventilation and can conduct when damp. **Static electricity** destroys chips, as described in [Electricity](#electricity). An enclosure protects against all of these. A case made with a 3D printer can also be replaced or modified freely.

## Spares and Parts

A failed part cannot be replaced if no replacement can be found, so replacements should be planned in advance:

- Keep **spares of parts that wear out or are easily lost**: storage cards, configuration modules, cables, power supplies and small programmable modules.
- Prefer **standard connectors and voltages**, such as USB power, Pmod sockets and common batteries, which can be replaced with whatever is available.
- Prefer **socketed and modular parts**. A memory module that plugs in can be replaced by hand; one soldered to the board cannot.
- Keep **basic tools**: a multimeter, a soldering iron, small screwdrivers and a magnifier. With these and the schematics, most faults in a small computer can be found, and many repaired.
- Keep **the schematics and documentation** for every board in use, in a form that can be read without the board working.

## Data

The rules from [Memory and Storage](#memory-and-storage) can be restated as practices:

- Keep **at least three copies** of anything important, on more than one kind of medium, with one copy in another place.
- Use **plain formats**: text for writing, and simple, widely documented formats for everything else.
- Record a **hash** of each important file, and check copies against it periodically.
- **Refresh** copies onto new media before the old media reach the end of their expected life. Flash cards and USB sticks are for moving data, not for keeping it for decades.
- Keep **small, vital data**, such as keys, passwords and essential notes, on media built for longevity, such as F-RAM, and on paper.
- Keep **a list** of what is stored where, so that every copy can be found.

## Software and the Means to Rebuild It

Software does not wear out, but it can become unusable. The programs that build it stop running on new computers, the websites that hosted it disappear, and the knowledge of how it was put together is lost.

The protection against this is to keep three things together, offline, and in more than one place:

- **the source code** of every program and design in use
- **the tools** needed to build it, ideally as source code themselves, together with the versions known to work
- **written instructions** for building and restoring everything, tested by following them

The most independent arrangement is a machine that can **rebuild itself**: one that can edit and compile its own software, and design and build its own hardware configuration, with no other computer involved. Each step towards this removes a dependency on something that might later be unavailable. Some small systems, including Zeitlos, work towards this with compilers and FPGA tools small enough to run on the machine they build for.

**Recoverability** is equally important: a known good state that can be restored in minutes. Keep a spare copy of the configuration flash and of the system image, and practise restoring them before they are needed.

## Keeping Information

A computer without information has limited use. Collections of reference works, manuals, maps and books can be kept offline and read on small machines, especially in plain text. Such a collection should contain what would be needed if it could not be searched for: technical documentation for the equipment in use, references for the owner's work, and the knowledge the owner would want to pass on. It should be updated whenever possible.

## People

The most durable store of knowledge is people. A machine that only one person understands depends on that person. Knowledge should therefore be taught, written down and shared within a community of people who use and maintain the same kinds of systems. Open designs make this possible: anyone can study them, and no permission is needed to repair, copy or improve them.

This book is intended to contribute to that work, and anyone may copy, print, translate and correct it.

## A Checklist

- Know how much power the equipment needs, and have a way to supply it without the grid.
- Keep equipment cool, dry, clean and in an enclosure.
- Keep spares of the parts that wear out, and the tools and schematics to repair the rest.
- Keep three copies of important data, in plain formats, and check them.
- Keep the source, the tools and the instructions needed to rebuild the system, and test them.
- Keep a known good system image and a spare copy of the configuration flash.
- Keep an offline library of the information the work depends on.
- Learn how the machines work, and teach others.
