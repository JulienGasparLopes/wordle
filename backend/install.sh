#!/bin/bash

# Check for python3 or python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "Error: Python not found. Please install Python."
    exit 1
fi

echo "Using $PYTHON_CMD"

# Create virtual environment
$PYTHON_CMD -m venv .venv

# Install requirements using the python from the venv
source .venv/bin/activate
pip install -r requirements.txt

echo "Installation complete."