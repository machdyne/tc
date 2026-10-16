# Timeless Computing
#
#   make deps      fetch the external projects the tests need into ext/
#   make test      run every example in the book, and check that the
#                  listings in the chapters match the tested files
#   make check     lint the chapter sources for the Zeitlos reader
#   make           build PDF, HTML, Markdown and plain text into dist/
#   make print     build the 13.5 x 21.5 cm print edition, dist/tc-print.pdf
#   make cover     build the front cover at print size, dist/tc-cover-front.pdf
#   make cover-wrap
#                  build the whole printed cover, dist/tc-cover-wrap.pdf, to
#                  the dimensions below, from the printer's cover calculator
#   make verify    run the Zeitlos reader's own parser over dist/tc.md
#
# The Markdown target does NOT go through LaTeX.
#
# chapters/*.md -> pandoc -> *.tex -> pandoc -> tc.md was a round trip
# through a print-oriented AST, and it came back with the print path's
# scaffolding baked in: fenced divs, {#anchor} attributes, simple
# tables in place of pipe tables, and syntax highlighting rendered as
# inline colour spans, which destroys code outright. It also silently
# dropped table cells. tools/mkbook.py copies the chapters instead and
# generates only the front pages and the contents list.
#
# The PDF, HTML and text targets are unchanged -- for those, the
# LaTeX route is the right one.

PYTHON ?= python3

# The chapter list lives in one place: the \input{} lines of tc.tex.
CHAPTERS := $(shell sed -n 's/^[ \t]*\\input{\(.*\)\.tex}.*/\1/p' tc.tex)

# External projects, fetched by `make deps`. Nothing here is a
# submodule: the book is rebuilt a few times a year, and a shallow
# clone of the current version of each is all the tests need.
EXT ?= ext
GITHUB ?= https://github.com/machdyne
DEPS = basic ms zeitlos

all: pdf html markdown text

build:
	mkdir -p build dist

pdf: gen build/cover-front.pdf
	latexmk -pdf -xelatex -output-directory=build tc.tex
	mv build/tc.pdf dist

# The print edition shares tc.tex; tc-print.tex switches it to the book
# layout in print-setup.tex. Its chapters are converted separately,
# because in a book the top level is \chapter rather than \section.
PRINT = build/print

print: build
	mkdir -p $(PRINT)
	@for c in $(CHAPTERS); do \
		echo "pandoc chapters/$$c.md (print)"; \
		pandoc $(PANDOC_OPTS) -f markdown+autolink_bare_uris \
			--top-level-division=chapter --lua-filter=tools/keep.lua \
			chapters/$$c.md -o $(PRINT)/$$c.tex || exit 1; \
	done
	latexmk -pdf -xelatex -output-directory=$(PRINT) tc-print.tex
	mv $(PRINT)/tc-print.pdf dist
	@if grep -q 'TODO' imprint.tex; then \
		echo "print: warning: imprint.tex still has a TODO"; \
	fi
	@want=$$(sed -n 's/^\\def\\tcpages{\([0-9]*\)}.*/\1/p' tc-print.tex); \
	got=$$(grep -a -c '/Type */Page[^s]' dist/tc-print.pdf); \
	if command -v pdfinfo > /dev/null; then \
		got=$$(pdfinfo dist/tc-print.pdf | sed -n 's/^Pages: *//p'); fi; \
	echo "print: $$got pages ($$want ordered)"; \
	if [ -n "$$want" ] && [ "$$got" != "$$want" ]; then \
		echo "print: warning: the book has $$got pages, not $$want;"; \
		echo "  trim it, or order $$got pages and recalculate the cover"; \
	fi

# Covers, from cover/cover.svg (needs rsvg-convert, Python's PIL and the
# Lato font). See tools/mkcover.py.
build/cover-front.pdf: cover/cover.svg tools/mkcover.py | build
	$(PYTHON) tools/mkcover.py screen -o $@

cover: build
	$(PYTHON) tools/mkcover.py front -o dist/tc-cover-front.pdf

# The printed cover, in mm, from BoD's cover calculator for this edition:
# hardcover, thread-sewn, straight spine, 13.5 x 21.5 cm, white 90 g,
# 256 pages (\tcpages in tc-print.tex). They change with the page count
# and the paper: run the calculator again if either changes.
#   WIDTH   total width including edge
#   HEIGHT  height including edge
#   SPINE   book spine width
#   WRAP    top/bottom/outside impact edge
#   HINGE   fold width within U1/U4
WIDTH ?= 332.9
HEIGHT ?= 255
SPINE ?= 18.9
WRAP ?= 17
HINGE ?= 8

# The ISBN barcode for the back cover, from the myBoD project.
BARCODE ?= cover/barcode.png
# The ground behind it: none (straight on the pale artwork), white,
# or a pale colour. Scan the proof copy before approving it.
BARCODE_BG ?= none
BARCODE_RADIUS ?= 0

cover-wrap: build
	@if [ -z "$(WIDTH)" ] || [ -z "$(HEIGHT)" ] || [ -z "$(SPINE)" ] || \
	    [ -z "$(WRAP)" ]; then \
		echo "cover-wrap: set WIDTH, HEIGHT, SPINE and WRAP (mm) from the"; \
		echo "printer's cover template, e.g. make cover-wrap WIDTH=330 \\"; \
		echo "  HEIGHT=251 SPINE=18 WRAP=18"; \
		exit 1; \
	fi
	$(PYTHON) tools/mkcover.py wrap -o dist/tc-cover-wrap.pdf \
		--width $(WIDTH) --height $(HEIGHT) --spine $(SPINE) --wrap $(WRAP) \
		--hinge $(HINGE) \
		$(if $(BARCODE),--barcode $(BARCODE) --barcode-bg '$(BARCODE_BG)' \
		  --barcode-radius $(BARCODE_RADIUS))

html: gen
	$(PYTHON) tools/screentex.py tc.tex build/tc-screen.tex
	cd build && pandoc tc-screen.tex -s --toc -t html --metadata pagetitle="Timeless Computing" -o ../dist/tc.html

text: gen
	$(PYTHON) tools/screentex.py tc.tex build/tc-screen.tex
	cd build && pandoc tc-screen.tex -s --toc -t plain -o ../dist/tc.txt

# No `gen` dependency: this reads the chapter sources directly.
markdown: build
	$(PYTHON) tools/mkbook.py --tex tc.tex --chapters chapters -o dist/tc.md

# Lint the sources without writing anything. --strict makes it fail
# the build on a duplicate heading slug or a dead cross-reference.
check:
	$(PYTHON) tools/mkbook.py --check-only --strict

# Run the reader's own parser tests and layout check over the output.
ZEITLOS ?= $(EXT)/zeitlos

verify: markdown
	@if [ -d "$(ZEITLOS)/sw/apps/read" ]; then \
		$(MAKE) -C $(ZEITLOS)/sw/apps/read test DOCS=$(CURDIR)/dist/tc.md; \
		$(MAKE) -C $(ZEITLOS)/sw/apps/read render DOC=$(CURDIR)/dist/tc.md \
			MODE=scroll; \
	else \
		echo "verify: no zeitlos checkout at $(ZEITLOS) (make deps), skipping"; \
	fi

# Every code listing in the book is a tested file under tests/.
test:
	$(PYTHON) tests/listings.py chapters tests
	EXT=$(CURDIR)/$(EXT) sh tests/run.sh

deps:
	mkdir -p $(EXT)
	@for r in $(DEPS); do \
		if [ -d $(EXT)/$$r/.git ]; then \
			echo "deps: updating $$r"; git -C $(EXT)/$$r pull -q --ff-only; \
		else \
			echo "deps: fetching $$r"; \
			git clone -q --depth 1 $(GITHUB)/$$r $(EXT)/$$r; \
		fi; \
	done
	$(MAKE) -C $(EXT)/basic basic
	$(MAKE) -C $(EXT)/ms ms

gen: build
	@for c in $(CHAPTERS); do \
		echo "pandoc chapters/$$c.md"; \
		pandoc $(PANDOC_OPTS) chapters/$$c.md -o build/$$c.tex || exit 1; \
	done

view:
	evince dist/tc.pdf

clean:
	rm -rf build/*

.PHONY: all pdf print cover cover-wrap html text markdown check verify \
	test deps gen view clean
