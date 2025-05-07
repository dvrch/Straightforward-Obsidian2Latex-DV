#!/bin/bash
# This file compiles the latex file to .pdf

# Set base path and file name
BASE_PATH="c:/Users/dvrch/Desktop/Straightforward-Obsidian2Latex/Straightforward-Obsidian2Latex/example_vault/✍Writing"
FILE_NAME="example_writing"
TEXFILE="$BASE_PATH/$FILE_NAME.tex"
PDFFILE="$BASE_PATH/$FILE_NAME.pdf"

# Print paths for debugging
echo "TEXFILE: $TEXFILE"
echo "PDFFILE: $PDFFILE"

# Run pdflatex twice to resolve references
pdflatex -interaction=nonstopmode -shell-escape "$TEXFILE"
if [ $? -ne 0 ]; then
    echo "First pdflatex compilation failed."
    exit 1
fi

# Run second pass for references
pdflatex -interaction=nonstopmode -shell-escape "$TEXFILE"
if [ $? -ne 0 ]; then
    echo "Second pdflatex compilation failed."
    exit 1
fi

# Open the resulting PDF file using PowerShell Start-Process on Windows
if [ -f "$PDFFILE" ]; then
    powershell.exe "Start-Process '$PDFFILE'"
else
    echo "PDF file not found: $PDFFILE"
    exit 1
fi