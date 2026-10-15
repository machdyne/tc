# Describing Hardware

Circuits were once designed by drawing them. Digital circuits of any size are now described in text, in a **hardware description language** (HDL), and tools convert the description into a chip or an FPGA configuration. This chapter introduces Verilog, the HDL used for the designs in this book, and the steps from a description to a working circuit.

## A Different Kind of Language

Verilog resembles C, but it is not a programming language in the usual sense, and this is the most important point about it. A program is a list of steps carried out one after another. A Verilog description is a list of pieces of hardware that all exist, and all operate, at the same time.

The line `assign sum = a ^ b;` does not compute a value once. It places an XOR gate whose output is always the XOR of its inputs, for as long as the circuit has power. The order of such lines in the file does not matter, as the order of parts on a circuit diagram does not.

Two languages are in common use: **Verilog**, created in 1984, and **VHDL**, from the same period. Both are standardized and widely supported, and the ideas of one apply directly to the other.

## Verilog Modules

A Verilog design is built from **modules**, each with named **ports** for its inputs and outputs. The full adder from [Digital Logic](#digital-logic) is written as follows:

```verilog
module full_adder (
    input  wire a, b, cin,
    output wire sum, cout
);
    assign sum  = a ^ b ^ cin;
    assign cout = (a & b) | (cin & (a ^ b));
endmodule
```

A **wire** is a connection, carrying whatever drives it. Each `assign` statement is a piece of combinational logic driving a wire, written with the same operators as the Boolean algebra in [Digital Logic](#digital-logic). On an ECP5 FPGA, this module becomes two LUTs.

A module is used inside another by creating an **instance** of it, as a circuit board can carry several copies of one chip. A 32-bit adder could be made of 32 full adder instances, and a computer of thousands of instances of hundreds of modules.

## Numbers and Vectors

A port or wire can carry many bits at once. `wire [7:0] data` declares an 8-bit **vector**, with bits numbered 7 (most significant) down to 0. Single bits and ranges are selected with brackets, so `data[0]` is the lowest bit and `data[7:4]` the top four.

Numbers are written with their width and base: `8'd200` is the 8-bit decimal number 200, `4'b1010` is four bits in binary, and `32'hE000_0000` is 32 bits in hex, with an underscore for readability. Braces join vectors together: `{4'b0000, data[7:4]}` is an 8-bit value whose low four bits are the top of `data`.

## Registers and Clocks

Combinational logic has no memory. Flip-flops and registers are described with an `always` block that runs at each rising clock edge:

```verilog
// Blink an LED from a fast clock by counting clock cycles.
module blink #(
    parameter WIDTH = 24            // 2^24 cycles at 12 MHz: 1.4 s
) (
    input  wire clk,
    output wire led
);
    reg [WIDTH-1:0] count = 0;

    always @(posedge clk)
        count <= count + 1;

    assign led = count[WIDTH-1];    // the top bit changes slowest
endmodule
```

`reg [WIDTH-1:0] count` declares a 24-bit value. Anything assigned inside an `always` block must be declared as a `reg`, whether or not it becomes a hardware register; this one does. `always @(posedge clk)` means "at every rising edge of `clk`", and `count <= count + 1` loads the register with its value plus one. This is a counter built from 24 flip-flops and an adder, as in [Digital Logic](#digital-logic). Its top bit changes every 2 to the 23rd cycles, which with a 12 MHz clock is about every 0.7 seconds. The LED is therefore on for 0.7 seconds and off for 0.7 seconds, and one complete blink takes the 1.4 seconds given in the comment.

`WIDTH` is a **parameter**, a constant that can be set differently for each instance. A testbench, described under [Simulation](#simulation) below, can create a 4-bit version, which blinks after a few cycles instead of millions, and check it quickly in simulation.

## Two Kinds of Assignment

Inside an `always` block, Verilog has two assignment operators, and confusing them is the most common beginner's mistake.

The **non-blocking** assignment `<=` describes a register loading at the clock edge. All non-blocking assignments in a clocked block take effect together, using the values from before the edge, as physical flip-flops do. The following swaps two registers correctly:

```text
always @(posedge clk) begin
    a <= b;
    b <= a;
end
```

In hardware, these lines describe two flip-flops with their connections crossed: the input of `a` is wired to the output of `b`, and the input of `b` to the output of `a`. At each edge both load at the same instant, so they exchange their values.

The **blocking** assignment `=` takes effect immediately, so the next line sees the new value. Written with `=`, the second line above would read the new value of `a`, and both registers would end with the old value of `b`. It is used for combinational logic written inside `always @*` blocks, where `@*` means "whenever any input changes".

The general rule is to use `<=` in clocked blocks and `=` in combinational ones, and not to mix them in one block.

## State Machines in Verilog

The traffic light from [Digital Logic](#digital-logic) is written as follows:

```verilog
// The traffic light from Digital Logic, as a state machine.
module traffic (
    input  wire clk,
    input  wire reset,
    input  wire done,               // the timer has run out
    output wire green, yellow, red
);
    localparam GREEN = 2'd0, YELLOW = 2'd1, RED = 2'd2;

    reg [1:0] state;

    always @(posedge clk) begin
        if (reset)
            state <= RED;
        else if (done)
            case (state)
                GREEN:   state <= YELLOW;
                YELLOW:  state <= RED;
                default: state <= GREEN;
            endcase
    end

    assign green  = (state == GREEN);
    assign yellow = (state == YELLOW);
    assign red    = (state == RED);
endmodule
```

`localparam` gives names to the state numbers. The `always` block is the state register together with its next-state logic. On reset, the state becomes red; otherwise it advances when the timer is done and is unchanged when it is not. The `case` statement selects by the current state. The outputs are combinational, each true only in its own state. This module and the table in [Digital Logic](#digital-logic) describe the same behaviour.

Every state machine needs a **reset**, a defined state to start from. An FPGA gives its flip-flops known values when it is configured, but a custom chip does not. In addition, a simulator shows unknown values until something sets them, and a running circuit sometimes needs to start again without being reloaded.

## Simulation

Hardware is difficult to debug once it is built, because a value inside a chip cannot be printed. Designs are therefore first tested by **simulation**, in which a program computes what the circuit would do, cycle by cycle, and every signal can be inspected.

A simulation is driven by a **testbench**. This is a Verilog module that describes no hardware, but is a script that creates an instance of the design, supplies its inputs and checks its outputs. Testbenches may use features that cannot become hardware, such as delays, loops over test values and printed messages. The main part of the full adder's testbench tries all eight input combinations and compares each result with ordinary addition:

```verilog
        for (i = 0; i < 8; i = i + 1) begin
            {a, b, cin} = i;
            #1;
            if ({cout, sum} !== a + b + cin)
                errors = errors + 1;
        end
```

`#1` waits one time unit for the logic to settle.

A simulator can also record every signal over time, to be viewed as **waveforms**: one horizontal line per signal, drawn high or low, with numbers written along the line for multi-bit values, all against a common time axis, much as a logic analyser displays a real circuit. A fault is found by locating the first moment at which some signal differs from what was intended and following it back to its cause.

A whole computer can be simulated in the same way. The testbench loads a program's machine code into the simulated memory, from a file of hex numbers, and lets the simulated processor run it. Simulation is many thousands of times slower than the hardware, so only short programs are practical, but every signal is visible at every cycle. Most faults in a new processor or device are found this way before the design is ever loaded into an FPGA.

## From Description to Bitstream

Converting a tested design into an FPGA configuration takes several steps, each done by a tool:

```text
  Verilog source          what the circuit does
       |
   synthesis              -> netlist: LUTs, flip-flops, RAMs, wires
       |
   place and route        -> each part given a place on the chip,
       |                     each wire a path through the routing
   bitstream generation   -> the configuration bits
       |
   programming            -> loaded into the FPGA or its flash
```

**Synthesis** reads the HDL, determines the logic it describes, simplifies it, and maps it onto the building blocks the FPGA provides. The result, a **netlist**, lists every LUT and flip-flop and how they connect. Yosys is a widely used open synthesis tool.

**Place and route** decides which physical block on the chip each part of the netlist will use, then finds paths through the routing for every connection. It also analyses timing and reports the fastest clock the design can use. nextpnr is a widely used open place-and-route tool.

**Bitstream generation**, called packing by some of the open tools, converts the placed and routed design into the configuration format of the particular FPGA.

**Programming** loads the bitstream into the FPGA, or writes it into the configuration flash so that the FPGA loads it at every start.

The tools also need a **constraints file**, which says which signal goes to which physical pin, what voltage standard each pin uses, and how fast each clock runs. A board's constraints file is written once and reused by every design for that board.

These steps can take seconds for a small design and many minutes for a large one, because placement and routing are difficult search problems. For a design of any size they need far more memory and speed than a small computer has, so they run on a larger computer. Experimental tools that run on an FPGA computer itself can build simple designs, but not a design as large as the computer's own.

## Reading the Reports

The tools report two numbers that matter on every build.

**Utilization** states how much of the chip the design uses: the LUTs, block RAMs and other resources used, out of those available. As a chip fills, the placer has less room to work with and timing becomes harder to meet. Above about three quarters full, designs become noticeably harder to build.

**Timing** gives the maximum frequency of each clock, based on the critical path described in [Digital Logic](#digital-logic). If it is below the frequency at which the design runs, the circuit may work on the bench and fail when warm, or fail in rare and confusing ways. A design that does not meet timing is not complete.

## Debugging on the Board

A design that works in simulation can still fail on the board: a pin is assigned wrongly in the constraints, an external chip behaves differently from its model, or a timing problem appears only in hardware. Signals inside an FPGA cannot be probed directly, so a design is given ways to show what it is doing:

- **LEDs** driven by internal signals show whether a clock is running, a state has been reached or an error has occurred.
- **Spare pins** can carry internal signals to an oscilloscope or logic analyser.
- **A serial port** in the design can report values as text, which is often the first sign of life from a new design.
- **An internal logic analyser**, a small circuit added to the design, records chosen signals into block RAM when a condition occurs, and sends the recording to another computer to be displayed as waveforms.
- **JTAG**, a standard debug connection present on most larger FPGAs, is used to load bitstreams directly and, with suitable support in the design, to read internal state.

A known good bitstream is kept, changes are made one at a time, and each new part is tested by itself before it is joined to the rest.

## Classic Mistakes

- **Blocking assignments in clocked blocks.** Registers should be assigned with `<=`.
- **Accidental latches.** In a combinational `always @*` block, every output must be assigned in every case. If an `if` has no `else`, the tool must keep the old value and so builds a latch, usually unintentionally.
- **Two drivers.** A signal can be driven from only one place. Assigning the same register in two different `always` blocks fails in synthesis, even if the simulator accepts it.
- **Missing reset.** Registers that must start in a known state need a reset or an initial value.
- **Unsynchronized inputs.** A button or a signal from another clock must pass through two flip-flops before it is used, as described in [Digital Logic](#digital-logic).
- **Width mismatches.** Assigning a 32-bit value to an 8-bit register silently drops the top bits. Tools warn about this, and the warnings should be read.
- **Simulation-only code.** Delays such as `#1`, printed messages and the scripted steps of a testbench cannot become hardware, and synthesis ignores or rejects them. A design that depends on them works only in the simulator.
- **Making clocks with logic.** Dividing a clock with a counter and using the result as another clock causes timing problems. The alternatives are to use the PLL, or to keep one clock and use the counter as an enable.

The blink module above follows the last rule. It does not create a slow clock; it uses the top bit of a counter that runs on the fast one.
