PYTHON := /c/Users/jaico/anaconda3/python
export MPLCONFIGDIR := /c/Users/jaico/.matplotlib

.PHONY: all clean

all: paper/paper.pdf

# Preprocessing: data wrangling and figures
output/figures/figure_5_2.png output/figures/figure_5_3.png: input/PaidSearch.csv code/preprocess.py
	$(PYTHON) code/preprocess.py

# DID estimation
output/tables/did_table.tex: input/PaidSearch.csv code/did_analysis.py
	$(PYTHON) code/did_analysis.py

# Paper compilation
paper/paper.pdf: paper/paper.tex output/figures/figure_5_2.png output/figures/figure_5_3.png output/tables/did_table.tex
	cd paper && pdflatex paper.tex && pdflatex paper.tex

clean:
	rm -f output/figures/*.png output/tables/*.tex paper/paper.pdf paper/paper.aux paper/paper.log

# Q1: If I edit code/preprocess.py, Make rebuilds the figure files and then recompiles the paper. It does not rerun did_analysis.py because the DID table does not depend on preprocess.py.
# Q2: If I edit code/did_analysis.py, Make rebuilds the DID table and then recompiles the paper. It does not rerun preprocess.py because the figures do not depend on did_analysis.py.
# Q3: If I edit paper/paper.tex, Make only recompiles the paper. No Python scripts run because neither the figures nor the DID table depend on paper.tex.

