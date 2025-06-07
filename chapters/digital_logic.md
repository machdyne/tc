# Digital Logic

## Binary & Other Number Systems

Computers operate on binary principles, but humans often use different numbering systems that translate into these binary operations. Understanding various number systems is fundamental to working with computers and digital systems.

### The Decimal System (Base-10)

The decimal system, also known as base-10, uses ten digits: `0` through `9`. It is the numbering system we use in everyday life because it aligns with the way humans count using our fingers.

### The Binary System

The binary system uses two digits: 0 and 1 (off and on). This is ideal for digital systems because it corresponds directly to the physical states of electronic components.

#### Counting in Binary

| Binary | Decimal |
|--------|---------|
| `0`    | 0       |
| `1`    | 1       |
| `10`   | 2       |
| `11`   | 3       |
| `100`  | 4       |
| `101`  | 5       |
| `110`  | 6       |
| `111`  | 7       |
| `1000` | 8       |
| `1001` | 9       |
| `1010` | 10      |
| `1011` | 11      |
| `1100` | 12      |
| `1101` | 13      |
| `1110` | 14      |
| `1111` | 15      |

#### Converting Binary to Decimal

To convert a binary number to decimal, you add up the values of each bit that is turned on (`1`). For example:

- Binary `0001` (1 = 1 in decimal)
- Binary `0010` (2 = 2 in decimal)
- Binary `0011` (2 + 1 = 3 in decimal)
- Binary `1010` (8 + 2 = 10 in decimal)
- Binary `1111` (8 + 4 + 2 + 1 = 15 in decimal)

### The Hexadecimal System (Base-16)

Hexadecimal, or "hex," uses base-16 and includes digits from `0-9` and letters `A-F` (or `a-f`), where `A` represents 10, `B` represents 11, up to `F` representing 15.

Why Use Hexadecimal?

Hexadecimal is commonly used in computing because it provides a more compact representation of binary data. Each hexadecimal digit corresponds to four binary digits (a nibble), making it easier to work with and read binary values.

Here are some examples of hexadecimal numbers along with their corresponding binary and decimal values:

| Hexadecimal | Binary      | Decimal |
|-------------|-------------|---------|
| 0           | 0000        | 0       |
| 1           | 0001        | 1       |
| A           | 1010        | 10      |
| F           | 1111        | 15      |
| 10          | 0001 0000   | 16      |
| FF          | 1111 1111   | 255     |
| 8C          | 1000 1100   | 140     |

### The Octal System (Base-8)

Octal, or "oct," uses base-8 and includes digits from `0-7`. It was historically used in early computing systems but is less common today.

Why Use Octal?

Octal is useful for simplifying the representation of binary data into smaller chunks. Each octal digit corresponds to three binary digits (bits).

Example:

- Binary: `001 010 110`  
- Octal: `126`

### General Numbering System Overview

All numbering systems can be categorized by their base, which determines the number of unique digits they use.

| Base | Name         | Common Uses                          |
|------|--------------|---------------------------------------|
| 2    | Binary       | The foundation of digital computing. |
| 8    | Octal        | Less common; used in older systems.  |
| 10   | Decimal      | The standard numbering system for humans. |
| 16   | Hexadecimal | Common in computing and electronics. |

### Why Different Numbering Systems?

Different numbering systems are used because:

1. Efficiency: Binary is efficient for computers but less readable for humans.
2. Readability: Hexadecimal and octal provide a more compact and human-readable format than binary.
3. Legacy Systems: Some older systems relied on octal or decimal representations.


## Logic Gates

### What is a Logic Gate?

A logic gate is a fundamental building block of digital circuits. It processes one or more input signals (binary values of 0 or 1) and produces a single binary output based on specific rules defined by its type. By combining them, you can create complex functions like adders, multipliers, and even entire CPUs.

### Basic Logic Gates

Here are truth tables for some of the fundamental types of logic gates:

1. AND Gate: Outputs true only if both inputs are true.

| Input A | Input B | Output |
|---------|---------|--------|
|    0    |    0    |    0   |
|    0    |    1    |    0   |
|    1    |    0    |    0   |
|    1    |    1    |    1   |

2. OR Gate: Outputs true if at least one input is true.

| Input A | Input B | Output |
|---------|---------|--------|
|    0    |    0    |    0   |
|    0    |    1    |    1   |
|    1    |    0    |    1   |
|    1    |    1    |    1   |

3. NOT Gate: Inverts the input.

| Input | Output |
|-------|--------|
|    0  |    1   |
|    1  |    0   |

4. NAND Gate: NOT AND.

| Input A | Input B | Output |
|---------|---------|--------|
|    0    |    0    |    1   |
|    0    |    1    |    1   |
|    1    |    0    |    1   |
|    1    |    1    |    0   |

5. XOR Gate: Exclusive OR.

| Input A | Input B | Output (Y) |
|---------|---------|------------|
|    0    |    0    |     0      |
|    0    |    1    |     1      |
|    1    |    0    |     1      |
|    1    |    1    |     0      |

### Real-World Analogy

Think of an AND gate as a car's ignition system, requiring both the key and the brake pedal to be pressed before starting the engine.

## Digital Circuits

### Building Blocks

Digital circuits are constructed using logic gates. For example:

- Half Adder: Adds two binary digits.

| Input A | Input B | Sum | Carry |
|---------|---------|-----|-------|
|    0    |    0    |  0  |   0   |
|    0    |    1    |  1  |   0   |
|    1    |    0    |  1  |   0   |
|    1    |    1    |  0  |   1   |

The construction of a half adder involves two fundamental logic gates: 

1. XOR (Exclusive OR) Gate: This gate calculates the sum (S) of the two binary inputs (A and B). The XOR gate outputs 1 when the inputs are different and 0 when they are the same.

2. AND Gate: This gate determines the carry (C) output. It outputs 1 only if both inputs (A and B) are 1, indicating that a carry is generated to the next higher bit.

Thus, a half adder consists of one XOR gate for the sum and one AND gate for the carry.

The half-adder is essential because it forms the basis of more complex arithmetic circuits. Without the ability to add binary digits, a computer cannot perform basic arithmetic operations, which are fundamental to nearly all computations.
