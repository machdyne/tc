# BASIC

BASIC was created in 1964 at Dartmouth College by John Kemeny and Thomas Kurtz, so that students in any subject, not only scientists, could use a computer. Its name stands for Beginner's All-purpose Symbolic Instruction Code. In the late 1970s and 1980s, almost every home computer started with a BASIC prompt, and many people learned to program by typing in listings printed in magazines.

BASIC remains useful. An interpreter fits in a few kilobytes, so it runs on the smallest chips. A program is a short list of numbered lines that is easy to read, and the result of each change is seen at once. This makes it a good first language and a practical one for small machines.

## Machdyne BASIC

There are hundreds of dialects of BASIC. This chapter uses **Machdyne BASIC 1**, which runs on Machdyne's programmable modules and tools, inside Zeitlos, and on ordinary computers. It is deliberately small, because it must fit, together with its own filesystem, in a microcontroller with 16 KB of flash and 2 KB of RAM.

Its main features and limits:

- Programs are numbered lines, stored and run in order of line number.
- There are 26 variables, `A` to `Z`, each holding one number.
- Every number is a 16-bit signed integer, from -32768 to 32767. There are no fractions and no string variables; text appears only in quotes.
- Programs and data are stored as plain text files.
- On hardware with pins, BASIC can read and drive them directly.

Larger BASICs add string variables (written like `N$`), arrays, fractional numbers and many more statements, but the ideas are the same. Machdyne BASIC 1 is also **frozen**: its definition will not change. Later versions may add to it, but must not change the meaning of any BASIC 1 program. A program written for it today is intended to keep its meaning for decades, on whatever machine implements it then.

## Lines and Commands

A line that starts with a number is stored as part of the program. Typing a line with a number that already exists replaces that line, and typing the number alone deletes it. Line numbers are traditionally written in steps of ten, which leaves room to insert lines later.

A line without a number is a **command**, and is carried out at once:

| Command   | Effect                      |
|-----------|-----------------------------|
| RUN       | run the program             |
| LIST      | show the program            |
| NEW       | erase the program           |
| SAVE name | save the program to a file  |
| LOAD name | load a saved program        |
| DIR       | list the files              |
| TYPE name | show the contents of a file |
| DEL name  | delete a file               |

Many BASICs also have an **immediate mode**, in which a statement typed without a line number, such as `PRINT 2 + 2`, runs at once. Machdyne BASIC 1 does not; statements must be placed in numbered lines.

## A First Program

```basic
10 FOR I = 1 TO 5
20 PRINT I; " SQUARED IS "; I * I
30 NEXT I
```

After these lines are typed, `RUN` prints:

```text
1 SQUARED IS 1
2 SQUARED IS 4
3 SQUARED IS 9
4 SQUARED IS 16
5 SQUARED IS 25
```

`FOR` and `NEXT` form a loop: `I` takes the values 1 to 5, and the line between them runs once for each value. `PRINT` shows a mixture of numbers and quoted text, separated by semicolons. A comma in place of a semicolon moves to the next print zone, 14 characters wide, which is useful for tables.

## Numbers and Arithmetic

BASIC uses the operators `+`, `-`, `*` and `/`, and `MOD` for the remainder after division. Multiplication and division are done before addition and subtraction, and parentheses group as in ordinary arithmetic.

Because every number is an integer, division discards the fraction: `7 / 2` is 3. Because numbers are 16 bits, results outside -32768 to 32767 wrap around, as described in [Information](#information). A program that works with large values must scale them, for example by keeping temperatures in tenths of a degree or money in cents, and must check that intermediate results stay in range.

Comparisons, such as `A > B`, give -1 for true and 0 for false. Any value other than 0 counts as true, so a variable that holds 1 or 0 can be used directly as a condition.

## Decisions and Loops

`IF` runs the rest of its line only if a condition is true, and `ELSE` gives an alternative. `GOTO` continues the program at another line. With these and `FOR`, any control flow can be written.

This program prints the prime numbers up to 50, those divisible only by 1 and themselves:

```basic
10 REM PRINT THE PRIME NUMBERS UP TO 50
20 FOR N = 2 TO 50
30 P = 1: D = 2
40 IF D * D > N THEN GOTO 70
50 IF N MOD D = 0 THEN P = 0
60 D = D + 1: GOTO 40
70 IF P THEN PRINT N; " ";
80 NEXT N
90 PRINT
```

```text
2 3 5 7 11 13 17 19 23 29 31 37 41 43 47
```

For each number `N`, the program assumes that it is prime (`P = 1`) and then tries dividing it by each `D` from 2 upward. Divisors come in pairs, and the smaller of a pair cannot exceed the square root of `N`. The search can therefore stop once `D * D` exceeds `N`, which removes most of the work. `REM` starts a remark, a comment for the reader, and a colon separates several statements on one line.

In Machdyne BASIC, the body of a `FOR` loop always runs at least once, even if the loop's end value has already been passed. For this reason the inner loop is built from `IF` and `GOTO` rather than `FOR D = 2 TO N - 1`, which, when N is 2, would still run once with D = 2 and wrongly mark 2 as not prime.

## Subroutines

Lines that perform one task can be made into a **subroutine**. `GOSUB` jumps to it, and `RETURN` continues at the statement after the `GOSUB`:

```basic
10 FOR N = 1 TO 3
20 GOSUB 100
30 NEXT N
40 END
100 REM PRINT A LINE OF N STARS
110 FOR S = 1 TO N
120 PRINT "*";
130 NEXT S
140 PRINT
150 RETURN
```

```text
*
**
***
```

The `END` on line 40 is necessary. Without it, the program would continue into the subroutine after the loop finishes and reach `RETURN` with nowhere to return to.

Because all variables are shared, a subroutine communicates through them: here the main loop sets `N`, and the subroutine reads it. With only 26 variables, it helps to record the purpose of each at the top of the program.

A well-organized BASIC program keeps its main loop short and near the top, and places each subroutine at its own round line number, such as 100, 200 and 300, with a `REM` line describing what it does. `GOTO` can make a program hard to follow, so it is best kept for simple loops and skips, with subroutines used for everything else.

## Input

`INPUT` waits for the user to type a number:

```text
10 INPUT "HOW MANY"; N
```

The quoted prompt is shown first, followed by a question mark. Everything a BASIC program prints and reads, apart from data files, passes through the **console**, which may be a screen and keyboard, a terminal on another computer, or a link over the module bus.

## Files

A program can write and read plain text files. Only one file can be open at a time, as number 1:

```basic
10 PINS -, -, AIN, -
20 OPEN "LOG.TXT" FOR APPEND AS #1
30 PRINT #1, ADC(3)
40 CLOSE #1
50 SLEEP 60
60 GOTO 20
```

About once a minute (`SLEEP` waits a number of seconds), this program reads an analog input and adds the reading as a new line at the end of `LOG.TXT`. Opening a file `FOR OUTPUT` replaces it instead, and opening it `FOR INPUT` allows it to be read with `INPUT #1`. The command `TYPE LOG.TXT` shows the result. Because the file is plain text, any computer can read it later.

On Machdyne's modules, files are stored in F-RAM or EEPROM. The filesystem follows the rules for surviving a power cut described in [Memory and Storage](#memory-and-storage). As a result, a data logger can be switched off at any time without damaging its log; at worst, the line being written is lost.

## Pins

On hardware that has pins, a BASIC program can read and drive them. First, the program declares the purpose of each pin with `PINS`, one mode per pin:

| Mode | Meaning                                          |
|------|--------------------------------------------------|
| -    | not used                                         |
| IN   | digital input                                    |
| PP   | push-pull output                                 |
| OD   | open-drain output                                |
| AIN  | analog input                                     |
| I2C  | the I2C bus (two pins together)                  |
| NET  | left to the system, for the bus that connects it |

`OUT` then sets an output pin high or low, `IN` reads a digital input as 0 or 1, `ADC` reads an analog input as a number from 0 to 1023, and `LED` turns the board's LED on or off. Because pins are declared first, a mistake such as driving a pin declared as an input produces an error message instead of unexpected behaviour.

This program keeps a heater on while a temperature sensor reads low:

```basic
10 REM KEEP A HEATER ON WHILE IT IS COLD
20 PINS -, -, AIN, PP
30 T = ADC(3)
40 IF T < 400 THEN OUT 4, 1 ELSE OUT 4, 0
50 REG 0, T / 4
60 WAIT 1000
70 GOTO 30
```

`WAIT` pauses for a number of milliseconds, so the loop runs about once a second. The program follows the pattern of nearly every control program: **read, decide, act, wait, repeat**. Pin 3 reads the sensor, and pin 4 switches the heater through a transistor or relay, as described in [Talking to the World](#talking-to-the-world).

A practical controller would improve on this in one respect. When the temperature stays close to the threshold, the heater switches on and off every second, which wears out relays. The usual remedy is **hysteresis**: the heater switches on below one value and off only above a slightly higher one, so that small fluctuations have no effect.

I2C devices are reached with the statement `I2C`, which writes to a device, and the function `I2CR`, which reads from one. This program reads the temperature sensor connected in [Talking to the World](#talking-to-the-world), at address 72, once a second:

```basic
10 REM READ AN I2C TEMPERATURE SENSOR
20 PINS NET, NET, I2C, I2C
30 T = I2CR(72, 0)
40 IF T = -1 THEN PRINT "NO SENSOR": END
50 IF T > 127 THEN T = T - 256
60 PRINT T; " C"
70 WAIT 1000
80 GOTO 30
```

`I2CR` gives -1 when no device answers, which line 40 reports instead of printing a wrong temperature. Line 50 converts the byte from two's complement into a negative number.

## Talking to a Host

Line 50 of the heater program stores a value in **program register** 0. A program has sixteen registers, `REG 0` to `REG 15`, each holding one byte. They are shared with the system the program runs in. On a module, a host computer on the bus can read and write them while the program runs. In this example, the host can read the latest reading, divided by four to fit in a byte, at any time without stopping the program, and could pass in a new threshold, scaled the same way, through another register.

## Starting by Itself

A program saved as `BOOT` (stored as `BOOT.BAS`) runs automatically when the machine starts. This turns a module into a dedicated controller: once programmed and installed, it performs its task every time it is powered, with or without a computer attached. The boot window described in [Talking to the World](#talking-to-the-world) ensures that a faulty `BOOT` program cannot lock the host out.

## One Language, Many Machines

The definition of Machdyne BASIC states what a program means; each machine determines which hardware it provides. A program that only computes and prints runs the same everywhere. A program that uses pins runs wherever those pins exist, and on a machine without them it stops with `NOT SUPPORTED` rather than behaving unexpectedly.

Machines may also add statements of their own. A BASIC with a screen may add drawing statements such as `PLOT`, `LINE` and `CIRCLE`, as the home computers did, and programs that use them run only where those statements exist.

As a result, a program can be written and tested on a full computer, within the limits of the module it is intended for, and then sent to a small module, where it behaves the same way.
