# Language Reference

This appendix summarizes the three programming languages and the hardware description language used in this book. Each summary covers the language as it is defined by its standard or reference document, which changes rarely or not at all, and leaves out the libraries and interfaces of particular systems, which change often.

## Machdyne BASIC 1

Machdyne BASIC 1 is frozen: later versions may add to it but must not change the meaning of any BASIC 1 program. Every value is a 16-bit signed integer, from -32768 to 32767, and arithmetic wraps around at those limits. The variables are the 26 letters `A` to `Z`.

### BASIC Statements

| Statement                | Effect                                    |
|--------------------------|-------------------------------------------|
| LET v = e, or v = e      | assign the value of e to variable v       |
| PRINT items              | print; a semicolon joins, a comma tabs    |
| INPUT v, INPUT "text"; v | read a number from the console            |
| IF e THEN ... ELSE ...   | run the rest of the line if e is not 0    |
| GOTO n                   | continue at line n                        |
| GOSUB n, RETURN          | call a subroutine at line n, and return   |
| FOR v = a TO b STEP s    | start a loop; the body runs at least once |
| NEXT v                   | end of the loop body                      |
| END                      | stop the program                          |
| REM text                 | a comment, to the end of the line         |
| SLEEP e                  | wait e seconds                            |
| WAIT e                   | wait e milliseconds                       |
| PINS m, m, m, m          | declare the use of pins 1 to 4            |
| OUT p, e                 | set output pin p low (0) or high (not 0)  |
| LED e                    | turn the LED off (0) or on (not 0)        |
| I2C a, v                 | write byte v to I2C device a              |
| I2C a, r, v              | write byte v to register r of device a    |
| REG n, e                 | set program register n (0 to 15)          |
| OPEN "f" FOR m AS #1     | open file f for INPUT, OUTPUT or APPEND   |
| PRINT #1, items          | write to the open file                    |
| INPUT #1, v              | read the next number from the open file   |
| CLOSE #1                 | close the open file                       |

A colon separates several statements on one line.

### BASIC Limits

Every implementation provides at least these:

| Limit              | At least               |
|--------------------|------------------------|
| program memory     | 1,024 bytes, tokenized |
| elements per line  | 64                     |
| active FOR loops   | 6                      |
| active GOSUB calls | 8                      |
| variables          | 26, A to Z             |
| program registers  | 16, each 0 to 255      |
| open files         | 1                      |

### BASIC Functions

| Function   | Value                                              |
|------------|----------------------------------------------------|
| IN(p)      | digital pin p, 0 or 1                              |
| ADC(p)     | analog input p, 0 to 1023                          |
| I2CR(a)    | a byte from I2C device a; -1 if it does not answer |
| I2CR(a, r) | a byte from register r of I2C device a             |
| REG(n)     | program register n, 0 to 255                       |
| EOF(1)     | -1 at the end of the open input file, otherwise 0  |

### BASIC Operators

From highest to lowest precedence. Operators of equal precedence are evaluated from left to right.

| Precedence | Operators         | Meaning                       |
|------------|-------------------|-------------------------------|
| 1          | -                 | negation                      |
| 2          | * / MOD           | multiply, divide, remainder   |
| 3          | + -               | add, subtract                 |
| 4          | = == <> < > <= >= | comparisons: -1 true, 0 false |
| 5          | NOT               | bitwise not                   |
| 6          | AND               | bitwise and                   |
| 7          | OR                | bitwise or                    |

Division truncates towards zero, so `-7 / 2` is -3. `MOD` takes the sign of its left operand.

### BASIC Pin Modes

| Mode | Meaning                                  | Pins    |
|------|------------------------------------------|---------|
| -    | not used                                 | any     |
| IN   | digital input                            | any     |
| PP   | push-pull output                         | any     |
| OD   | open-drain output                        | any     |
| AIN  | analog input                             | 3, 4    |
| I2C  | I2C bus: 3 is the clock, 4 the data      | 3 and 4 |
| UART | reserved for a later version             | 3 and 4 |
| NET  | left to the system, for the bus it is on | 1 and 2 |

`RUN` starts every program with the declaration `PINS NET, NET, -, -`.

### BASIC Commands

| Command    | Effect                               |
|------------|--------------------------------------|
| RUN        | run the program from its lowest line |
| LIST       | show the program                     |
| NEW        | erase the program                    |
| SAVE name  | save the program as a text file      |
| LOAD name  | replace the program with a saved one |
| TYPE name  | show the contents of a file          |
| DIR        | list the files                       |
| DEL name   | delete a file                        |
| FORMAT YES | erase all files                      |
| HELP       | list the commands and keywords       |

File names have up to eight letters, digits, `_` or `-`, and an optional extension of up to three; a name without an extension is given `.BAS`. A system that starts a program by itself runs `BOOT.BAS`. Ctrl+C stops a running program.

### BASIC Error Messages

| Message             | Cause                                 |
|---------------------|---------------------------------------|
| SYNTAX ERROR        | not a valid line or command           |
| TOO LONG            | too many elements in a line           |
| TOO BIG             | a number above 32767                  |
| NO LINE             | a jump to a missing line              |
| DIV BY 0            | division or MOD by zero               |
| NO MEMORY           | the program does not fit              |
| NO FOR, NO GOSUB    | NEXT or RETURN without its start      |
| TOO DEEP            | too many loops or calls active        |
| PIN NOT DECLARED    | a use that PINS did not declare       |
| BAD PINS, ON A BUS  | a pin declaration or use not allowed  |
| OUT OF RANGE        | a pin or register number out of range |
| I2C ERROR           | an I2C device did not answer          |
| BAD NAME, NOT FOUND | an invalid or missing file name       |
| DISK FULL, DIR FULL | no room for the file                  |
| BAD FILE #          | a file number other than 1            |
| FILE OPEN, NOT OPEN | a file is open, or none is            |
| END OF FILE         | reading past the end of the file      |
| NOT FORMATTED       | the storage is not formatted          |
| DAMAGED, I/O ERROR  | the storage cannot be read            |
| NOT SUPPORTED       | the hardware is not present           |
| BREAK               | stopped with Ctrl+C                   |

## Scheme Reference

The Scheme in this book follows the Revised(4) Report on the Algorithmic Language Scheme (R4RS). Machdyne Scheme implements a documented subset of it. It leaves out hygienic macros, continuations that can be resumed after they have returned, separate exact and inexact numbers (all numbers are floating point), and the procedures for ports and files, which each system provides in its own way. The tables list the standard forms and procedures that it implements.

### Scheme Special Forms

```text
(quote x)  'x                  x itself, not evaluated
(lambda (args) body)           a new procedure
(define name value)            give a name to a value
(define (name args) body)      define a procedure
(set! name value)              change the value of a variable
(if test then else)            choose one of two expressions
(cond (test e ...) ...         the first clause whose test is
      (else e ...))              true
(case key ((v ...) e ...) ...) the clause that lists key
(and e ...)  (or e ...)        stop at the first false, or the
                                 first true, value
(begin e ...)                  in order; the value of the last
(let ((name value) ...) body)  local names, bound together
(let* ...)                     bound one after another
(letrec ...)                   bound for mutual recursion
(let loop ((var init) ...)     named let: a loop that calls
  body)                          loop to repeat
(do ((var init step) ...)      an iteration that ends when
    (test result) body)          test is true
(delay e)                      a promise, run by force
`x  ,x  ,@x                    quasiquote, unquote, splice
```

### Scheme Standard Procedures

| Kind       | Procedures                                               |
|------------|----------------------------------------------------------|
| equality   | eq? eqv? equal? not                                      |
| types      | boolean? symbol? number? char? string? vector? pair?     |
|            | null? procedure? list?                                   |
| pairs      | cons car cdr set-car! set-cdr! caar cadr ... cddddr      |
| lists      | list length append reverse list-tail list-ref memq memv  |
|            | member assq assv assoc map for-each                      |
| numbers    | + - * / = < > <= >= zero? positive? negative? odd? even? |
|            | max min abs quotient remainder modulo gcd lcm floor      |
|            | ceiling truncate round sqrt expt                         |
|            | number->string string->number                            |
| characters | char=? char<? char>? char<=? char>=? char-alphabetic?    |
|            | char-numeric? char-whitespace? char-upper-case?          |
|            | char-lower-case? char->integer integer->char             |
|            | char-upcase char-downcase                                |
| strings    | make-string string string-length string-ref string-set!  |
|            | string=? string<? string>? string<=? string>=? substring |
|            | string-append string-copy string-fill!                   |
|            | string->symbol symbol->string                            |
| vectors    | make-vector vector vector-length vector-ref vector-set!  |
|            | vector->list list->vector vector-fill!                   |
| control    | apply force call-with-current-continuation (call/cc)     |
| in and out | display write read                                       |

Machdyne Scheme also provides `dynamic-wind` and `eval`, which were added to the standard in its next revision, R5RS.

Only `#f` is false. Procedures whose names end in `?` return true or false, and those whose names end in `!` change data in place.

## C Reference

The C in this book follows the 1999 standard, C99.

### C Keywords

C99 has 37 reserved words:

```text
auto       break      case       char       const      continue
default    do         double     else       enum       extern
float      for        goto       if         inline     int
long       register   restrict   return     short      signed
sizeof     static     struct     switch     typedef    union
unsigned   void       volatile   while      _Bool      _Complex
_Imaginary
```

### C Operators

From highest to lowest precedence. Operators on the same line have equal precedence; the last column gives the order in which a chain of them is grouped.

```text
()  []  ->  .  x++  x--          call, index, member     left
++x --x  +  -  !  ~  *  &        prefix, unary           right
  sizeof  (type)                 size, cast              right
*  /  %                          multiply, divide        left
+  -                             add, subtract           left
<<  >>                           shift                   left
<  <=  >  >=                     compare                 left
==  !=                           equal, not equal        left
&                                bitwise and             left
^                                bitwise exclusive or    left
|                                bitwise or              left
&&                               logical and             left
||                               logical or              left
?:                               conditional             right
=  +=  -=  *=  /=  %=            assignment              right
  <<=  >>=  &=  ^=  |=
,                                sequence                left
```

Two rules prevent many mistakes: `&`, `^` and `|` bind more loosely than `==`, so `(flags & MASK) == 0` needs its parentheses; and `=` assigns while `==` compares.

### C Standard Headers

| Header    | Provides                                         |
|-----------|--------------------------------------------------|
| stdio.h   | input and output: printf, scanf, fopen, fgets    |
| stdlib.h  | malloc, free, exit, atoi, strtol, qsort, abs     |
| string.h  | strlen, strcmp, strcpy, memcpy, memset           |
| ctype.h   | isdigit, isalpha, isspace, toupper               |
| math.h    | sqrt, sin, cos, pow, floor                       |
| stdint.h  | exact-width integers: uint8_t, int16_t, uint32_t |
| stdbool.h | bool, true, false                                |
| stddef.h  | size_t, NULL, offsetof                           |
| limits.h  | INT_MAX, CHAR_BIT and other limits               |
| assert.h  | assert                                           |
| time.h    | time, clock                                      |

### printf Conversions

| Conversion | Prints                  | Example           | Output  |
|------------|-------------------------|-------------------|---------|
| %d         | a signed integer        | ("%d", -42)       | -42     |
| %u         | an unsigned integer     | ("%u", 42u)       | 42      |
| %x, %X     | hexadecimal             | ("%x", 255)       | ff      |
| %o         | octal                   | ("%o", 8)         | 10      |
| %c         | a character             | ("%c", 65)        | A       |
| %s         | a string                | ("%s", "hi")      | hi      |
| %f         | a floating-point number | ("%.2f", 3.14159) | 3.14    |
| %p         | a pointer               | ("%p", ptr)       | address |
| %%         | a percent sign          | ("%%")            | %       |

A number between `%` and the letter sets a minimum width, `0` pads with zeros, and `.n` sets the precision: `%04X` prints 255 as `00FF`.

### C Escape Sequences

```text
\n    line feed               \\    backslash
\r    carriage return         \'    single quote
\t    tab                     \"    double quote
\0    the zero byte           \x41  the byte 0x41, "A"
```

## Verilog Reference

The Verilog in this book follows the 2005 standard, IEEE 1364-2005, and uses only the parts that can be synthesized into hardware, together with those needed for testbenches.

### Verilog Constructs

| Construct                          | Meaning                             |
|------------------------------------|-------------------------------------|
| module name (ports); ... endmodule | a unit of design                    |
| input, output, inout               | port directions                     |
| wire, reg                          | a connection; a value set in always |
| [7:0]                              | an 8-bit vector, bit 7 the highest  |
| parameter, localparam              | a constant, settable or local       |
| assign w = expr;                   | combinational logic                 |
| always @(posedge clk)              | logic clocked on the rising edge    |
| always @*                          | combinational logic in a block      |
| begin ... end                      | group statements                    |
| if ... else, case ... endcase      | choices inside an always block      |
| <=                                 | non-blocking: for clocked logic     |
| =                                  | blocking: for combinational logic   |
| initial                            | testbench code, run once at start   |
| #n                                 | in a testbench, wait n time units   |
| $display, $finish                  | in a testbench, print and stop      |

### Verilog Numbers and Operators

```text
8'd200  4'b1010  16'hFF   width, base (d, b, h, o), value
{a, b}                    concatenation
{4{a}}                    repetition: a four times
x[3]  x[7:4]              a bit, a range of bits
&  |  ^  ~                bitwise and, or, exclusive or, not
&&  ||  !                 logical and, or, not
&x  |x  ^x                reduction: and, or, xor of all bits
==  !=  <  >  <=  >=      comparisons
+  -  *  <<  >>           arithmetic and shifts
c ? a : b                 choice: a multiplexer
```
