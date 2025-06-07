# FPGAs

## Introduction to FPGAs

### What is an FPGA?

An FPGA (Field-Programmable Gate Array) is a type of integrated circuit that can be configured by a user after manufacturing to perform specific tasks. Unlike CPUs or GPUs, which are designed for general-purpose computing, FPGAs are highly customizable and can be reprogrammed to suit various applications.

### Why Choose FPGAs?

FPGAs offer several advantages:

- Flexibility: Reprogrammable for different tasks.
- Parallel Processing: Capable of handling multiple tasks simultaneously.
- Efficiency: Lower power consumption compared to traditional CPUs for specific tasks.

### Applications of FPGAs

FPGAs are used in diverse fields, including:

- Digital Signal Processing
- Networking (e.g., packet processing)
- Automotive systems
- Defense systems
- Medical equipment

### Comparing FPGAs and ASICs

ASICs (Application-Specific Integrated Circuits) are custom-designed chips built for specific tasks, optimized for performance and efficiency in those particular functions.

#### Key Differences

1. **Flexibility**:
   - **FPGAs**: Highly flexible; can be reprogrammed to adapt to different tasks or evolving needs.
   - **ASICs**: Fixed functionality once manufactured; not designed for changes after production.

2. **Performance**:
   - **FPGAs**: Slower due to their programmable nature, but versatile enough for multiple tasks.
   - **ASICs**: Faster and more efficient as they are optimized for their specific task, often outperforming FPGAs in that area.

3. **Cost and Design Time**:
   - **FPGAs**: Cheaper and quicker to develop using pre-made chips and software tools, ideal for prototyping and varied applications.
   - **ASICs**: More expensive and time-consuming due to custom hardware design and manufacturing (silicon fabrication), but costs are amortized over high volumes.

4. **Power Consumption**:
   - **FPGAs**: Sometimes use more power due to their programmable components.
   - **ASICs**: Optimized for efficiency in their specific task, often using less power effectively.

5. **Use Cases**:
   - **FPGAs**: Ideal for flexible applications like research, prototyping, or dynamic environments where requirements change.
   - **ASICs**: Best suited for high-volume production with fixed needs, such as specialized tasks in networking or video processing.

## Basic Layout of a Simple FPGA

An FPGA is an integrated circuit that can be configured by the user after manufacturing to perform specific tasks. Unlike CPUs or GPUs, which are designed for general-purpose computing, FPGAs are highly customizable and can be reprogrammed to suit various applications.

Here's a basic overview of the key components in an FPGA:

1. **Configurable Logic Blocks (CLBs)**: These are the fundamental building blocks of an FPGA. CLBs contain Look-Up Tables (LUTs), which can be programmed to implement any logical function, such as AND gates, OR gates, or more complex functions.

2. **Flip-Flops**: These are used for storing data and creating timing delays in the circuit.

3. **Block RAMs (BRAMs)**: These are small blocks of memory that can be used for storage within the FPGA.

4. **Multipliers**: These are specialized hardwired circuits for performing multiplication operations, which are essential for arithmetic-intensive applications like digital signal processing or cryptography.

5. **I/O Blocks**: These are input/output blocks that allow the FPGA to connect to external devices, such as LEDs, buttons, or other microcontrollers.

6. **Interconnects**: These are the internal connections that route data between different parts of the FPGA. They can be programmed to create custom pathways for signals.

### What Are Look-Up Tables (LUTs)?

A Look-Up Table (LUT) is a memory component within an FPGA's Configurable Logic Block (CLB). LUTs are used to implement logical functions by storing the truth tables of those functions. For example:

- A 4-LUT can store 16 possible input combinations (since \(2^4 = 16\)) and their corresponding outputs.
- When an input is applied to the LUT, it looks up the stored truth table to determine the correct output.

LUTs are highly flexible because they can be reprogrammed to implement any logical function. For instance:

```verilog
// Truth table for a 2-LUT implementing an XOR gate:
input | output
0    | 1
1    | 0

// Verilog code for the same functionality:
output = (input == 1) ? 0 : 1;
```

### How Are LUTs Programmed?

LUTs are programmed by configuring their stored truth tables. This is done through a configuration file that defines how each CLB should be set up. The configuration file is generated using hardware description languages like Verilog or VHDL, and it specifies the desired logical operations for each part of the FPGA.

The programming process involves:

1. **Designing the Circuit**: Using a hardware description language (e.g., Verilog), you define how the circuit should behave.
   
2. **Synthesis**: Tools like Yosys convert the high-level Verilog code into a netlist, which describes the logical connections between components.

3. **Place and Route**: Nextpnr or other tools map the logical circuits to the physical layout of the FPGA, determining where each component will be placed and how signals will route through the interconnects.

4. **Configuration File Generation**: The final configuration file (often in `.bit` or `.sof` format) is generated, which contains the specific instructions for configuring each LUT and other components within the FPGA.

5. **Programming the FPGA**: The configuration file is loaded into the FPGA's memory using a programmer (e.g., a JTAG cable).

### Summary

FPGAs are highly flexible and programmable integrated circuits that can be configured to perform a wide variety of tasks. LUTs are the core components within FPGAs that store truth tables for logical functions, and they are programmed by generating configuration files in hardware description languages like Verilog or VHDL. By configuring these components, users can create custom digital circuits tailored to their specific needs.

### Tools

#### HDL Synthesis

An HDL (Hardware Description Language) synthesis tool processes a high-level descriptive code written in languages like Verilog or VHDL. This tool converts the abstract behavioral description of a digital circuit into a lower-level representation, such as a netlist, which defines the logical gates and connections required to implement the design on an FPGA. The synthesis tool optimizes the design for factors like area, speed, and power consumption, ensuring efficient use of the FPGA's resources.

#### Place-and-Route

After the HDL synthesis, the place-and-route tool takes the generated netlist and maps it onto the physical structure of the FPGA. This involves two main steps:

1. **Placing:** The tool determines the optimal positions for each component (like LUTs and flip-flops) on the FPGA chip to minimize delays and maximize efficiency.

2. **Routing:** It then routes the connections between these components, ensuring that all necessary signals can travel without interference or excessive delay. This step is crucial for managing the complex web of interconnections within the FPGA.

Together, these tools transform a high-level design into a physically realizable configuration on an FPGA, enabling the implementation of custom digital circuits.

## Verilog - Hardware Description Language

### Introduction to Verilog

Verilog is a hardware description language (HDL) used to describe digital circuits. It allows you to design and simulate hardware components, such as logic gates and microprocessors.

### Simple Verilog Example

In this example we will blink an LED (Light Emitting Diode).

```verilog
// LED blinking circuit
module blinky (
    input   clock_10hz,
    output  LED
);

reg led = 0;
wire clock;

assign clock = clock_10hz;

always @(posedge clock) begin
    led = ~led;
end

assign LED = led;

endmodule
```

This code defines a module that toggles an LED on and off using a clock input.

## Building the Blinky Circuit

### Tools Needed

- An FPGA computer or FPGA development board.
- Yosys: A HDL synthesis tool for converting Verilog code into a hardware description.
- nextpnr: Maps the description onto the FPGA chip.

You will also need a bitstream database and tools for the FPGA you're using, for example:

- Project IceStorm (ICE40)
- Project Trellis (ECP5)
- Project X-Ray (XC7)
- Project Peppercorn (CCGM1)

### Building and Programming the Blinky Circuit

Here’s how you might program an FPGA to blink an LED:

1. **Define the Circuit**:
   - As we did above, use Verilog to describe a simple oscillator circuit that toggles an output signal at regular intervals.

2. **Synthesize and Configure**:
   - Convert the Verilog code into a configuration file using synthesis tools.
   
3. **Program the FPGA**:
   - Load the configuration file onto the FPGA board using programming software.

4. **Test the Circuit**:
   - Connect an LED to the specified output pin and power on the board. The LED should start blinking according to the programmed oscillator frequency.

