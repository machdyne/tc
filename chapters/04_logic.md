# Digital Logic

Digital logic builds decisions, arithmetic and memory out of switches. This chapter starts with single gates and ends with the parts from which every processor is made. The same parts reappear later as the contents of an FPGA and as the things a hardware designer describes.

## Logic Gates

A **logic gate** is a small circuit with one or more inputs and one output, each either 0 or 1. The behaviour of a gate is completely described by a **truth table**, which lists the output for every combination of inputs.

The common gates, for two inputs A and B:

| A   | B   | AND | OR  | NAND | NOR | XOR | XNOR |
|-----|-----|-----|-----|------|-----|-----|------|
| 0   | 0   | 0   | 0   | 1    | 1   | 0   | 1    |
| 0   | 1   | 0   | 1   | 1    | 0   | 1   | 0    |
| 1   | 0   | 0   | 1   | 1    | 0   | 1   | 0    |
| 1   | 1   | 1   | 1   | 0    | 0   | 0   | 1    |

- **AND** is 1 only when both inputs are 1.
- **OR** is 1 when either input is 1, or both.
- **XOR** (exclusive or) is 1 when the inputs differ.
- **NAND**, **NOR** and **XNOR** are AND, OR and XOR with the output inverted.

The **NOT** gate, or inverter, has one input and outputs its opposite. It is the CMOS circuit from the chapter [Electricity](#electricity).

Gates with more inputs work the same way. A four-input AND is 1 only when all four inputs are 1.

## Boolean Algebra

Logic can be written as algebra, named after George Boole, who described it in 1854. This book writes AND as `&`, OR as `|`, XOR as `^` and NOT as `~`, the symbols used by C and Verilog.

These rules simplify and rearrange logic:

```text
A & 1 = A         A | 0 = A        AND with 1, OR with 0: unchanged
A & 0 = 0         A | 1 = 1        AND with 0 is 0; OR with 1 is 1
A & A = A         A | A = A
A & ~A = 0        A | ~A = 1       a value and its opposite
~~A = A                            double inversion cancels
~(A & B) = ~A | ~B                 De Morgan's laws:
~(A | B) = ~A & ~B                 invert, swap AND and OR
```

De Morgan's laws are the most useful. They say that NOT-AND is the same as OR-ing the inverted inputs, so any circuit can be rearranged between ANDs and ORs. Hardware tools apply rules like these automatically to reduce a circuit to a smaller equivalent.

## Everything From NAND

The NAND gate is **universal**: any logic circuit can be built from NAND gates alone.

```text
NOT A    = A NAND A
A AND B  = NOT (A NAND B)  = (A NAND B) NAND (A NAND B)
A OR B   = (NOT A) NAND (NOT B)                  (De Morgan)
```

NOR is also universal. As a result, a computer can be built from one kind of building block, repeated, which is one reason chips can have a regular structure. An FPGA takes the same idea further, as the chapter [Inside an FPGA](#inside-an-fpga) explains: it uses one kind of programmable block that can become any gate.

## Combinational Circuits

A circuit whose outputs depend only on its present inputs is **combinational**. Four combinational circuits appear everywhere.

A **multiplexer** selects one of several inputs. Given a select input S, a 2-to-1 multiplexer outputs A when S is 0 and B when S is 1:

```text
out = (A & ~S) | (B & S)
```

With more select bits, a multiplexer can choose among 4, 8 or more inputs. A processor uses multiplexers to select which register feeds the arithmetic unit, and which result is written back.

A **decoder** turns a binary number into one active line. A 2-to-4 decoder has two inputs and four outputs, and exactly one output is 1: the one whose number matches the input. A computer uses decoders to select one memory chip or one device out of many, based on an address.

An equality **comparator** checks whether two numbers are equal. It applies XNOR to each pair of corresponding bits and combines all the results with AND.

An **adder** adds binary numbers. When two single bits A and B are added, the sum bit is A XOR B, and there is a carry exactly when both are 1, which is A AND B. That circuit is a **half adder**:

| A   | B   | Sum (A ^ B) | Carry (A & B) |
|-----|-----|-------------|---------------|
| 0   | 0   | 0           | 0             |
| 0   | 1   | 1           | 0             |
| 1   | 0   | 1           | 0             |
| 1   | 1   | 0           | 1             |

To add numbers of many bits, each column must also add the carry from the column to its right. A **full adder** takes three inputs, A, B and a carry in:

```text
sum       = A ^ B ^ carry_in
carry_out = (A & B) | (carry_in & (A ^ B))
```

Full adders chained together, each one's carry out feeding the next one's carry in, form an adder for numbers of any width. This is a **ripple-carry adder**:

```text
     A3 B3       A2 B2       A1 B1       A0 B0
      | |         | |         | |         | |
    +-----+     +-----+     +-----+     +-----+
 <--| FA  |<----| FA  |<----| FA  |<----| FA  |<-- carry in (0)
    +-----+     +-----+     +-----+     +-----+
       |           |           |           |
       S3          S2          S1          S0
```

The same adder can subtract. As the chapter [Information](#information) explained, a two's complement number is negated by inverting its bits and adding one. To compute A - B, each bit of B is inverted with an XOR gate and the first carry in is set to 1. A single control bit therefore turns an adder into a subtractor.

An adder that can also subtract, AND, OR and compare, with a multiplexer to choose which result comes out, is an **arithmetic logic unit** (ALU), the part of a processor that performs calculations.

## Propagation Delay

A gate does not respond instantly. Its output changes a short time after its input, typically a fraction of a nanosecond in a modern chip. This is its **propagation delay**.

Delays add up along a path. In a ripple-carry adder, the carry may have to pass through every stage before the top bit of the sum is correct, so a 32-bit adder is much slower than a 4-bit one. While the carry is still rippling, the outputs are briefly wrong. Faster adders use extra logic to compute carries in parallel. In general, every combinational circuit needs time to settle, and the rest of the system must wait until it has.

## Sequential Circuits

A combinational circuit has no memory: when its inputs change, the previous result is lost. A computer also needs circuits that remember. A circuit whose outputs depend on what happened before is **sequential**.

Memory comes from **feedback**: an output connected back to an input. Two NOR gates connected in a loop form a **latch**:

```text
   R ---+-----+
        | NOR |--+---------> Q
    +---+-----+  |
    |            |
    +-------\ /--+        each gate's output is fed back
             X            into an input of the other gate
    +-------/ \--+
    |            |
    +---+-----+  |
        | NOR |--+---------> ~Q
   S ---+-----+
```

The upper gate computes `Q = NOR(R, ~Q)`, and the lower one `~Q = NOR(S, Q)`. A NOR gate outputs 1 only when both its inputs are 0. Setting and then resetting the latch takes three steps:

| Step             | S   | R   | ~Q  | Q   |
|------------------|-----|-----|-----|-----|
| S goes high      | 1   | 0   | 0   | 1   |
| S goes low again | 0   | 0   | 0   | 1   |
| R goes high      | 0   | 1   | 1   | 0   |

In the first step, S is 1, so the lower gate gives 0; the upper gate then sees R and `~Q` both at 0, and gives 1. In the second step neither input is high, yet Q stays at 1, because each gate's output holds the other gate in place. In the third, R forces Q to 0, which lets the lower gate's output rise to 1. The latch has remembered that S was the last input to be high. A high pulse on S (set) therefore sets Q to 1, and a high pulse on R (reset) sets Q to 0. With both inputs low, the loop holds its last state, so it stores one bit. S and R must never be high at the same time, because both outputs would then be 0 and the state that followed would be unpredictable.

## The Clock and the Flip-Flop

A large circuit built from many latches is difficult to analyse, because each change propagates through it at its own pace. Almost all digital design instead follows one discipline: a single signal, the **clock**, switches steadily between 0 and 1, and the circuit's memory changes only at one moment of each clock cycle, the **rising edge**, when the clock goes from 0 to 1.

The element used for this is the **D flip-flop**. It has a data input D, a clock input and an output Q. At each rising edge of the clock, Q takes the value D has at that instant, and holds it until the next rising edge, whatever D does in between.

```text
clock   __/~~\__/~~\__/~~\__/~~\__
D       ~~~~~~\________/~~~~~~~~~~
Q       __/~~~~~\___________/~~~~~
          ^     ^     ^     ^
          each rising edge copies D to Q
```

Between edges, the combinational logic is free to settle. At the edge, the flip-flops capture the settled results all at once. Then the logic settles again from the new values. This **synchronous** style divides the operation of a circuit into a sequence of discrete steps, one per clock cycle, and it is how processors, and almost everything built in an FPGA, are designed.

The clock's speed is measured in **hertz** (Hz), cycles per second. One megahertz (MHz) is a million cycles per second, so a 48 MHz clock has a rising edge about every 21 nanoseconds.

## Registers, Counters and Shift Registers

Several flip-flops side by side on the same clock store a multi-bit number. This is a **register**. A 32-bit register is 32 flip-flops.

A register whose output passes through an adder that adds one, and back into its input, is a **counter**: its value increases by one at every clock edge. Counters measure time, count events, step through memory and divide clocks. The top bit of a 24-bit counter on a 12 MHz clock changes about once every 0.7 seconds, so an LED driven by it is on for 0.7 seconds and off for 0.7 seconds. This is the usual way to blink an LED from a fast clock, as shown in [Describing Hardware](#describing-hardware).

Flip-flops connected in a chain, each one's output feeding the next one's input, form a **shift register**: each clock edge moves every bit one place along. It converts between serial and parallel data: bits loaded one at a time can be read out together, or the reverse. Every serial connection in a computer, from a keyboard cable to a network, has shift registers at each end.

## State Machines

A **state machine** is a register that holds the current state, plus combinational logic that computes the next state from the current state and the inputs. At each clock edge, the machine moves to its next state.

A simple traffic light controller has three states:

```text
            timer done              timer done
   +-------+ ---------> +--------+ ---------> +-----+
   | GREEN |            | YELLOW |            | RED |
   +-------+            +--------+            +-----+
       ^                                         |
       +-----------------------------------------+
                         timer done
```

| Current state | Input         | Next state | Lights    |
|---------------|---------------|------------|-----------|
| GREEN         | timer done    | YELLOW     | green on  |
| YELLOW        | timer done    | RED        | yellow on |
| RED           | timer done    | GREEN      | red on    |
| any           | timer running | (same)     | (same)    |

The three states fit in two bits of a register, and the table becomes a few gates. Every controller in a computer, from the circuit that reads a keyboard to the control unit of a processor, is a state machine of this kind, sometimes with many more states.

## Timing

Synchronous design has one hard rule: the combinational logic between two flip-flops must settle before the next clock edge. More precisely, each flip-flop needs its input to be stable for a short **setup time** before the edge, and to remain stable for a short **hold time** after it.

The slowest path in the whole circuit, called the **critical path**, therefore sets the fastest usable clock. If the longest path, including the setup time, takes 20 nanoseconds to settle, the clock can be at most 50 MHz. To use a faster clock, a designer must shorten that path, for example by splitting a long calculation over two clock cycles. Hardware tools report the critical path and the maximum clock frequency of every design, and FPGA designers check this figure routinely.

A second problem arises when a signal from outside, such as a button or a signal from a circuit on a different clock, changes at the moment a flip-flop samples it. The flip-flop can be caught between 0 and 1 for a moment, a condition called **metastability**. The standard remedy is to pass such signals through two flip-flops in a row before using them, giving any uncertainty a full clock cycle to resolve.

## From Logic to a Processor

Every part of a processor has now been described:

- **registers** to hold numbers
- an **ALU** of adders and gates to compute with them
- **multiplexers** to route values between them
- **decoders** to select memory and devices
- a **state machine** to step through the work, one clock cycle at a time

The next chapter puts these parts together into a computer.
