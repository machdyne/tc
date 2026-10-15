# A Short History

Computing builds on more than two thousand years of discovery. This appendix gives a brief account of how the ideas in this book came about, followed by a timeline of the main events.

## From Electricity to Electronics

For most of history, electricity was a curiosity: a spark from rubbed amber, a twitch in a frog's leg. It became useful in the nineteenth century, once Alessandro Volta's battery provided a steady current and Georg Ohm, Michael Faraday and James Clerk Maxwell explained how current, magnetism and voltage are related. The first great application was communication. From the 1840s the electric telegraph carried messages across continents, coded as short and long pulses, and the telephone followed in the 1870s. Both are early examples of information carried as electrical signals, the subject of [Information](#information).

The vacuum tube, invented in the first decade of the twentieth century, made electronics possible. A small voltage on one part of a tube controls a larger current through it, so a tube can amplify a signal or act as a switch with no moving parts. Tubes made radio and television practical, and in the 1940s they made the first electronic computers possible.

## Machines That Calculate

The idea of a general-purpose computing machine is older than electronics. In the 1830s Charles Babbage designed the Analytical Engine, a mechanical computer driven by instructions on punched cards, and Ada Lovelace described how it could be programmed. It was never built. In 1854 George Boole published an algebra of true and false, which in 1937 Claude Shannon showed could describe circuits built from switches: the basis of [Digital Logic](#digital-logic). In 1936 Alan Turing described an abstract machine that could carry out any computation that can be described precisely, and so defined what a computer is in principle.

The Second World War turned these ideas into machines. Konrad Zuse built programmable computers from telephone relays in Germany. In Britain, Colossus used vacuum tubes to help break enemy codes. In the United States, ENIAC, completed in 1945 with about 18,000 tubes, was programmed by rewiring panels of cables, which could take days.

## The Stored Program

The decisive step came in the mid-1940s with the idea of keeping the program in the computer's memory, alongside its data. It was set out in a 1945 report on the EDVAC computer, written by John von Neumann from work with J. Presper Eckert and John Mauchly, and first run in practice by the Manchester Baby in 1948. A stored-program computer can be given a new task by loading new numbers into its memory, and can even create programs itself. Nearly every computer since has been built this way, and [The Computer](#the-computer) describes how.

Programming languages followed. Early programs were written in machine code or assembly language. In the late 1950s, languages such as FORTRAN and Lisp let programs be written in a form closer to mathematics, and translated into machine code by the computer itself. BASIC, created in 1964, was designed so that students in any subject could use a computer.

## Smaller and Cheaper

The transistor, demonstrated in 1947, did the work of a vacuum tube while being smaller, more reliable and far more economical with power. From 1958 the integrated circuit placed many transistors on one piece of silicon, and the number that fitted on a chip doubled roughly every two years for half a century, a trend known as Moore's law. In 1971 a complete processor fitted on a single chip, the microprocessor.

Inexpensive microprocessors made the personal computer possible. Kits appeared in the mid-1970s, and by the early 1980s millions of homes and schools had small computers that started directly into BASIC. Their owners could see a program's effect the moment it was typed, and many learned to program by entering listings printed in magazines. These machines were slow by later standards, but they responded instantly, because there was little software between the keyboard and the screen. Graphical interfaces, with windows and a pointer, had been developed in research laboratories in the 1970s and reached ordinary users in the 1980s.

At the same time, Unix, developed at Bell Labs from 1969, and the C language in which it was rewritten from 1973, showed that an operating system could be small, written in a high-level language, and moved from one kind of computer to another. Many of the ideas in [Operating Systems](#operating-systems) come from it.

## Networks

Computers were first connected to each other in the late 1960s, when the ARPANET linked research institutions in the United States. Its packet-switching design, and from 1983 the TCP/IP protocols, became the basis of the Internet described in [Communication](#communication). Outside the research world, people connected home computers over the telephone network to bulletin board systems from 1978 onwards. The World Wide Web, created at CERN between 1989 and 1991, made the Internet accessible to the general public.

## Growth and Complexity

Each new generation of hardware was faster and had more memory, and software grew to use it. Operating systems, applications and web pages became many times larger and more capable, and also harder to understand, to secure and to keep running on older hardware. In 1995 the computer scientist Niklaus Wirth drew attention to the observation that software was becoming slower more rapidly than hardware was becoming faster. The problems described at the start of [Timeless Computing](#timeless-computing) are the long-term result.

## Open Designs

Two developments made the alternative described in this book possible. The first was free and open-source software. From the 1980s, projects such as GNU and, from 1991, Linux showed that a complete system could be developed in public and shared with anyone.

The second was open hardware. FPGAs were introduced in 1985, but for thirty years they could be configured only with their manufacturers' closed tools. In 2010 work began at the University of California, Berkeley on RISC-V, an instruction set that anyone may implement without a licence. In 2015 Project IceStorm documented the configuration format of a family of FPGAs and released the first complete open-source toolchain for it, and open tools for other families followed. For the first time, every layer of a working computer, from its processor to its applications, could be designed, studied and changed with open tools. The chapters [Inside an FPGA](#inside-an-fpga) to [The Machine](#the-machine) describe what that makes possible.

## Timeline

### Discovering Electricity

- **About 600 BC.** Thales of Miletus is said to have noticed that rubbed amber attracts light objects. The Greek word for amber, *elektron*, gives electricity its name.
- **1600.** William Gilbert publishes a study of magnetism and static electricity, and coins the Latin word *electricus*.
- **1780s.** Luigi Galvani observes that electricity makes a frog's leg twitch.
- **1800.** Alessandro Volta builds the first battery, the voltaic pile, giving experimenters a steady current for the first time.
- **1820.** Hans Christian Oersted discovers that an electric current deflects a compass needle, linking electricity and magnetism.
- **1827.** Georg Ohm publishes the law relating voltage, current and resistance.
- **1831.** Michael Faraday discovers electromagnetic induction, the principle of the generator and the transformer.
- **1830s and 1840s.** The electric telegraph, including Samuel Morse's system and code, sends messages across countries at the speed of electricity.
- **1860s.** James Clerk Maxwell's equations unify electricity, magnetism and light.
- **1876.** Alexander Graham Bell patents the telephone.
- **1880s.** Electric power networks are built. Alternating current, developed by Nikola Tesla and others, wins out for long-distance transmission.
- **1897.** J. J. Thomson identifies the electron.

### Electronics

- **1904.** John Ambrose Fleming invents the vacuum tube diode.
- **1906.** Lee de Forest adds a control grid, making the triode, which can amplify and switch signals.
- **1947.** John Bardeen and Walter Brattain, in William Shockley's group at Bell Labs, build the first transistor.
- **1958 and 1959.** Jack Kilby at Texas Instruments and Robert Noyce at Fairchild Semiconductor independently invent the integrated circuit.
- **1963.** CMOS logic is invented at Fairchild.
- **1965.** Gordon Moore observes that the number of transistors on a chip is doubling at a steady rate, a trend that held for decades.
- **1985.** Xilinx sells the first commercial FPGA.

### Computers

- **1837.** Charles Babbage designs the Analytical Engine, a mechanical general-purpose computer that was never completed.
- **1843.** Ada Lovelace publishes notes on the Analytical Engine, including a method for computing Bernoulli numbers on it, often called the first computer program.
- **1854.** George Boole publishes the algebra of logic.
- **1936.** Alan Turing describes a theoretical machine that can carry out any computation, laying the foundation of computer science.
- **1937.** Claude Shannon shows that Boole's algebra can describe and design switching circuits.
- **1941.** Konrad Zuse completes the Z3, an electromechanical programmable computer.
- **1944.** Colossus, designed by Tommy Flowers, breaks codes at Bletchley Park, the first programmable electronic digital computer.
- **1945.** ENIAC, built by John Mauchly and J. Presper Eckert, is completed. It is reprogrammed by rewiring.
- **1948.** The Manchester Baby runs the first program stored in electronic memory.
- **1958.** John McCarthy creates Lisp.
- **1964.** John Kemeny and Thomas Kurtz create BASIC at Dartmouth College.
- **1969.** The ARPANET, ancestor of the Internet, links its first computers. Work on Unix begins at Bell Labs.
- **1971.** Intel's 4004 puts a whole processor on one chip.
- **1972.** Dennis Ritchie creates C.
- **1975.** Guy Steele and Gerald Sussman create Scheme. The Altair 8800 kit starts the personal computer era.
- **1977 to 1985.** Home and personal computers spread: the Apple II, the TRS-80, the Commodore 64, the BBC Micro and the ZX Spectrum, all of which started up into BASIC, followed by the IBM PC, the Macintosh and the Amiga.
- **1978.** The first public bulletin board system goes online.
- **1983.** The ARPANET switches to TCP/IP.
- **1984.** Verilog is created.
- **1989 to 1991.** Tim Berners-Lee creates the World Wide Web.
- **1991.** Linus Torvalds releases Linux.

### Open Hardware

- **2010.** Work on RISC-V begins at the University of California, Berkeley. Its specification is published openly and anyone may implement it.
- **2015.** Project IceStorm documents the configuration format of the Lattice iCE40 and releases the first complete open-source FPGA toolchain. Open tools for other FPGA families follow.
