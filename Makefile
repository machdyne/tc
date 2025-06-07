all: pdf html markdown text

pdf: gen
	mkdir -p build
	latexmk -pdf -xelatex -output-directory=build tc.tex
	mv build/tc.pdf dist

html: gen
	cd build && pandoc ../tc.tex -s --toc -t html -o ../dist/tc.html

markdown: gen
	cd build && pandoc ../tc.tex -s --toc -t markdown -o ../dist/tc.md

text: gen
	cd build && pandoc ../tc.tex -s --toc -t plain -o ../dist/tc.txt

gen:
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
