# Scheme

Lisp was invented by John McCarthy in 1958, and is one of the two oldest programming languages still in use. Scheme is a small dialect of Lisp, created at MIT in 1975 by Guy Steele and Gerald Sussman. Its complete definition fits in about fifty pages, and it has been used for decades to teach the foundations of computer science.

Scheme programs are built from a few ideas combined freely: expressions, functions and lists. Learning it teaches a way of thinking about programs, including how a programming language itself works.

## Machdyne Scheme

The Scheme in this chapter is Machdyne Scheme, a small interpreter that runs inside Zeitlos and on ordinary computers. It implements most of R4RS, the Revised(4) Report on the Algorithmic Language Scheme of 1991, the standard version of the language at that time. It omits a few advanced features that are difficult to fit on a small machine, and the standard procedures for files, which each system provides in its own way. All its numbers are floating point. Everything in this chapter is standard Scheme and works in any implementation.

## Expressions

Every part of a Scheme program is an **expression**, and every compound expression is written in the same way: in parentheses, with the operation first and its arguments after it.

```text
(+ 1 2)               3
(* 6 7)               42
(+ 1 (* 2 3))         7
(- 10 (/ 8 2))        6
```

This **prefix notation** has two advantages. There are no precedence rules, because the parentheses state exactly what is grouped with what. In addition, operations can take any number of arguments: `(+ 1 2 3 4)` is 10.

Scheme is normally used through a REPL, the read-eval-print loop described in [Operating Systems](#operating-systems). In this chapter, `; =>` marks the value an expression produces. Everything from a semicolon to the end of the line is a comment.

## Definitions

`define` gives a name to a value or to a function:

```scheme
(define (square x) (* x x))
(square 12)                   ; => 144
```

This reads as: to compute the square of `x`, multiply `x` by `x`. Once defined, `square` is used in the same way as the built-in operations.

## Choices

`if` takes a test, an expression for when the test is true, and one for when it is false. `cond` checks a series of tests in order and uses the first that is true:

```scheme
(define (size n)
  (cond ((< n 10) 'small)
        ((< n 100) 'medium)
        (else 'large)))
(size 42)                     ; => medium
```

The values `'small`, `'medium` and `'large` are **symbols**: names used as data, an alternative to strings or numeric codes. The quote mark means "this name itself, not the value it stands for".

The true and false values are written `#t` and `#f`. In Scheme only `#f` counts as false; zero, the empty list and the empty string all count as true.

## Numbers

Standard Scheme distinguishes exact numbers, such as integers and fractions, from inexact ones. In Machdyne Scheme every number is a floating-point double, as described in [Information](#information). Whole numbers are exact up to 2 to the 53rd, which is enough for counting and for most arithmetic on integers, but division produces fractions, and fractions are approximate:

```scheme
(/ 7 2)                       ; => 3.5
(quotient 7 2)                ; => 3
(= (+ 0.1 0.2) 0.3)           ; => #f

(define (close? a b)
  (< (abs (- a b)) 0.000001))
(close? (+ 0.1 0.2) 0.3)      ; => #t
```

`quotient` and `remainder` divide whole numbers as BASIC and C do. Two results that should be equal are compared by testing whether they are close, as `close?` does, rather than with `=`.

## Recursion

Scheme has no statement for loops. Repetition is written as **recursion**, in which a function calls itself:

```scheme
(define (factorial n)
  (if (= n 0)
      1
      (* n (factorial (- n 1)))))
(factorial 10)                ; => 3628800
```

The definition states what a factorial is: 1 for zero, and otherwise n times the factorial of n - 1. Its evaluation can be followed by replacing each call with its definition:

```text
(factorial 3)
(* 3 (factorial 2))
(* 3 (* 2 (factorial 1)))
(* 3 (* 2 (* 1 (factorial 0))))
(* 3 (* 2 (* 1 1)))
6
```

Each pending multiplication must be remembered until the innermost call returns, so this function uses stack space in proportion to `n`.

## Tail Calls

When the recursive call is the last action of a function, nothing needs to be remembered, and the call can reuse the current stack frame. Scheme guarantees this: such a **tail call** runs in constant space, and is therefore as efficient as a loop. A loop is usually written with a **named let**, which defines a local function and calls it immediately:

```scheme
(define (sum-to n)
  (let loop ((i 1) (total 0))
    (if (> i n)
        total
        (loop (+ i 1) (+ total i)))))
(sum-to 100)                  ; => 5050
```

`loop` starts with `i` as 1 and `total` as 0. Each call to `loop` is a tail call that carries the new values forward, so the computation can repeat a million times without growing the stack. The variables that would change in a loop in another language are here the arguments of the next call.

## Lists

The **list** is the central data structure of Lisp, whose name comes from "list processing". A list is written in parentheses and quoted, so that Scheme treats it as data rather than as an expression to evaluate:

```scheme
(define days '(mon tue wed thu fri))
(car days)                    ; => mon
(cdr days)                    ; => (tue wed thu fri)
(cons 'sun days)              ; => (sun mon tue wed thu fri)
```

Three operations do most of the work:

- `car` gives the first item of a list.
- `cdr` gives the rest of the list, everything after the first item.
- `cons` builds a new list with one item added at the front.

The names come from two parts of a machine word on the IBM 704, the computer on which Lisp was first implemented.

Internally, a list is a chain of **pairs**. Each pair holds one item and a reference to the next pair, and the chain ends with the empty list `'()`. This is the linked list described in [Thinking in Programs](#thinking-in-programs):

```text
  days
   |
   v
 +-----+---+   +-----+---+   +-----+---+         +-----+----+
 | mon | --+-->| tue | --+-->| wed | --+-- ... ->| fri | () |
 +-----+---+   +-----+---+   +-----+---+         +-----+----+
```

`cons` does not copy the list it adds to; it makes one new pair that points to the old list. As a result, lists can share their tails, and building a list one item at a time is inexpensive.

Most functions on lists follow the same pattern: they handle the empty list, and otherwise do something with the `car` and recurse on the `cdr`:

```scheme
(define (sum lst)
  (if (null? lst)
      0
      (+ (car lst) (sum (cdr lst)))))
(sum '(3 1 4 1 5))            ; => 14
```

## Lookup Tables

A list of pairs can serve as a lookup table, called an **association list**. `cons` makes a pair from any two values. When the second value is a list, the result is a longer list; when it is not, the pair is written with a dot between its two parts, so `(cons 'ben 2501)` is `(ben . 2501)`. Such **dotted pairs** suit a table of names and values:

```scheme
(define phones '((anna . 4711) (ben . 2501) (cleo . 1234)))
(cdr (assq 'ben phones))      ; => 2501
```

`assq` finds the first pair whose first part is the given symbol, or returns `#f` if there is none. For a few dozen entries, an association list is sufficient.

## Functions as Values

In Scheme, a function is a value like any other. It can be passed to another function, returned from one, or stored in a list. A function that takes or returns functions is called **higher-order**.

The standard function `map` applies a function to every item of a list:

```scheme
(map square '(1 2 3 4))       ; => (1 4 9 16)
```

Higher-order functions are defined like any other. This one keeps the items of a list for which a test is true:

```scheme
(define (keep ok? lst)
  (cond ((null? lst) '())
        ((ok? (car lst)) (cons (car lst) (keep ok? (cdr lst))))
        (else (keep ok? (cdr lst)))))

(keep even? '(1 2 3 4 5 6))           ; => (2 4 6)
(keep (lambda (x) (> x 10)) '(5 50 8 80))   ; => (50 80)
```

`lambda` makes a function without giving it a name, which is convenient when a small function is needed only once. The definition `(define (square x) (* x x))` is shorthand for `(define square (lambda (x) (* x x)))`.

With `map`, `keep` and similar functions, many tasks that need a loop and some bookkeeping in other languages become a single expression.

## Closures

A function made by `lambda` retains access to the variables that were visible where it was made, even after the code that created them has finished. Such a function is a **closure**:

```scheme
(define (make-counter)
  (let ((count 0))
    (lambda ()
      (set! count (+ count 1))
      count)))

(define tally (make-counter))
(tally)                       ; => 1
(tally)                       ; => 2
```

Each call to `make-counter` creates a new variable `count` and returns a function that can reach it; no other code can. `set!` changes a variable's value; by convention, the exclamation mark indicates that something is changed in place. Closures provide private, persistent state without any additional language features, and many larger programming techniques are built on them.

## Memory

Scheme programs create pairs, strings and closures freely and never release them. The interpreter releases them automatically: from time to time, a **garbage collector** finds every object the program can still reach, starting from its variables, and recycles the rest. Scheme programmers, like those of most modern languages, never free memory by hand, which eliminates a whole class of errors. The cost is some additional memory and an occasional pause while the collector runs.

## Code Is Data

A Scheme program is written as lists, and lists are Scheme's main data structure. As a result, a program can readily build, examine and run other programs. This is an evaluator for a small language of sums and products:

```scheme
(define (calc e)
  (cond ((number? e) e)
        ((eq? (car e) '+) (+ (calc (cadr e)) (calc (caddr e))))
        ((eq? (car e) '*) (* (calc (cadr e)) (calc (caddr e))))
        (else 'unknown)))

(calc '(+ 1 (* 2 3)))         ; => 7
```

`cadr` and `caddr` are shorthand for the second and third items of a list. The evaluator examines the expression. A number is its own value. A list starting with `+` or `*` is evaluated by evaluating its two arguments and combining the results.

Interpreters work in this way. If `calc` is extended with variables, `if`, `lambda` and function calls, it becomes an interpreter for Scheme itself, which is known to require only a page or two of code. This shows that a programming language is itself a program, and that a small one can be complete.

## Scheme on a Machine

A Scheme system on a particular computer adds procedures for what the standard leaves out: files, windows, the network and the hardware. With them, a few lines of Scheme typed at the REPL can automate the machine or form a small windowed tool, without the need for a compiler.

Scheme is well suited to problems concerned with structure: lists of things, rules, transformations, small languages, and problems that benefit from interactive exploration. For obtaining the greatest speed from a slow processor, C is the better choice.
