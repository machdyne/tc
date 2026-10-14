# Thinking in Programs

A program is a precise description of how to perform a task, written for a machine that does exactly what it is instructed to do and nothing else. Learning to program consists mostly of learning to divide a task into steps small and clear enough for a machine to follow. This chapter covers the ideas common to every programming language. The three chapters after it show those ideas in three different languages, each of which runs on Machdyne's systems.

## Why Program

A computer can be used without being programmed. Programming, however, is what makes a general-purpose computer general. A person who can write short programs can make the machine perform tasks that nobody planned for: renaming a thousand files, logging a temperature every hour, converting a document or controlling a pump.

Programming also teaches how computers work, which makes faults easier to find and correct. Code generated automatically, including by AI models, must still be read, understood and corrected by someone. In addition, a person who can program can keep their tools working without depending on an outside service.

## Algorithms

An **algorithm** is a method for solving a problem in a finite number of exact steps. Algorithms are older than computers. One of the oldest known, recorded by Euclid around 300 BC, finds the greatest common divisor of two numbers, the largest number that divides both exactly:

```text
to find the greatest common divisor of A and B:
    while B is not zero:
        let R be the remainder of A divided by B
        replace A with B, and B with R
    the answer is A
```

For 1071 and 462, the remainders are 147, then 21, then 0, so the answer is 21. The appendix [Three Languages Side by Side](#three-languages-side-by-side) shows the same algorithm in BASIC, Scheme and C.

A description of steps in plain words, such as this one, is called **pseudocode**. It is a useful way to plan a program before choosing a language.

## State

A program works by changing **state**: the values held in memory. A **variable** is a named place that holds a value. Assigning to a variable replaces its previous value:

```text
count = 0
count = count + 1
```

The second line is not an equation, which would be false. It is an instruction to compute `count + 1` and store the result back in `count`. Every step of a running program can be understood as reading some state and writing some new state. When a program behaves incorrectly, the question is almost always which part of the state differs from what was expected, and when it changed.

Values have **types**: whole numbers, fractional numbers, characters, text, true-or-false values and others. A type determines what a value means and which operations apply to it. As [Information](#information) showed, the same bits can mean different things. Types are the means by which a language records which meaning applies.

## Control Flow

Programs are built from three kinds of structure:

- **Sequence**: one step, then the next.
- **Choice**: if a condition is true, one step; otherwise another.
- **Repetition**: a step repeated a fixed number of times, or until a condition becomes true.

Every algorithm, however large, can be written with these three. Euclid's method above uses all of them: a sequence of steps inside a loop that repeats while a condition holds.

## Functions

A **function**, also called a procedure or subroutine, is a named part of a program that takes some inputs, called **arguments**, performs a task, and usually returns a result. Once written, a function can be used without regard to how it works. It is the most important tool in programming, because it is the means by which a large problem is divided into small ones.

A good function does one clear thing and has a name that describes it. A program for a weather station might have functions to read the sensor, convert the reading to degrees, decide whether it is freezing and write a line to the log. Each is short and can be checked on its own, and the main program reads almost as a description of the task.

A function can call itself. This is **recursion**, and it suits problems that contain smaller instances of themselves. The factorial of a number n, written n!, is n times the factorial of n - 1, and the factorial of 0 is 1. A recursive function states exactly that. Recursion needs a **base case**, here 0, at which it stops. Without one, the function calls itself until the stack is exhausted.

## Data Structures

The arrangement of data matters as much as the steps that operate on it. A few structures cover most needs:

- An **array** is a row of values of the same type, numbered from 0, each reached directly by its number. Arrays are fast and simple, but fixed in size.
- A **string** is a sequence of characters, usually stored as an array.
- A **record**, or structure, groups a few named values that belong together, such as a name, a date and an amount.
- A **linked list** is a chain of records, each holding a value and the address of the next. It can grow and shrink easily, but reaching the hundredth item requires passing through the first ninety-nine.
- A **tree** is similar to a list, except that each record can point to several others. A folder of files, in which each folder can hold further files and folders, is a tree.
- A **hash table**, also called a dictionary or map, stores values under keys, such as words and their definitions, and finds a key quickly without searching every entry.

With the right structure, the algorithm is often straightforward.

## Efficiency

On a slow computer, the efficiency of an algorithm has practical consequences. The useful measure is how the amount of work grows as the amount of data grows.

Finding a name in an unsorted list of n names may require checking all n of them. If the list doubles in length, the work doubles. In a sorted list, a program can instead examine the middle entry, determine which half contains the name, and repeat. Each step halves the remaining entries, so a million names require only about twenty comparisons. This method is **binary search**, and it is the difference between a program that answers at once and one that makes the user wait.

Some methods grow much faster. Comparing every item with every other item takes n times n steps, so a thousand items require a million comparisons. A loop inside a loop over a large amount of data is often a sign that a better method exists.

## Compilers and Interpreters

A processor runs only machine code, so a program in any other language must be translated. There are two approaches.

A **compiler** translates the whole program into machine code before it runs. The result runs at full speed, and many mistakes are reported before the program runs at all. The cost is a separate step between writing and running. C is normally compiled.

An **interpreter** reads the program and carries out each part directly, as it proceeds. It is slower, often by a factor of ten or more. In exchange, a programmer can type a line and see its effect immediately, change the program while it runs, and work on a machine that has no compiler. BASIC and Scheme are usually interpreted.

Many systems lie between the two. Some interpreters first translate the program into a compact internal form, often called **bytecode** or tokens, and interpret that, which is faster than working from the text. Machdyne BASIC checks each line and converts it into tokens as it is typed.

## Mistakes

Almost every program contains mistakes, called **bugs**, when first written. They are of three broad kinds:

- **Syntax errors**: the program is not valid in its language, in the way that a sentence with its words in the wrong order is not valid. The compiler or interpreter reports these.
- **Run-time errors**: the program is valid but attempts something impossible when it runs, such as dividing by zero or reading past the end of an array.
- **Logic errors**: the program runs without complaint and gives the wrong answer. These are the most difficult to find, because nothing reports them.

Finding bugs is called **debugging**. The method matters more than the tools:

1. **Reproduce** the problem reliably. A bug that cannot be made to occur on demand cannot be confirmed as fixed.
2. **Observe** instead of guessing. Print the values of variables at key points, or step through the program, and compare the results with what was expected.
3. **Narrow the search.** Find the earliest point at which the state is wrong. Halving the search space each time, as in binary search, finds the cause quickly.
4. **Fix the cause**, not the symptom. Then check that the original problem is gone and that nothing else has broken.

Small **tests**, programs that run a function with known inputs and check its outputs, find many bugs early and prevent them from returning.

## Writing for People

A program is read far more often than it is written, frequently by its own author months later. Clear names, short functions, consistent layout and brief comments that explain why something is done, rather than what, make a program much easier to maintain. The simplest program that performs the task is usually the best one.

## Three Languages

The next three chapters use three languages. Each represents a different way of thinking about programs, and each has been in use for decades. All three run on Zeitlos, and BASIC also runs on Machdyne's modules.

| Language | Born | Style                     | Best for                    |
|----------|------|---------------------------|-----------------------------|
| BASIC    | 1964 | numbered lines            | first programs, modules     |
| Scheme   | 1975 | expressions and functions | ideas, structure, scripting |
| C        | 1972 | near the machine          | speed, hardware, systems    |

The chapters can be read in any order, starting with the language that best suits the reader's purpose.
