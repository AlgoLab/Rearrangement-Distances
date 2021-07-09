targets = main.pdf

all : $(targets)

%.pdf : %.tex
	latexmk -pdf $< && latexmk -c $<

.PHONY : clean
clean :
	rm -f *~
