#!/bin/bash
# Run script for Gource GUI

cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Run the GUI
python3 main.py
