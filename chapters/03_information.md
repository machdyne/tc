# Information

A wire in a computer is either high or low. Everything a computer handles, whether a number, a letter, a photograph or a program, must be expressed as patterns of those two states. This chapter describes how this is done.

## Bits

A single high-or-low value is a **bit**, short for binary digit, written as 1 or 0. One bit can answer one yes-or-no question. Two bits can distinguish four things (00, 01, 10, 11), three bits eight things, and in general n bits can distinguish 2 to the power n things. Each extra bit doubles the count.

Computers use two states rather than ten because two states are the easiest to distinguish reliably, as the previous chapter explained.

## Counting in Binary

Ordinary numbers are written in **decimal**, or base 10. Each position is worth ten times the one to its right: in 352, the 3 means three hundreds, the 5 five tens and the 2 two ones.

**Binary**, or base 2, works the same way with two digits. Each position is worth twice the one to its right:

```text
position value:  128  64  32  16   8   4   2   1
binary digits:     1   0   0   0   1   1   0   0
                 128 +             8 + 4           = 140
```

A binary number is read by adding the values of the positions that hold a 1. A number is written in binary by subtracting the largest position value that fits, marking a 1 in that position, and repeating with the remainder.

The first sixteen numbers:

| Decimal | Binary | Decimal | Binary |
|---------|--------|---------|--------|
| 0       | 0000   | 8       | 1000   |
| 1       | 0001   | 9       | 1001   |
| 2       | 0010   | 10      | 1010   |
| 3       | 0011   | 11      | 1011   |
| 4       | 0100   | 12      | 1100   |
| 5       | 0101   | 13      | 1101   |
| 6       | 0110   | 14      | 1110   |
| 7       | 0111   | 15      | 1111   |

The rightmost bit, worth 1, is called the **least significant bit**. The leftmost is the **most significant bit**. A number is odd exactly when its least significant bit is 1. Shifting all the bits one place left doubles a number; shifting them right halves it, discarding any remainder.

## Bytes and Words

Bits are handled in groups. A group of 8 bits is a **byte**, which can hold 256 different values, 0 to 255. A group of 4 bits, half a byte, is a **nibble**.

A processor works most naturally with a fixed size of group called its **word**. The processors in this book have 32-bit words; small microcontrollers and older computers use 8 or 16 bits. The size of a group determines the range of numbers it can hold:

| Bits | Values        | Unsigned range          |
|------|---------------|-------------------------|
| 8    | 256           | 0 to 255                |
| 16   | 65,536        | 0 to 65,535             |
| 32   | 4,294,967,296 | 0 to about 4.29 billion |

## Hexadecimal

Long binary numbers are hard for people to read and easy to miscopy. **Hexadecimal**, or hex, is base 16, and each hex digit stands for exactly four bits. The digits are 0 to 9 and then A to F for ten to fifteen.

| Hex | Binary | Decimal | Hex | Binary | Decimal |
|-----|--------|---------|-----|--------|---------|
| 0   | 0000   | 0       | 8   | 1000   | 8       |
| 1   | 0001   | 1       | 9   | 1001   | 9       |
| 2   | 0010   | 2       | A   | 1010   | 10      |
| 3   | 0011   | 3       | B   | 1011   | 11      |
| 4   | 0100   | 4       | C   | 1100   | 12      |
| 5   | 0101   | 5       | D   | 1101   | 13      |
| 6   | 0110   | 6       | E   | 1110   | 14      |
| 7   | 0111   | 7       | F   | 1111   | 15      |

To convert binary to hex, the binary digits are split into groups of four from the right, and each group is replaced with its hex digit. The byte `1000 1100` is `8C` in hex, and a byte is always exactly two hex digits. A 32-bit word is eight hex digits, such as `0x4000_0000`. The `0x` prefix marks a number as hex, and an underscore is sometimes added, as here, to make long numbers easier to read.

Hex is used wherever the individual bits matter: memory addresses, hardware registers, colours and the contents of files. Decimal is used for quantities.

**Octal**, base 8, uses one digit for every three bits. It was common on older machines and remains in use in a few places, such as the file permissions of **Unix**, an operating system first written in 1969 whose design lives on in Linux, the BSD systems and macOS.

## Negative Numbers

A group of bits has no sign of its own; it is only a pattern. To represent negative numbers, nearly every computer uses a convention called **two's complement**: the most significant bit counts as negative.

In an 8-bit two's complement number, the leftmost position is worth -128 instead of +128:

```text
position value: -128  64  32  16   8   4   2   1
                   1   1   1   1   1   1   1   1  = -128 + 127 = -1
                   1   0   0   0   0   0   0   0  = -128
                   0   1   1   1   1   1   1   1  = 127
```

So 8 bits hold -128 to 127 when treated as signed, or 0 to 255 when treated as unsigned. The bits are the same; only the interpretation differs.

A two's complement number is negated by inverting every bit and adding one. The main advantage of the convention is that addition needs no special case: the same adding circuit works for both positive and negative numbers, and subtraction is the addition of the negated number.

## Overflow

A group of bits has a fixed range. Adding 1 to the largest value does not produce a larger number; the result wraps around to the smallest value, as a car's odometer returns to zero after its highest reading.

In Machdyne BASIC, the language of the chapter [BASIC](#basic), every number is a 16-bit signed integer, so the range is -32768 to 32767. `32767 + 1` gives -32768, and `300 * 300` gives 24464, which is 90000 with the excess bits thrown away. Larger languages use more bits, which raises the limit but does not remove it. Overflow is a common source of errors, and a programmer should know how large the numbers in a program can become.

## Fractions

Many quantities are not whole numbers. There are two common ways to store fractions.

**Fixed point** stores whole numbers with an agreed, implied scale. Prices stored in cents are fixed point: 1999 means 19.99. It is exact and fast, and it is how small machines without fraction hardware usually work.

A fixed-point format can also give a fixed number of bits to the fraction. In a 32-bit number with 16 fraction bits, the integer 98,304 means 98,304 / 65,536 = 1.5. Addition is ordinary integer addition; a multiplication, with the product held in 64 bits, is followed by a shift right of 16 bits to restore the scale.

**Floating point** stores a number as a set of significant digits and a separate exponent, like scientific notation in binary: a sign, a fraction and a power of two. Nearly every computer uses the formats of the standard IEEE 754:

| Format | Bits | Sign, exponent, fraction | Decimal digits | Largest       |
|--------|------|--------------------------|----------------|---------------|
| single | 32   | 1, 8, 23                 | about 7        | about 3.4e38  |
| double | 64   | 1, 11, 52                | about 16       | about 1.8e308 |

Here 3.4e38 means 3.4 times 10 to the 38th. Floating point covers a wide range, from the size of an atom to the size of a galaxy, with the same relative precision throughout. It has three consequences that a programmer must keep in mind:

- **Most decimal fractions are not exact.** In binary, one tenth is a repeating fraction, as one third is in decimal, so `0.1 + 0.2` is not exactly `0.3`. Two results that should be equal are compared by testing whether they differ by less than a small amount, not with `=`.
- **Whole numbers are exact only up to a limit.** A double holds every integer up to 2 to the 53rd, about 9 x 10 to the 15th; beyond that, some integers cannot be stored. A single is exact only to about 16 million.
- **Special values** stand for results that are not ordinary numbers: infinity, for a result too large to store, and NaN ("not a number"), for an undefined result such as zero divided by zero.

A processor either has floating-point hardware or performs each operation in software, as a sequence of integer instructions. The processors in the FPGA computers of this book have none, so a floating-point operation takes tens to hundreds of times as long as an integer one. Fixed point is suited to money and to small machines; floating point to measurements and science.

## Text

Text is stored by giving each character a number. The oldest common scheme still in use is **ASCII**, from the 1960s, which assigns the numbers 0 to 127 to the English letters, digits, punctuation and a set of control codes. Capital `A` is 65, lowercase `a` is 97, and the digit `0` is 48. A full table is in [Tables](#tables).

The digit `7` is stored as 55, not 7. The text "42" and the number 42 are different in memory, and a program must convert explicitly between them.

The first 32 ASCII codes are not printable. They control the device the text is sent to: code 10 (line feed) moves to a new line, code 13 (carriage return) moves to the start of the line, code 8 is backspace and code 27 is escape. Unix-like systems end each line of a text file with a line feed alone; MS-DOS, Windows and some network protocols use carriage return followed by line feed. This difference still causes problems when files are moved between systems.

A character's number is not its appearance. A **font** gives each character a **glyph**, the shape that is drawn, so the same text can be shown in many fonts. A computer that has no glyph for a character shows a substitute, often a box or a question mark.

ASCII covers only English. Extensions such as **ISO 8859-15** (Latin-9) use the upper codes, 160 to 255, for accented letters and the euro sign, which is enough for most Western European languages. **Unicode** gives a number to every character in every writing system, with more than a million possible codes.

Unicode text is usually stored as **UTF-8**, an encoding in which ASCII characters stay single bytes with their old values, and every other character takes two to four bytes, each with its top bit set. As a result, a program that handles only ASCII can pass UTF-8 text through without damaging it. UTF-8 is the current standard for text and the appropriate choice unless there is a specific reason to use another encoding.

Text read with the wrong encoding is garbled. The letter "e" with an acute accent is the two bytes `0xC3 0xA9` in UTF-8; read as ISO 8859-15, those bytes appear as two different characters, an "A" with a tilde followed by a copyright sign. The bytes are not damaged, and the text reads correctly again when the right encoding is used. A plain text file does not record its encoding, so it is kept with the file's description, or the file is kept in UTF-8.

## Pictures and Sound

A picture on a screen is a grid of **pixels**. Each pixel is a number that gives its colour. The number of bits per pixel determines how many colours there can be: 1 bit gives two (black and white), 4 bits give 16, 8 bits give 256, and 24 bits give about 16.7 million, eight bits each for red, green and blue.

The memory needed is width times height times bits per pixel. A 640 by 480 screen at 1 bit per pixel needs 307,200 bits, which is 38,400 bytes. The same screen in 24-bit colour needs 921,600 bytes, twenty-four times as much. On a small computer that difference determines what is possible, which is one reason simple machines often use few colours.

Sound is a pressure wave, and it is stored by measuring the wave many times a second. Each measurement is a **sample**. Two numbers describe digital sound: the **sample rate**, how many samples per second, and the sample size. Compact discs use 44,100 samples per second at 16 bits per sample. A higher sample rate can capture higher pitches, and more bits per sample capture quieter detail.

## Units of Size

Sizes are counted in bytes with the usual prefixes, but their meaning has long been ambiguous. Memory comes in powers of two, so a "kilobyte" of memory has traditionally meant 1,024 bytes rather than 1,000. Storage manufacturers and international standards use 1,000.

| Name          | Decimal meaning | Binary name    | Binary meaning  |
|---------------|-----------------|----------------|-----------------|
| kilobyte (KB) | 1,000 bytes     | kibibyte (KiB) | 1,024 bytes     |
| megabyte (MB) | 1,000,000 bytes | mebibyte (MiB) | 1,048,576 bytes |
| gigabyte (GB) | 10 to the 9th   | gibibyte (GiB) | 2 to the 30th   |

In practice, memory sizes such as "32MB of RAM" mean the binary sizes. Context usually makes the meaning clear.

A second ambiguity is between bits and bytes. Memory chips and data rates are often given in bits, written with a lowercase b or "bit". A 64 Kbit memory chip holds 8 KB, and a link of 12 Mbit/s moves at most 1.5 MB each second.

## Meaning Comes From Use

A byte containing `0x41` might be the number 65, the letter A, part of a pixel, part of a sound or part of a processor instruction. Nothing in the byte indicates which. Its meaning comes entirely from how a program uses it.

As a result, the same memory can hold any kind of information, and the same circuits can process all of it. However, a program that misinterprets data, by reading text as a number or running data as instructions, behaves in unintended ways. Much of the care in programming goes into keeping track of what each piece of data means.
