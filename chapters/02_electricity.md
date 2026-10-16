# Electricity

A computer is an electrical machine. Every number it stores and every decision it makes is a voltage on a wire. This chapter describes the electricity needed to understand the rest of the book, and to connect devices to a computer without damaging either.

## Charge and Current

All matter is made of atoms. An atom has a small, heavy centre, the nucleus, which carries positive electric charge, surrounded by much lighter electrons, which carry negative charge. Opposite charges attract and like charges repel.

In some materials, mostly metals, the outermost electrons are loosely held and can drift from atom to atom. These materials are **conductors**. In others, such as glass, plastic and dry air, the electrons are held tightly. These are **insulators**. A wire is a conductor wrapped in an insulator.

When electrons drift along a conductor in one direction, charge flows. That flow is **current**, measured in **amperes** (A), usually shortened to amps. One amp is a large current in electronics. An output pin of a chip can typically supply a few thousandths of an amp, written milliamps (mA).

For historical reasons, current is described as flowing from positive to negative, although the electrons move the other way. Circuit diagrams and this book use this "conventional current". The difference does not matter for any circuit in this book.

## Voltage

Charge flows only when something drives it. That driving force is **voltage**, measured in **volts** (V). A battery or power supply creates a voltage between its two terminals, and if a conductive path connects them, current flows through it.

Water in pipes is a useful analogy. Voltage corresponds to the pressure difference, current to the rate of flow, and a narrow pipe to a restriction of the flow. The analogy is imperfect but adequate for this book.

Voltage is always measured between two points. A wire is "at 3.3 volts" only relative to some other point. In a circuit, that reference point is called **ground** and is defined as 0 V. When this book gives a single voltage for a wire, it means the voltage between that wire and ground.

## Resistance and Ohm's Law

Every material resists current to some degree. **Resistance** is measured in **ohms**. A **resistor** is a component made to have a particular resistance.

Voltage, current and resistance are related by **Ohm's law**:

```text
V = I x R      voltage = current x resistance
I = V / R      current = voltage / resistance
R = V / I      resistance = voltage / current
```

These are three arrangements of the same rule. Doubling the voltage across a resistor doubles the current through it; doubling the resistance halves the current.

A common calculation is the resistor for a light-emitting diode (LED) connected to a computer's output pin, which produces 3.3 V when on. A red LED needs about 2 V across it to light, and is sufficiently bright at 5 mA. A resistor in series must take up the remaining voltage:

```text
voltage across resistor = 3.3 V - 2.0 V = 1.3 V
resistance = 1.3 V / 0.005 A = 260 ohms
```

Resistors are made in standard values, so the nearest value above is used, 270 ohms. Without the resistor, the LED would draw far more current than it or the pin can tolerate, and one of them would be damaged.

```text
   output pin  ---[ 270 ohms ]---|>|--- ground
     3.3 V                       LED
```

Large resistances are written with prefixes: 1,000 ohms is 1 kilohm (1k), and 1,000,000 ohms is 1 megohm (1M). The same prefixes apply to every unit: a millivolt is a thousandth of a volt, a microamp a millionth of an amp, and a nanosecond a thousand-millionth of a second.

## Power

**Power** is the rate at which energy is used, measured in **watts** (W):

```text
P = V x I      power = voltage x current
```

A circuit drawing 0.5 A from a 5 V supply uses 2.5 W. Almost all of that power ends up as heat. For this reason a resistor carrying too much current becomes hot, and a processor needs cooling.

Power matters for timeless computing because it determines what a computer can run from. A small FPGA computer typically uses a few watts, about what a USB phone charger can supply. A desktop computer can use a hundred times as much. A few watts can come from a modest battery or a small solar panel; several hundred watts requires a substantial installation.

## Capacitors and Time

A **capacitor** stores charge, in proportion to the voltage across it. Its size, the **capacitance**, is measured in **farads** (F); the capacitors on a circuit board range from a few picofarads (pF, millionths of a millionth) to a few thousand microfarads (uF); a nanofarad (nF) is a thousandth of a microfarad.

A capacitor charged through a resistor does not reach the supply voltage at once. The current through the resistor falls as the capacitor's voltage rises, so the voltage approaches the supply ever more slowly. The **time constant**, R x C, sets the pace: after one time constant the capacitor has reached about 63 percent of the supply voltage, and after five it is within 1 percent.

```text
time constant = R x C
10k x 100 nF = 10,000 ohms x 0.0000001 F = 0.001 s = 1 ms
```

The same calculation describes many circuits. A resistor and capacitor on a reset pin hold a chip in reset for a few milliseconds after power is applied, until the supply is steady. A resistor and capacitor can smooth the bounce of a switch. They can also turn a rapidly switched digital output into a steady voltage, as described in [Talking to the World](#talking-to-the-world). They also limit how fast a signal can change: a long wire has capacitance, and with a high-value pull-up resistor, described under [Floating Inputs and Pull-ups](#floating-inputs-and-pull-ups), it rounds the edges of a fast signal until they are too slow to be read correctly.

## Direct and Alternating Current

A battery produces **direct current** (DC): its voltage always has the same polarity. Mains electricity is **alternating current** (AC): its voltage reverses many times a second, which makes it easy to transform between voltages and to send over long distances.

Electronic circuits run on low-voltage DC. A power adapter converts mains AC to DC, typically 5 V for USB. Inside the computer, **regulators** convert that to the exact voltages each chip needs: 3.3 V for most input and output signals, and lower voltages, often around 1 V, for the core of an FPGA or processor. Lower voltages waste much less power, and the small transistors in a modern chip core cannot tolerate higher ones.

## Power Supplies and Batteries

A regulator is one of two kinds. A **linear regulator** drops the excess voltage across a transistor and turns it into heat: converting 5 V to 3.3 V at 0.3 A wastes (5 - 3.3) x 0.3 = 0.51 W, about a third of the 1.5 W drawn. It is simple, cheap and electrically quiet. A **switching regulator** switches its input on and off rapidly and smooths the result with an inductor and capacitors. It wastes only 5 to 15 percent, but is more complex and produces some electrical noise. Small boards often use both: a switching regulator for the main supply, and a linear one for a circuit that needs a clean supply.

A supply can provide only a limited current. A USB 2.0 port must be able to supply 0.5 A at 5 V, and a USB 3.0 port 0.9 A, to a device it has recognized; chargers often supply 2 A or more. A device that draws more than its supply can provide causes the voltage to sag. When the voltage falls below what a chip needs, it stops working correctly, which is a **brown-out**. Many chips detect this and hold themselves in reset until the voltage recovers. Unexplained crashes, especially when a motor starts or a card is written, are often caused by an inadequate supply or cable.

A battery's capacity is usually given in milliamp-hours (mAh) at its nominal voltage. Its energy in watt-hours is capacity multiplied by voltage: a 3,000 mAh cell at 3.7 V holds about 11 Wh.

| Type                   | Cell volts | Recharge | Notes             |
|------------------------|------------|----------|-------------------|
| alkaline               | 1.5        | no       | keeps for years   |
| nickel-metal hydride   | 1.2        | yes      | replaces AA, AAA  |
| lithium-ion            | 3.0-4.2    | yes      | needs a protector |
| lithium iron phosphate | 3.2        | yes      | long life         |
| lead-acid              | 2.0        | yes      | heavy; solar      |

A battery's voltage changes as it discharges, so a regulator is still needed between the battery and the circuit. Rechargeable cells must be charged by a charger designed for their chemistry. A lithium cell in particular must never be charged above its maximum voltage or discharged below its minimum, and is used with a small protection circuit, in the cell or in the battery pack, that prevents both.

## Components

A few types of component make up nearly every circuit board.

- **Resistors** limit current and set voltages.
- **Capacitors** store a small amount of charge. Placed next to a chip, they supply the brief bursts of current the chip needs when it switches, and reduce noise on the power supply. These are **decoupling** capacitors, and nearly every chip needs them.
- **Inductors** store energy in a magnetic field and resist changes in current. They appear mainly in power supplies.
- **Diodes** let current flow in one direction only. An LED is a diode that emits light when current flows.
- **Crystals** and **oscillators** vibrate at a precise frequency and provide the steady timing signal, the clock, that a computer runs on.
- **Transistors** are switches controlled by electricity. They are the subject of the next section.
- **Integrated circuits** (ICs, or chips) are complete circuits, sometimes containing billions of transistors, made on a single piece of silicon and sealed in a package with metal pins.

## The Transistor as a Switch

The kind of transistor used in digital chips is the metal-oxide-semiconductor field-effect transistor, or **MOSFET**. A voltage on one of its connections, the **gate**, controls whether current can flow between two others, the **source** and the **drain**. Used in this way, a transistor is a switch with no moving parts. It can turn on and off billions of times a second without wearing out. Another common kind, the **bipolar transistor**, is controlled instead by a small current into its **base**, and is often used on circuit boards to switch loads such as relays and motors.

MOSFETs come in two complementary forms. An n-type transistor conducts when its gate is high (near the supply voltage). A p-type transistor conducts when its gate is low (near ground). One of each, connected in series between the supply and ground with their gates joined, forms the simplest digital circuit, an **inverter**:

```text
                 3.3 V
                   |
     input --> [ p-type ]   conducts when the input is low
       |           |
       |           +------> output
       |           |
       +-----> [ n-type ]   conducts when the input is high
                   |
                 ground
```

When the input is low, the top transistor conducts and the bottom one does not, so the output is connected to the supply: high. When the input is high, the bottom transistor conducts and the output is connected to ground: low. The output is always the opposite of the input.

This arrangement is called **CMOS**, for complementary metal-oxide-semiconductor. In either state one transistor is off, so almost no current flows from the supply to ground. A CMOS circuit therefore uses power mainly when it switches. As a result, a slower clock means lower power, and an idle CMOS chip draws little current.

Every logic circuit in the following chapters, and every circuit inside an FPGA, is built from arrangements of transistors like these.

## Logic Levels

Digital circuits use voltages to represent two values, **high** and **low**, which stand for 1 and 0. For 3.3 V logic, an input reads low when it is below about 0.8 V and high when it is above about 2 V. Between those levels the result is not defined, and a well-designed circuit spends almost no time there.

This gap is the main advantage of digital electronics. A signal can pick up a moderate amount of noise, or lose some voltage along a wire, and still be read correctly. A stored number does not gradually drift, as a recording on tape does. Each stage of a circuit restores the signal to a clean high or low before passing it on.

Different families of chips use different levels. Older logic and many hobby boards use 5 V; FPGA pins usually use 3.3 V or less. **Never connect a 5 V output to a 3.3 V input** unless the input is documented as tolerant. The excess voltage can destroy the input, and sometimes the whole chip. A resistor divider or a level-shifter chip converts between the two.

## Floating Inputs and Pull-ups

An input pin that is connected to nothing is said to be **floating**. It picks up stray charge and may read high, low, or alternate between them. A switch connected between a pin and ground has the same problem when the switch is open.

The solution is a **pull-up resistor**: a resistor, typically 2.2k to 10k, from the pin to the supply. When nothing else drives the pin, the resistor pulls it high. When a switch or another chip connects the pin to ground, the pin reads low, because the resistor allows only a small current. A **pull-down** resistor works in the same way, towards ground.

Pull-ups make possible a kind of output called **open-drain**. An open-drain output can only pull a wire low. To make the wire high, the output stops driving it, and the pull-up raises it. Several open-drain outputs can share one wire safely. If any of them pulls low, the wire is low, and because none of them ever drives the wire high, two outputs cannot conflict. The two-wire I2C bus, described in [Talking to the World](#talking-to-the-world), works in this way.

## Reading a Schematic

A **schematic**, or circuit diagram, shows which components a circuit contains and how they are connected. It does not show where they are on the board. For the repair of any electronic device, the schematic is the most important document, because it shows what each part is for and what should be found at each point.

The conventions are the same in nearly every schematic:

- Each component is drawn as a symbol with its pins, and labelled with a **reference designator**, such as R4 or U2, and its value or part number. The same designator is printed beside the part on the board, which links the drawing to the hardware.
- Lines are wires. Where lines meet at a dot, they are connected; where they cross without a dot, they are not.
- Every set of connected pins is a **net**. A net may be given a name, such as SDA or CLK, and every place on the schematic with the same name is connected, even on different pages.
- **Power symbols** such as 3V3, 5V and GND are nets of the same kind. Every GND symbol is the same ground.
- The pins of a chip are numbered, and the number beside each connection gives the physical pin.

| Letter | Component    | Letter | Component           |
|--------|--------------|--------|---------------------|
| R      | resistor     | Q      | transistor          |
| C      | capacitor    | U      | integrated circuit  |
| L      | inductor     | Y, X   | crystal, oscillator |
| D      | diode, LED   | J, P   | connector           |
| F      | fuse         | SW     | switch              |
| FB     | ferrite bead | TP     | test point          |

Values are often written with the prefix in place of the decimal point, so that a point lost in printing cannot change the value: 4k7 is 4.7k, 2R2 is 2.2 ohms, and 100n is 100 nF. A part marked DNP ("do not populate") is drawn but left off the board.

A schematic is read by following nets. To find why an LED does not light, the reader finds the LED on the schematic, follows its net back through its resistor to the pin that drives it, and then checks each of these points on the board. Schematics are usually divided into blocks: the power supply, the clock, the main chip, the memory and each connector. A fault usually lies in one block, and the power block is checked first, because nothing works without it.

## Reading a Data Sheet

A **data sheet** is the manufacturer's description of a component. It is often long, but its parts are in a standard order, and most questions are answered by a few of them:

- **Pin descriptions** give the name and function of each pin.
- **Absolute maximum ratings** are the limits beyond which the part may be damaged, such as the highest voltage on any pin. They are not working conditions.
- **Recommended operating conditions** give the supply voltage and temperature range within which the part is guaranteed to work.
- **Electrical characteristics** give guaranteed figures: the input voltages read as low and high, the current an output can supply, and the current the part draws. Each figure has minimum, typical and maximum values; a design should rely on the minimum or maximum, not the typical.
- **Timing diagrams** show the order and spacing of signals, such as how long data must be steady before a clock edge.
- **Application circuits** show how the part is normally connected, including its decoupling capacitors.
- **Package drawings** give the physical dimensions.

Data sheets for the parts in an open design are usually listed in its documentation. Like the schematics, they should be kept with the equipment.

## Working Safely

Electrical work carries risks both to the person and to the equipment.

Hazards to the person:

- **Mains voltage.** Any device connected to a wall socket contains mains voltage somewhere, and mains voltage can kill. In a desktop computer, the power supply is inside the case. Power supplies, monitors and chargers also contain capacitors that can hold a dangerous charge for some time after they are unplugged. A power supply or other mains-powered device should be opened only by a person trained to do so.
- **High current.** Low voltages, such as the 5 V of a USB port or the 12 V inside a PC, are not a shock hazard. However, a short circuit across a battery or a large power supply can deliver enough current to heat a wire, a tool or a ring until it burns.
- **Batteries.** Lithium batteries can catch fire if they are punctured, crushed, overcharged or short-circuited.

Hazards to the equipment:

- **Static electricity.** A person walking across a carpet can build up a charge of thousands of volts. The discharge may not be felt, but it can destroy a chip. Touch a grounded metal object before handling a bare circuit board, and hold boards by their edges.
- **Short circuits.** A wire or tool that connects a supply directly to ground lets a large current flow, which can burn components and circuit board traces. Disconnect power before changing connections.
- **Pin limits.** A chip's output can supply only a few milliamps. Larger loads need a driver, as described in [Talking to the World](#talking-to-the-world).

The small computers described in this book run from a 5 V USB supply, and their circuit boards carry only low voltages. The mains hazards remain in the power adapter, which should be treated as a sealed unit.

## Making Connections

A **breadboard** is a plastic block with rows of spring contacts, into which components and wires are pushed without soldering. It is suited to trying a circuit, but its contacts loosen over time, and a circuit that is meant to last is soldered.

**Soldering** joins metal parts with a melted alloy, the solder. The iron, at about 330 to 380 degrees Celsius, heats the pin and the pad together for a second or two, and the solder is fed to them rather than to the iron, so that it flows onto both. A good joint is smooth and wets both surfaces; a dull, balled joint may not conduct reliably. Most solder wire has a core of flux, whose fumes should not be breathed, and leaded solder requires washing the hands afterwards. Most faults in hand-built and old equipment are bad joints and broken wires.

Before power is applied to a new connection, a few checks prevent most damage:

- **Ground** is shared: every device that exchanges signals must have its ground connected to the others.
- **Voltages match**: an output's high level suits the input it drives, as described under [Logic Levels](#logic-levels).
- **Polarity** is correct: batteries, diodes, LEDs and some capacitors work in only one direction, and a chip in its socket the wrong way round can be destroyed.
- **No short circuit**: the resistance between the supply and ground, measured with power off, is not near zero.
- **Pull-ups** are present where open-drain signals require them.

## Measuring and Finding Faults

A **multimeter** is the most useful measuring instrument for this work. It measures voltage when its two probes touch two points; current when it is placed in series, so that the current flows through it; resistance; and continuity, beeping when two points are connected. With a multimeter and Ohm's law, most electrical faults in a small computer can be found.

Two other instruments show signals that change too fast for a multimeter. An **oscilloscope** draws a voltage as it changes over time, showing whether a clock is running, whether a signal's edges are clean and whether a supply is steady. A **logic analyser** records many digital signals at once as highs and lows, and can decode buses such as I2C and SPI into the bytes they carry. Inexpensive USB logic analysers are sufficient for most work on small computers.

Faults are found most quickly in a fixed order:

1. **Look.** Burnt or discoloured parts, swollen capacitors, cracked joints, corrosion and loose connectors account for many faults.
2. **Power.** Each supply voltage is measured at the chips that use it, not only at the connector.
3. **Clock.** The crystal or oscillator is running at its specified frequency.
4. **Reset and configuration.** The chip has left reset; an FPGA has loaded its configuration.
5. **Signals.** Each signal is followed from where it is produced to where it is used, with the schematic.

Only one thing is changed at a time, and each result is written down. A working unit of the same kind, where one is available, gives the correct reading for every point.
