# Style Guide

The book is written in a plain, formal expository style. It says things as simply and concisely as possible while still speaking to a person. It is neither robotic nor performative: its only purpose is to inform.

## Voice

- Write in the third person. Refer to "the reader", "the owner", "a programmer" or the thing itself. Do not address the reader as "you", except in direct practical instructions where any other wording would be awkward ("Disconnect power before changing connections" is preferred to "You should disconnect...").
- Do not use the authorial "we".
- State facts directly. Prefer "A flip-flop stores one bit" to "A flip-flop is a clever little circuit that stores one bit".
- Explain why as well as what, briefly. Reasoning is welcome; persuasion is not.
- Define every term before or when it is first used.

## Avoid

- Rhetorical contrasts and reversals used for effect ("It is fast, yet it feels slow").
- Quips, aphorisms and slogans ("A copy that has not been verified is a hope").
- Exclamations, rhetorical questions and teasers ("Here is the trick").
- Selling the subject ("the deepest lesson", "remarkable", "surprisingly useful", "beautiful").
- Reassurance and encouragement ("Don't worry", "This is easier than it looks").
- Short dramatic sentences placed for emphasis at the end of a paragraph.
- Analogies, except where one genuinely clarifies an idea that is otherwise hard to grasp. One clear analogy is better than several.
- Imperatives addressed to the reader in explanatory text ("Trace it by hand", "Notice that").
- Filler words: "simply", "just", "really", "actually", "of course", "in fact", "very", "quite".

## Prefer

- Complete, medium-length sentences with one idea each.
- Paragraphs that open with their main point.
- Concrete numbers and examples over general claims.
- Lists and tables where the content is a set of parallel items.
- Neutral transitions: "As a result", "For this reason", "In addition".

## Spelling and terms

British spelling (colour, behaviour, organize with -ize). "bootloader", "system on a chip" (SOC), "microcontroller", "Pmod", "F-RAM", "10k" for resistor values.

## Format constraints

The Markdown is read on Zeitlos by a reader with a limited subset. See the comments at the top of tools/mkbook.py. Code and table lines must be at most 78 columns. Run `make check` and `make test` after editing.
