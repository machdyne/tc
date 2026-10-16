# Three Languages Side by Side

This appendix shows four small programs, each written in BASIC, Scheme and C. Each version computes the same result, and the differences show how each language expresses repetition, choice and functions. All of the programs fit within the 16-bit integers of Machdyne BASIC.

## Greatest Common Divisor

Euclid's algorithm from [Thinking in Programs](#thinking-in-programs) finds the greatest common divisor of 1071 and 462, which is 21.

BASIC, with a loop built from `IF` and `GOTO`:

```basic
10 A = 1071: B = 462
20 IF B = 0 THEN GOTO 60
30 T = A MOD B
40 A = B: B = T
50 GOTO 20
60 PRINT A
```

Scheme, as a recursive function. The recursive call is a tail call, so it runs as a loop:

```scheme
(define (gcd-of a b)
  (if (= b 0)
      a
      (gcd-of b (remainder a b))))

(gcd-of 1071 462)             ; => 21
```

C, with a `while` loop:

```c
int gcd(int a, int b)
{
    while (b != 0) {
        int t = a % b;
        a = b;
        b = t;
    }
    return a;
}
```

## Factorial

The factorial of 7, written 7!, is 1 x 2 x 3 x 4 x 5 x 6 x 7 = 5040. It is the largest factorial that fits in a 16-bit signed integer: 8! is 40320.

BASIC, multiplying in a `FOR` loop:

```basic
10 F = 1
20 FOR I = 1 TO 7
30 F = F * I
40 NEXT I
50 PRINT F
```

Scheme, following the definition directly: the factorial of 0 is 1, and the factorial of n is n times the factorial of n - 1. The multiplication happens after the recursive call returns, so this is not a tail call, and each call uses stack space.

```scheme
(define (factorial n)
  (if (= n 0)
      1
      (* n (factorial (- n 1)))))

(factorial 7)                 ; => 5040
```

C, with a `for` loop:

```c
int factorial(int n)
{
    int f = 1;
    for (int i = 1; i <= n; i++)
        f *= i;
    return f;
}
```

## A Conversion Table

A table of temperatures from 0 to 100 degrees Celsius in steps of 20, with their equivalents in Fahrenheit: F = C x 9 / 5 + 32. Each version prints six rows of two numbers, from 0 and 32 to 100 and 212; BASIC places the second number in the next print zone.

BASIC, where `STEP` sets the increment and the comma moves to the next print zone:

```basic
10 FOR C = 0 TO 100 STEP 20
20 PRINT C, C * 9 / 5 + 32
30 NEXT C
```

Scheme, with a procedure that prints one row and then calls itself for the next:

```scheme
(define (table c)
  (if (<= c 100)
      (begin
        (display c)
        (display " ")
        (display (+ (/ (* c 9) 5) 32))
        (display "\n")
        (table (+ c 20)))))

(table 0)
```

C, with `printf`, where each `%d` is replaced by the next number:

```c
    for (int c = 0; c <= 100; c += 20)
        printf("%d %d\n", c, c * 9 / 5 + 32);
```

In BASIC and C, the multiplication is done before the division, so the integer division loses nothing. Written as `C / 5 * 9`, the result would be rounded down for any value of C that is not a multiple of 5.

## The Collatz Sequence

The sequence starts from a number. An even number is halved; an odd one is multiplied by 3 and increased by 1. This repeats until the number is 1. Every starting number ever tried reaches 1 eventually, although no one has proved that all of them do. Starting from 27, it takes 111 steps, and the number rises as high as 9232 on the way.

BASIC, with a decision inside the loop:

```basic
10 N = 27: S = 0
20 IF N = 1 THEN GOTO 60
30 IF N MOD 2 = 0 THEN N = N / 2 ELSE N = 3 * N + 1
40 S = S + 1
50 GOTO 20
60 PRINT S
```

Scheme, with `cond` choosing among three cases, and the step count carried as an argument:

```scheme
(define (collatz n steps)
  (cond ((= n 1) steps)
        ((even? n) (collatz (/ n 2) (+ steps 1)))
        (else (collatz (+ (* 3 n) 1) (+ steps 1)))))

(collatz 27 0)                ; => 111
```

C, with `if` and `else` inside a `while` loop:

```c
int collatz(int n)
{
    int steps = 0;
    while (n != 1) {
        if (n % 2 == 0)
            n = n / 2;
        else
            n = 3 * n + 1;
        steps++;
    }
    return steps;
}
```

## Common Constructs

| Construct  | BASIC             | Scheme                 | C                |
|------------|-------------------|------------------------|------------------|
| comment    | REM note          | ; note                 | /* note */       |
| assign     | A = 5             | (set! a 5)             | a = 5;           |
| arithmetic | A * (B + 1)       | (* a (+ b 1))          | a * (b + 1)      |
| remainder  | A MOD B           | (remainder a b)        | a % b            |
| equality   | A = B             | (= a b)                | a == b           |
| choice     | IF A > 0 THEN ... | (if (> a 0) x y)       | if (a > 0) ...   |
| loop       | FOR I = 1 TO 10   | (let loop ((i 1)) ...) | for (i = 1; ...) |
| function   | GOSUB 100         | (define (f x) ...)     | int f(int x)     |
| output     | PRINT A           | (display a)            | printf("%d", a); |
| truth      | -1, 0             | #t, #f                 | non-zero, 0      |
