# Timeless Computing

![Book Cover](https://github.com/machdyne/tc/blob/32c8dc7da0ad52f5420d7888877552061c905be8/cover.jpg)

*Timeless Computing* explains how a computer works, from the flow of electricity through logic gates, processors, memory, operating systems and security to programs written in BASIC, Scheme and C. It then shows how a complete computer can be built on an FPGA, a chip whose circuits are defined by a design that its owner can read, correct and change.

The book presents timeless computing as one approach to owning a computer: a machine built to remain useful for decades, and simple enough to be understood, maintained and adapted by the person who relies on it. Machdyne's FPGA computers and the Zeitlos operating system serve as working examples.

It is written for readers with no technical background, and serves as a coherent reference for those with experience.

The book is dedicated to the public domain.

You can read the [Markdown version of the book here](https://github.com/machdyne/tc/blob/main/dist/tc.md) or the [HTML version of the book here](https://machdyne.github.io/tc/dist/tc.html).

## Building

The book is available as PDF, HTML, Markdown and plain text files in the `dist` directory, but you can also build it from source:

```
$ make
```

You will need `texlive-full`, `pandoc` and `latexmk`.

The chapter order is set by the `\input` lines in `tc.tex`.

### Print edition and cover

Each edition is named by its year (`2026 Edition` on the title page and cover) and each corrected printing within it by a revision number, on the back of the title page (`2026 Edition, revision 1`). Corrections raise the revision and keep the ISBN; a new edition resets the revision to 1 and needs a new ISBN.

```
$ make print
$ make cover
$ make cover-wrap WIDTH=... HEIGHT=... SPINE=... WRAP=...
```

`make print` builds `dist/tc-print.pdf`, the book block for printing: 13.5 x 21.5 cm, two-sided, 10 pt text and 8 pt code, black only, padded to a multiple of four pages for a thread-sewn binding. Its publisher's imprint is in `imprint.tex`. The ISBN, the barcode in `cover/barcode.png` and the imprint identify the edition published by BoD, and appear only in the print edition and its cover. The text is in the public domain, but anyone else who prints the book should remove them and use an ISBN of their own, or none. It uses the same sources as the screen edition; its layout is in `print-setup.tex`. `tools/keep.lua` keeps every diagram, and tables of up to 8 rows, from being split across two pages, and moves a heading with them; program listings and longer tables may break, as they read from top to bottom, and a table repeats its header row on the next page. Its limits trade this against the page count.

The cover is drawn in `cover/cover.svg`. `make cover` builds the front cover at print size with 5 mm bleed. `make cover-wrap` builds the whole printed cover, back, spine and front, to the dimensions of the printer's cover template, which depend on the binding, page count and paper (all in mm; `WRAP` is the margin outside the visible front board: bleed, plus the turn-in on a hardcover). The ISBN barcode is printed straight on the pale artwork; `BARCODE_BG` puts it on a white or pale ground instead. The cover tools need the Python packages in `requirements.txt` (`pip install -r requirements.txt`), and three other programs: `rsvg-convert` from librsvg, `pdftocairo` from poppler (only for a barcode supplied as PDF) and the Lato font. On Debian and Ubuntu these are the packages `librsvg2-bin`, `poppler-utils` and `fonts-lato`; with Homebrew on macOS, `librsvg`, `poppler` and the Lato font from Google Fonts.

## Checking

The Markdown edition is read on Zeitlos by its own reader, which supports a subset of Markdown. Lint the chapters for it with:

```
$ make check
```

Every code listing in the book is a tested file under `tests/`. To fetch the external projects the tests use (Machdyne BASIC, Machdyne Scheme and Zeitlos) into `ext/` and run them:

```
$ make deps
$ make test
$ make verify
```

`make test` also checks that each listing in the chapters matches its tested file. It needs a C compiler, and uses Icarus Verilog, Yosys and the RISC-V binutils (`riscv64-unknown-elf-as`) if they are installed. `make verify` runs the Zeitlos reader's parser and layout checks over `dist/tc.md`.

## Contributing

The top contributors will receive a free physical copy of the book when it's completed.

The book is written in Markdown located in the `chapters` directory.

By submitting a contribution to this repository, you agree to dedicate your contribution to the public domain under the Creative Commons Zero (CC0) 1.0 Universal license. 

This means your contributions will be free to use without any restrictions.

Please do not contribute copyrighted material.

For more details, see: https://creativecommons.org/publicdomain/zero/1.0/

## License

To the extent possible under law, the contributors to this project have waived all copyright and related or neighboring rights to this work (the "Timeless Computing" book) under the CC0 1.0 Universal license.

