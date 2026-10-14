# Three Languages Side by Side

Euclid's algorithm from [Thinking in Programs](#thinking-in-programs), finding the greatest common divisor of 1071 and 462, written in each of the three languages. Each prints or returns 21.

BASIC, with a loop built from `IF` and `GOTO`:

```basic
10 A = 1071: B = 462
20 IF B = 0 THEN GOTO 60
30 T = A MOD B
40 A = B: B = T
50 GOTO 20
60 PRINT A
```

Scheme, as a recursive function. The recursive call is a tail call, so this runs as a loop:

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
