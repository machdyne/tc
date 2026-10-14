# Electricity

A computer is an electrical machine. Every number it stores and every decision it makes is a voltage on a wire. This chapter describes the electricity needed to understand the rest of the book, and to connect devices to a computer without damaging either.

## Charge and Current

All matter is made of atoms. An atom has a small, heavy centre, the nucleus, which carries positive electric charge, surrounded by much lighter electrons, which carry negative charge. Opposite charges attract and like charges repel.

In some materials, mostly metals, the outermost electrons are loosely held and can drift from atom to atom. These materials are **conductors**. In others, such as glass, plastic and dry air, the electrons are held tightly. These are **insulators**. A wire is a conductor wrapped in an insulator.

When electrons drift along a conductor in one direction, charge flows. That flow is **current**, measured in **amperes** (A), usually shortened to amps. One amp is a large current in electronics. Most signals in a computer carry a few thousandths of an amp, written milliamps (mA).

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

Large resistances are written with prefixes: 1,000 ohms is 1 kilohm (1k), and 1,000,000 ohms is 1 megohm (1M). The same prefixes apply to every unit: a millivolt is a thousandth of a volt, and a microamp a millionth of an amp.

## Power

**Power** is the rate at which energy is used, measured in **watts** (W):

```text
P = V x I      power = voltage x current
```

A circuit drawing 0.5 A from a 5 V supply uses 2.5 W. Almost all of that power ends up as heat. For this reason a resistor carrying too much current becomes hot, and a processor needs cooling.

Power matters for timeless computing because it determines what a computer can run from. A small FPGA computer typically uses a few watts, about what a USB phone charger can supply. A desktop computer can use a hundred times as much. A few watts can come from a modest battery or a small solar panel; a hundred watts requires a substantial installation.

## Direct and Alternating Current

A battery produces **direct current** (DC): its voltage always has the same polarity. Mains electricity is **alternating current** (AC): its voltage reverses many times a second, which makes it easy to transform between voltages and to send over long distances.

Electronic circuits run on low-voltage DC. A power adapter converts mains AC to DC, typically 5 V for USB. Inside the computer, **regulators** convert that to the exact voltages each chip needs: 3.3 V for most input and output signals, and lower voltages, often around 1 V, for the core of an FPGA or processor. Lower voltages waste much less power, and the small transistors in a modern chip core cannot tolerate higher ones.

## Components

A few types of component make up nearly every circuit board.

- **Resistors** limit current and set voltages.
- **Capacitors** store a small amount of charge. Placed next to a chip, they supply the brief bursts of current the chip needs when it switches, and reduce noise on the power supply. These are **decoupling** capacitors, and every chip has them.
- **Inductors** store energy in a magnetic field and resist changes in current. They appear mainly in power supplies.
- **Diodes** let current flow in one direction only. An LED is a diode that emits light when current flows.
- **Crystals** and **oscillators** vibrate at a precise frequency and provide the steady timing signal, the clock, that a computer runs on.
- **Transistors** are switches controlled by electricity. They are the subject of the next section.
- **Integrated circuits** (ICs, or chips) are complete circuits, sometimes containing billions of transistors, made on a single piece of silicon and sealed in a package with metal pins.

## The Transistor as a Switch

A transistor has three connections. A voltage on one of them, the **gate**, controls whether current can flow between the other two. Used in this way, a transistor is a switch with no moving parts. It can turn on and off billions of times a second without wearing out.

The type used in digital chips is the MOSFET, which comes in two complementary forms. An n-type transistor conducts when its gate is high (near the supply voltage). A p-type transistor conducts when its gate is low (near ground). One of each, connected in series between the supply and ground with their gates joined, forms the simplest digital circuit, an **inverter**:

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

## Working Safely

Electrical work carries risks both to the person and to the equipment.

Hazards to the person:

- **Mains voltage.** Any device connected to a wall socket contains mains voltage somewhere, and mains voltage can kill. In a desktop computer, the power supply is inside the case. Power supplies, monitors and chargers also contain capacitors that can hold a dangerous charge for some time after they are unplugged. A power supply or other mains-powered device should be opened only by a person trained to do so.
- **High current.** Low voltages, such as the 5 V of a USB port or the 12 V inside a PC, are not a shock hazard. However, a short circuit across a battery or a large power supply can deliver enough current to heat a wire, a tool or a ring until it burns.
- **Batteries.** Lithium batteries can catch fire if they are punctured, crushed, overcharged or short-circuited.

Hazards to the equipment:

- **Static electricity.** A person walking across a carpet can build up a charge of thousands of volts. The discharge may not be felt, but it can destroy a chip. Touch a grounded metal object before handling a bare circuit board, and hold boards by their edges.
- **Short circuits.** A wire or tool that connects a supply directly to ground lets a large current flow, which can burn components and circuit board traces. Disconnect power before changing connections.
- **Pin limits.** A chip's output can supply only a small current, often a few milliamperes. A motor, relay or long string of LEDs must be driven through a transistor or driver chip.

The small computers described in this book run from a 5 V USB supply, and their circuit boards carry only low voltages. The mains hazards remain in the power adapter, which should be treated as a sealed unit.

A **multimeter** is the most useful measuring instrument for this work. It measures voltage when its two probes touch two points; current when it is placed in series, so that the current flows through it; resistance; and continuity, beeping when two points are connected. With a multimeter and Ohm's law, most electrical faults in a small computer can be found.
