# Connector Pinouts

This appendix lists the pins of connectors in common use with small computers. Pin 1 is usually marked on a board by a square pad, a dot, an arrow or a small number. Signal names ending in N are active when low; a plus or minus sign marks one half of a differential pair. Before a connection is made from these tables, the voltages are checked as described in [Connecting a Device](#connecting-a-device).

## Pmod

A Pmod connector has one row of six pins, or two rows of six. Pins 5 and 6 are ground and the supply, usually 3.3 V; on a 12-pin connector, so are pins 11 and 12. Pins 7 to 10 repeat the arrangement of pins 1 to 4.

```text
  6-pin:   1   2   3   4  GND VCC
 12-pin:   1   2   3   4  GND VCC
           7   8   9  10  GND VCC
```

The Pmod specification defines standard uses of pins 1 to 4, so that a module and a host can agree without further documentation:

| Type      | Pin 1 | Pin 2    | Pin 3    | Pin 4 |
|-----------|-------|----------|----------|-------|
| 1, GPIO   | GPIO  | GPIO     | GPIO     | GPIO  |
| 2, SPI    | CS    | MOSI     | MISO     | SCK   |
| 3, UART   | CTS   | TXD      | RXD      | RTS   |
| 5, motors | DIR1  | EN1      | DIR2     | EN2   |
| 6, I2C    | INT   | RESET    | SCL      | SDA   |
| 7, I2S    | LRCLK | DAC data | ADC data | BCLK  |

Many modules do not follow the standard types exactly, so the module's own documentation decides.

## Sechs

The six contacts of a Sechs module, described in [Small Computers](#small-computers), match one row of a 6-pin Pmod connector:

| Pin | Name | Use                                          |
|-----|------|----------------------------------------------|
| 1   | A    | shared I2C bus clock (the module is a slave) |
| 2   | B    | shared I2C bus data                          |
| 3   | C    | the module's own I/O; as a UART, the module  |
|     |      | receives on C                                |
| 4   | D    | the module's own I/O; as a UART, the module  |
|     |      | transmits on D                               |
| 5   | GND  | ground                                       |
| 6   | 3V3  | 3.3 V, supplied by the carrier               |

The carrier provides the pull-up resistors for A and B, of 2.2k to 10k; modules never do. Anything the carrier drives onto C or D passes through a series resistor of about 1k.

## Zwölf

Zwölf modules, which comply with Sechs when they run Sechs firmware such as Machdyne BASIC, have twelve contacts in two rows: the six of Sechs, four more for the module's own uses, a reset and a write protect. Viewed from the top:

```text
   1   2   3   4   5   6
   7   8   9  10  11  12
```

| Pin | Name   | Use                                           |
|-----|--------|-----------------------------------------------|
| 1   | A      | shared I2C bus clock (slave)                  |
| 2   | B      | shared I2C bus data                           |
| 3   | C      | local I2C clock (master), or I/O              |
| 4   | D      | local I2C data, or I/O                        |
| 5   | GND    | ground                                        |
| 6   | 3V3    | 3.3 V                                         |
| 7   | E      | module-specific                               |
| 8   | F      | module-specific                               |
| 9   | G      | module-specific                               |
| 10  | H      | module-specific, often an interrupt or the    |
|     |        | programming pin                               |
| 11  | RESETN | reset; left open or pulled low                |
| 12  | WPN    | write protect; left open or pulled low, never |
|     |        | driven high                                   |

## Werkzeug

Werkzeug, Machdyne's USB multi-tool, is built around an RP2040 microcontroller. Its 20-pin I/O header, numbered as in its documentation:

```text
   1   2   3   4   5   6   7   8   9  10
  11  12  13  14  15  16  17  18  19  20
```

| Pin | Signal | Pin | Signal       |
|-----|--------|-----|--------------|
| 1   | GPIO0  | 11  | GPIO8        |
| 2   | GPIO1  | 12  | GPIO9        |
| 3   | GPIO2  | 13  | GPIO10       |
| 4   | GPIO3  | 14  | GPIO11       |
| 5   | GPIO4  | 15  | GPIO26, ADC0 |
| 6   | GPIO5  | 16  | GPIO27, ADC1 |
| 7   | GPIO6  | 17  | GPIO28, ADC2 |
| 8   | GPIO7  | 18  | GPIO29, ADC3 |
| 9   | GND    | 19  | GND          |
| 10  | 3V3    | 20  | 3V3          |

Its 12-pin Pmod connector carries GPIO19, 17, 15 and 13 on pins 1 to 4, and GPIO18, 16, 14 and 12 on pins 7 to 10. Its two LEDs, green on GPIO20 and red on GPIO21, light when their pins are low.

## Raspberry Pi GPIO

The 40-pin header of the Raspberry Pi, used on most of its models since 2014. Pin 1 has a square pad, and the odd-numbered pins form the row nearer the centre of the board. Signals are at 3.3 V, and the pins are not 5 V tolerant.

| Pin | Signal           | Pin | Signal          |
|-----|------------------|-----|-----------------|
| 1   | 3.3 V            | 2   | 5 V             |
| 3   | GPIO2, I2C SDA   | 4   | 5 V             |
| 5   | GPIO3, I2C SCL   | 6   | GND             |
| 7   | GPIO4            | 8   | GPIO14, UART TX |
| 9   | GND              | 10  | GPIO15, UART RX |
| 11  | GPIO17           | 12  | GPIO18, PWM0    |
| 13  | GPIO27           | 14  | GND             |
| 15  | GPIO22           | 16  | GPIO23          |
| 17  | 3.3 V            | 18  | GPIO24          |
| 19  | GPIO10, SPI MOSI | 20  | GND             |
| 21  | GPIO9, SPI MISO  | 22  | GPIO25          |
| 23  | GPIO11, SPI SCK  | 24  | GPIO8, SPI CE0  |
| 25  | GND              | 26  | GPIO7, SPI CE1  |
| 27  | ID_SD            | 28  | ID_SC           |
| 29  | GPIO5            | 30  | GND             |
| 31  | GPIO6            | 32  | GPIO12, PWM0    |
| 33  | GPIO13, PWM1     | 34  | GND             |
| 35  | GPIO19           | 36  | GPIO16          |
| 37  | GPIO26           | 38  | GPIO20          |
| 39  | GND              | 40  | GPIO21          |

Pins 27 and 28 are reserved for the memory chip that identifies an add-on board.

## Serial Connectors

A **TTL serial** cable or adapter, of the kind used for a serial console, usually has a six-pin connector in this order, with signals at 3.3 V or 5 V:

| Pin | Signal | Wire colour, where used |
|-----|--------|-------------------------|
| 1   | GND    | black                   |
| 2   | CTS    | brown                   |
| 3   | VCC    | red                     |
| 4   | TXD    | orange                  |
| 5   | RXD    | yellow                  |
| 6   | RTS    | green                   |

TXD is the adapter's output and connects to the computer's receive pin; RXD connects to its transmit pin.

An **RS-232** serial port on a 9-pin D connector, as on older computers, swings to plus and minus 12 V and must not be connected directly to a 3.3 V pin:

| Pin | Signal              | Pin | Signal               |
|-----|---------------------|-----|----------------------|
| 1   | DCD, carrier detect | 6   | DSR, set ready       |
| 2   | RXD, receive        | 7   | RTS, request to send |
| 3   | TXD, transmit       | 8   | CTS, clear to send   |
| 4   | DTR, terminal ready | 9   | RI, ring indicator   |
| 5   | GND                 |     |                      |

These are the pins of a computer's port. A cable between two computers, a **null modem** cable, crosses pins 2 and 3.

## USB Connectors

| Pin | USB-A, USB-B | Micro-B | Wire colour |
|-----|--------------|---------|-------------|
| 1   | VBUS, 5 V    | VBUS    | red         |
| 2   | D-           | D-      | white       |
| 3   | D+           | D+      | green       |
| 4   | GND          | ID      |             |
| 5   |              | GND     | black       |

D+ and D- are a differential pair carrying data at USB 2.0 speeds. The ID pin of a micro-B plug is grounded in an adapter cable that makes the device act as a host.

A **USB-C** connector has 24 pins, in two rows that mirror each other, so that the plug fits either way up:

| Pins               | Signal   | Use                               |
|--------------------|----------|-----------------------------------|
| A1, A12, B1, B12   | GND      | ground                            |
| A4, A9, B4, B9     | VBUS     | power, 5 V unless more is agreed  |
| A6, B6             | D+       | USB 2.0 data                      |
| A7, B7             | D-       | USB 2.0 data                      |
| A5, B5             | CC1, CC2 | configuration: orientation, power |
| A8, B8             | SBU1, 2  | sideband use, for other modes     |
| A2, A3, B2, B3     | TX pairs | high-speed data, USB 3 and others |
| A10, A11, B10, B11 | RX pairs | high-speed data, USB 3 and others |

A device that is powered from USB-C must connect each of its CC pins to ground through a 5.1k resistor. Without them, a USB-C power supply does not turn on its 5 V output, and a simple board that works from a USB-A port receives no power from a USB-C charger.

## Ethernet Cables

An Ethernet cable has eight wires in four twisted pairs, ending in RJ45 plugs. Two standards give the order of the colours; a cable with the same standard at both ends is a straight cable, which is the usual kind.

| Pin | T568B        | T568A        | 10 and 100 Mbit/s |
|-----|--------------|--------------|-------------------|
| 1   | white/orange | white/green  | transmit +        |
| 2   | orange       | green        | transmit -        |
| 3   | white/green  | white/orange | receive +         |
| 4   | blue         | blue         | not used          |
| 5   | white/blue   | white/blue   | not used          |
| 6   | green        | orange       | receive -         |
| 7   | white/brown  | white/brown  | not used          |
| 8   | brown        | brown        | not used          |

The transmit and receive labels are those of a computer. Gigabit Ethernet uses all four pairs in both directions. Most current equipment detects a crossed cable and adapts to it.

## VGA Connector

A VGA connector is a 15-pin D connector in three rows. The colour signals are analog voltages from 0 to 0.7 V into 75 ohms; the sync signals are digital.

| Pin | Signal       | Pin | Signal           |
|-----|--------------|-----|------------------|
| 1   | red          | 9   | 5 V, for DDC     |
| 2   | green        | 10  | GND, sync return |
| 3   | blue         | 11  | reserved         |
| 4   | reserved     | 12  | DDC data (SDA)   |
| 5   | GND          | 13  | horizontal sync  |
| 6   | red return   | 14  | vertical sync    |
| 7   | green return | 15  | DDC clock (SCL)  |
| 8   | blue return  |     |                  |

**DDC** is an I2C bus on which the monitor reports its supported modes, from a small memory chip.

## HDMI Connector

A standard HDMI connector, type A, has 19 pins. DVI carries the same digital video signals on a larger connector.

| Pin | Signal             | Pin | Signal             |
|-----|--------------------|-----|--------------------|
| 1   | TMDS data 2+       | 11  | TMDS clock shield  |
| 2   | TMDS data 2 shield | 12  | TMDS clock-        |
| 3   | TMDS data 2-       | 13  | CEC                |
| 4   | TMDS data 1+       | 14  | reserved           |
| 5   | TMDS data 1 shield | 15  | DDC clock (SCL)    |
| 6   | TMDS data 1-       | 16  | DDC data (SDA)     |
| 7   | TMDS data 0+       | 17  | DDC and CEC ground |
| 8   | TMDS data 0 shield | 18  | 5 V                |
| 9   | TMDS data 0-       | 19  | hot plug detect    |
| 10  | TMDS clock+        |     |                    |

The four TMDS pairs carry the picture as fast serial streams, one pair for each colour and one for the clock. DDC works as on VGA. CEC lets devices control each other, and hot plug detect tells the source that a display is connected.

## SD Cards

A microSD card has eight contacts. It can be used in its own four-bit mode or as an SPI device, which needs fewer signals, as described in [Talking to the World](#talking-to-the-world):

| Pin | SD mode     | SPI mode       |
|-----|-------------|----------------|
| 1   | DAT2        | not used       |
| 2   | CD, DAT3    | CS             |
| 3   | CMD         | MOSI, data in  |
| 4   | VDD, 3.3 V  | VDD, 3.3 V     |
| 5   | CLK         | SCK            |
| 6   | VSS, ground | VSS, ground    |
| 7   | DAT0        | MISO, data out |
| 8   | DAT1        | not used       |
