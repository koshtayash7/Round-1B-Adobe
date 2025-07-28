#!/bin/bash
echo "[INFO] Running Document Intelligence System..."
mkdir -p output
python3 src/main.py input_pdfs/ output/output.json
