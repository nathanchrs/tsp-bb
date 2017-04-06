LATEX=pdflatex

.PHONY: all clean doc

all: doc

doc:
	-$(LATEX) doc/report.tex -output-directory doc

clean:
	-rm result
	-rm result.png
	-rm doc/report.aux
	-rm doc/report.log
	-rm doc/report.pdf
