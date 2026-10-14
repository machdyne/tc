# Tables

## ASCII Characters

The ASCII characters from 32 to 127, with their codes in decimal and hexadecimal. Codes 32 to 126 are printable; 127, DEL, is a control character. Capital and lowercase letters differ by exactly 32 (hex `20`), a single bit, and the digit characters `0` to `9` are 48 to 57, so subtracting 48 from a digit's code gives its value.

```text
Dec  Hex  Char    Dec  Hex  Char    Dec  Hex  Char    Dec  Hex  Char
 32   20  space    56   38  8        80   50  P       104   68  h
 33   21  !        57   39  9        81   51  Q       105   69  i
 34   22  "        58   3A  :        82   52  R       106   6A  j
 35   23  #        59   3B  ;        83   53  S       107   6B  k
 36   24  $        60   3C  <        84   54  T       108   6C  l
 37   25  %        61   3D  =        85   55  U       109   6D  m
 38   26  &        62   3E  >        86   56  V       110   6E  n
 39   27  '        63   3F  ?        87   57  W       111   6F  o
 40   28  (        64   40  @        88   58  X       112   70  p
 41   29  )        65   41  A        89   59  Y       113   71  q
 42   2A  *        66   42  B        90   5A  Z       114   72  r
 43   2B  +        67   43  C        91   5B  [       115   73  s
 44   2C  ,        68   44  D        92   5C  \       116   74  t
 45   2D  -        69   45  E        93   5D  ]       117   75  u
 46   2E  .        70   46  F        94   5E  ^       118   76  v
 47   2F  /        71   47  G        95   5F  _       119   77  w
 48   30  0        72   48  H        96   60  `       120   78  x
 49   31  1        73   49  I        97   61  a       121   79  y
 50   32  2        74   4A  J        98   62  b       122   7A  z
 51   33  3        75   4B  K        99   63  c       123   7B  {
 52   34  4        76   4C  L       100   64  d       124   7C  |
 53   35  5        77   4D  M       101   65  e       125   7D  }
 54   36  6        78   4E  N       102   66  f       126   7E  ~
 55   37  7        79   4F  O       103   67  g       127   7F  DEL
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
