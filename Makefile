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
# Point ZEITLOS at a checkout to enable it; skipped otherwise, so this
# stays optional for anyone building only the book.
ZEITLOS ?= ../zeitlos

verify: markdown
	@if [ -d "$(ZEITLOS)/sw/apps/read" ]; then \
		$(MAKE) -C $(ZEITLOS)/sw/apps/read test DOCS=$(CURDIR)/dist/tc.md; \
		$(MAKE) -C $(ZEITLOS)/sw/apps/read render DOC=$(CURDIR)/dist/tc.md \
			MODE=scroll; \
	else \
		echo "verify: no zeitlos checkout at $(ZEITLOS), skipping"; \
	fi

gen: build
	pandoc $(PANDOC_OPTS) chapters/timeless_computing.md -o build/timeless_computing.tex
	pandoc $(PANDOC_OPTS) chapters/electronics.md -o build/electronics.tex
	pandoc $(PANDOC_OPTS) chapters/digital_logic.md -o build/digital_logic.tex
	pandoc $(PANDOC_OPTS) chapters/computing.md -o build/computing.tex
	pandoc $(PANDOC_OPTS) chapters/programming.md -o build/programming.tex
	pandoc $(PANDOC_OPTS) chapters/fpgas.md -o build/fpgas.tex
	pandoc $(PANDOC_OPTS) chapters/socs.md -o build/socs.tex
	pandoc $(PANDOC_OPTS) chapters/zeitlos.md -o build/zeitlos.tex
	pandoc $(PANDOC_OPTS) chapters/survival.md -o build/survival.tex

view:
	evince dist/tc.pdf

clean:
	rm -f build/*

.PHONY: all pdf html text markdown check verify gen view clean
