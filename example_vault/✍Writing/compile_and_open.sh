#!/bin/bash
# filepath: c:\Users\dvrch\Desktop\Memoire 2024\Straightforward-Obsidian2Latex\Straightforward-Obsidian2Latex-DV\example_vault\✍Writing\compile_and_open.sh

# This file compiles the latex file to .pdf

# Set base path and file name
BASE_PATH="C:\Users\dvrch\Desktop\Memoire 2024\Straightforward-Obsidian2Latex\Straightforward-Obsidian2Latex-DV\example_vault\✍Writing"
FILE_NAME="example_writing"


TEXFILE="$BASE_PATH/$FILE_NAME.tex"
PDFFILE="$BASE_PATH/$FILE_NAME.pdf"

# Replace \begin{tabularx} with \begin{tabularx}{1.0\textwidth}
sed -i "s/\\\\begin{tabularx}{p/\\\\begin{tabularx}{1.0\\\\textwidth}{p/g" "$TEXFILE"

# Print paths for debugging
echo "TEXFILE: $TEXFILE"
echo "PDFFILE: $PDFFILE"

# Compile the bibliography
bibtex "$BASE_PATH/$FILE_NAME"

# Compile the LaTeX file
pdflatex -interaction=nonstopmode -shell-escape "$TEXFILE"
if [ $? -ne 0 ]; then
    echo "pdflatex compilation failed."
    exit 1
fi
#

# Compile the LaTeX file again for references
pdflatex -interaction=nonstopmode -shell-escape "$TEXFILE"
pdflatex -interaction=nonstopmode -shell-escape "$TEXFILE"

# Open the resulting PDF file
# Use 'start' on Windows (Git Bash) and 'xdg-open' on Linux/macOS
if [[ "$OSTYPE" == "msys" ]]; then
  start "$PDFFILE"
else
  xdg-open "$PDFFILE"
fi