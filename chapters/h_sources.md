# Sources

This book does not assume access to a network. For readers who have one, this appendix lists where to find the projects it describes, their source code and documentation, and further reading. Web addresses change over time; if one no longer works, search for the project's name.

## Machdyne

| What                        | Where                       |
|-----------------------------|-----------------------------|
| Machdyne                    | https://machdyne.com        |
| Zeitlos                     | https://zeitlos.org         |
| Community bulletin board    | telnet bbs.machdyne.com     |
| Source code of all projects | https://github.com/machdyne |

The source of each project mentioned in this book, under https://github.com/machdyne:

| Repository | Contents                                                   |
|------------|------------------------------------------------------------|
| tc         | this book, with the tests for its examples                 |
| zeitlos    | the Zeitlos SOC and operating system                       |
| basic      | Machdyne BASIC, its language reference and module firmware |
| ms         | Machdyne Scheme                                            |
| sechs      | the Sechs module interface standard                        |
| zwolf      | the Zwölf module platform, predecessor of Sechs           |
| mmod       | the MMOD memory module standard                            |
| kakao      | Kakao Linux for Machdyne computers                         |
| ark        | an offline information collection                          |
| blaustahl  | the Blaustahl F-RAM storage device                         |
| kaltstahl  | the Kaltstahl F-RAM storage device                         |
| werkzeug   | the Werkzeug multi-tool                                    |
| zucker     | Zucker, the SOC that preceded Zeitlos                      |

## Open Hardware Tools

- **Yosys**, synthesis: https://github.com/YosysHQ/yosys
- **nextpnr**, place and route: https://github.com/YosysHQ/nextpnr
- **Project IceStorm**, Lattice iCE40: https://github.com/YosysHQ/icestorm
- **Project Trellis**, Lattice ECP5: https://github.com/YosysHQ/prjtrellis
- **Project X-Ray**, Xilinx 7-series: https://github.com/f4pga/prjxray
- **Project Peppercorn**, GateMate: https://github.com/YosysHQ/prjpeppercorn
- **Icarus Verilog**, simulation: https://github.com/steveicarus/iverilog
- **PicoRV32**, a RISC-V softcore: https://github.com/YosysHQ/picorv32
- **LiteX**, SOC builder: https://github.com/enjoy-digital/litex

## Standards

- The RISC-V instruction set specifications are published by RISC-V International at https://riscv.org.
- The Revised(4) Report on the Algorithmic Language Scheme (R4RS), 1991, defines the Scheme dialect used in this book. Later reports, such as R5RS and R7RS, are its successors.
- The C language is standardized by ISO; the examples in this book follow the 1999 standard, C99.
- Verilog is standardized as IEEE 1364; the examples follow Verilog-2005.

## Further Reading

These books cover the subjects of this book in more depth. All are widely available in libraries.

- Charles Petzold, *Code: The Hidden Language of Computer Hardware and Software*. How computers work, built up from switches, for any reader.
- Sarah L. Harris and David Harris, *Digital Design and Computer Architecture, RISC-V Edition*. Digital logic, Verilog and processor design, ending with a working RISC-V processor.
- Paul Horowitz and Winfield Hill, *The Art of Electronics*. The standard practical reference on electronics.
- Harold Abelson and Gerald Jay Sussman, with Julie Sussman, *Structure and Interpretation of Computer Programs*. Programming and the nature of programming languages, taught in Scheme.
- Brian Kernighan and Dennis Ritchie, *The C Programming Language*. A concise introduction to C, by Kernighan and C's creator, Ritchie.
- Andrew Tanenbaum and Albert Woodhull, *Operating Systems: Design and Implementation*. Operating systems explained through a complete small microkernel system.
- John Kemeny and Thomas Kurtz, *Back to BASIC*. The creators of BASIC on why they made it and what it was for.
