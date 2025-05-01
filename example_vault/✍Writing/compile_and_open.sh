#!/bin/bash
# This file compiles the latex file to .pdf

# Set base path and file name
BASE_PATH="C:\Users\dvrch\Desktop\Memoire 2024\Straightforward-Obsidian2Latex\Straightforward-Obsidian2Latex-DV\example_vault\✍Writing"
FILE_NAME="example_writing"
TEXFILE="$BASE_PATH/$FILE_NAME.tex"
PDFFILE="$BASE_PATH/$FILE_NAME.pdf"

# Print paths for debugging
echo "TEXFILE: $TEXFILE"
echo "PDFFILE: $PDFFILE"

# Compile the LaTeX file
pdflatex -interaction=nonstopmode -shell-escape "$TEXFILE"
if [ $? -ne 0 ]; then
    echo "pdflatex compilation failed."
    exit 1
f

# Open the resulting PDF file
# Use 'start' on Windows (Git Bash) and 'xdg-open' on Linux/macOS
if [[ "$OSTYPE" == "msys" ]]; then
  start "$PDFFILE"
else
  xdg-open "$PDFFILE"
fi
