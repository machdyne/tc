# Tables

## ASCII Characters

The ASCII characters from 32 to 127, with their codes in decimal and hexadecimal. Codes 32 to 126 are printable; 127, DEL, is a control character. Capital and lowercase letters differ by exactly 32 (hex `20`), a single bit, and the digit characters `0` to `9` are 48 to 57, so subtracting 48 from a digit's code gives its value.

```text
Dec  Hex  Char   Dec  Hex  Char   Dec  Hex  Char   Dec  Hex  Char
 32   20  space   56   38  8       80   50  P      104   68  h
 33   21  !       57   39  9       81   51  Q      105   69  i
 34   22  "       58   3A  :       82   52  R      106   6A  j
 35   23  #       59   3B  ;       83   53  S      107   6B  k
 36   24  $       60   3C  <       84   54  T      108   6C  l
 37   25  %       61   3D  =       85   55  U      109   6D  m
 38   26  &       62   3E  >       86   56  V      110   6E  n
 39   27  '       63   3F  ?       87   57  W      111   6F  o
 40   28  (       64   40  @       88   58  X      112   70  p
 41   29  )       65   41  A       89   59  Y      113   71  q
 42   2A  *       66   42  B       90   5A  Z      114   72  r
 43   2B  +       67   43  C       91   5B  [      115   73  s
 44   2C  ,       68   44  D       92   5C  \      116   74  t
 45   2D  -       69   45  E       93   5D  ]      117   75  u
 46   2E  .       70   46  F       94   5E  ^      118   76  v
 47   2F  /       71   47  G       95   5F  _      119   77  w
 48   30  0       72   48  H       96   60  `      120   78  x
 49   31  1       73   49  I       97   61  a      121   79  y
 50   32  2       74   4A  J       98   62  b      122   7A  z
 51   33  3       75   4B  K       99   63  c      123   7B  {
 52   34  4       76   4C  L      100   64  d      124   7C  |
 53   35  5       77   4D  M      101   65  e      125   7D  }
 54   36  6       78   4E  N      102   66  f      126   7E  ~
 55   37  7       79   4F  O      103   67  g      127   7F  DEL
```

## Control Characters

The codes below 32 control a terminal or printer instead of printing. These are the ones still in common use:

| Dec | Hex | Name | Keyboard      | Use                              |
|-----|-----|------|---------------|----------------------------------|
| 0   | 00  | NUL  |               | ends a string in C               |
| 3   | 03  | ETX  | Ctrl+C        | interrupt a running program      |
| 4   | 04  | EOT  | Ctrl+D        | end of input                     |
| 7   | 07  | BEL  | Ctrl+G        | sound the bell                   |
| 8   | 08  | BS   | Ctrl+H        | backspace                        |
| 9   | 09  | HT   | Ctrl+I, Tab   | horizontal tab                   |
| 10  | 0A  | LF   | Ctrl+J        | line feed: new line              |
| 13  | 0D  | CR   | Ctrl+M, Enter | carriage return                  |
| 27  | 1B  | ESC  | Esc           | starts terminal escape sequences |

## Powers of Two

| n   | 2 to the n    | Common name            |
|-----|---------------|------------------------|
| 4   | 16            | values in a nibble     |
| 8   | 256           | values in a byte       |
| 10  | 1,024         | 1 KiB                  |
| 12  | 4,096         | a common flash sector  |
| 16  | 65,536        | 64 KiB; 16-bit values  |
| 20  | 1,048,576     | 1 MiB                  |
| 24  | 16,777,216    | 16 MiB; 24-bit colours |
| 30  | 1,073,741,824 | 1 GiB                  |
| 32  | 4,294,967,296 | 4 GiB; 32-bit values   |

## Unit Prefixes

| Prefix | Symbol | Factor        | Example                         |
|--------|--------|---------------|---------------------------------|
| giga   | G      | 1,000,000,000 | 1 GHz processor clock           |
| mega   | M      | 1,000,000     | 48 MHz                          |
| kilo   | k      | 1,000         | 10k resistor                    |
| milli  | m      | 0.001         | 5 mA through an LED             |
| micro  | u      | 0.000001      | 10 uA in sleep                  |
| nano   | n      | 0.000000001   | 21 ns per clock cycle at 48 MHz |

The proper symbol for micro is the Greek letter mu; a plain u is the usual substitute where it cannot be typed.

## Electrical Formulas

```text
V = I x R              Ohm's law: volts = amps x ohms
P = V x I              power: watts = volts x amps
E = P x t              energy: watt-hours = watts x hours
R = (Vsupply - Vled) / I     series resistor for an LED
f = 1 / T              frequency = 1 / period
```

## Resistor Colour Code

Small resistors are marked with coloured bands. On a four-band resistor, the first two bands are digits, the third is the number of zeros to add, and the fourth, set apart from the others, is the tolerance.

| Colour | Digit | Multiplier | Tolerance |
|--------|-------|------------|-----------|
| black  | 0     | 1          |           |
| brown  | 1     | 10         | 1%        |
| red    | 2     | 100        | 2%        |
| orange | 3     | 1k         |           |
| yellow | 4     | 10k        |           |
| green  | 5     | 100k       | 0.5%      |
| blue   | 6     | 1M         | 0.25%     |
| violet | 7     | 10M        | 0.1%      |
| grey   | 8     |            |           |
| white  | 9     |            |           |
| gold   |       | 0.1        | 5%        |
| silver |       | 0.01       | 10%       |

Red, violet, brown and gold is 2, 7 and one zero: 270 ohms, within 5%. A five-band resistor has three digits before the multiplier.

## Surface-Mount Markings

Surface-mount resistors are too small for colour bands and are marked with a short code:

| Marking | Rule                                        | Value    |
|---------|---------------------------------------------|----------|
| 472     | two digits, then the number of zeros        | 4.7k     |
| 103     |                                             | 10k      |
| 100     |                                             | 10 ohms  |
| 4701    | three digits, then the number of zeros (1%) | 4.7k     |
| 4R7     | R marks the decimal point                   | 4.7 ohms |
| R10     |                                             | 0.1 ohm  |
| 01C     | EIA-96: an E96 value number and a letter    | 10k      |
| 0, 000  | a zero-ohm link, used as a jumper           | 0        |

In the EIA-96 code, used on the smallest 1% resistors, the two digits number the 96 values of the E96 series, from 01 for 100 to 96 for 976, and the letter is a multiplier: Z 0.001, Y or R 0.01, X or S 0.1, A 1, B or H 10, C 100, D 1,000, E 10,000 and F 100,000. A table of the E96 series is needed to decode the number; 01C is 100 x 100.

Capacitors that are marked use three digits in picofarads, the third again the number of zeros: 104 is 100,000 pF, or 100 nF, and 105 is 1 uF. Small ceramic capacitors are usually not marked at all, and are measured or identified from the board's documentation. On a diode, the band marks the cathode; on a tantalum capacitor, the band marks the positive end. On a chip, a dot or notch marks pin 1, and the short code printed on top is explained in the marking section of its data sheet.

## Standard Resistor Values

Resistors are made in series of values spaced so that each is a fixed ratio above the last. The E12 series, for 10% tolerance, has twelve values in each decade:

```text
10   12   15   18   22   27   33   39   47   56   68   82
```

The same values repeat in every decade: 2.7 ohms, 27 ohms, 270 ohms, 2.7k, 27k and so on. The E24 series adds a value between each pair, for 5% tolerance.

## Logic Level Thresholds

A digital input reads a voltage as 0 or 1 only when it is clearly low or clearly high; in between, the result is not defined. Typical limits for the common logic families:

| Family       | Supply | Low input at most | High input at least |
|--------------|--------|-------------------|---------------------|
| 5 V CMOS     | 5.0 V  | 1.5 V             | 3.5 V               |
| 5 V TTL      | 5.0 V  | 0.8 V             | 2.0 V               |
| 3.3 V LVCMOS | 3.3 V  | 0.8 V             | 2.0 V               |
| 2.5 V LVCMOS | 2.5 V  | 0.7 V             | 1.7 V               |
| 1.8 V LVCMOS | 1.8 V  | 0.63 V            | 1.17 V              |

A 3.3 V output drives a 5 V TTL input correctly, but not always a 5 V CMOS input. A 5 V output connected to a 3.3 V input can damage it unless the input is specified as 5 V tolerant. The data sheet of each part gives its exact limits.

