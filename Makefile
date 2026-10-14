# Timeless Computing
#
#   make deps      fetch the external projects the tests need into ext/
#   make test      run every example in the book, and check that the
#                  listings in the chapters match the tested files
#   make check     lint the chapter sources for the Zeitlos reader
#   make           build PDF, HTML, Markdown and plain text into dist/
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

pdf: gen
	latexmk -pdf -xelatex -output-directory=build tc.tex
	mv build/tc.pdf dist

html: gen
	cd build && pandoc ../tc.tex -s --toc -t html -o ../dist/tc.html

text: gen
	cd build && pandoc ../tc.tex -s --toc -t plain -o ../dist/tc.txt

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
	rm -f build/*

.PHONY: all pdf html text markdown check verify test deps gen view clean
