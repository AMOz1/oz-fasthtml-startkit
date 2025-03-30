#!/bin/bash

# Get the directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
else
    # Create virtual environment if it doesn't exist
    python3 -m venv venv
    source venv/bin/activate
    # Install requirements
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    fi
    # Install launcher requirements if they exist separately
    if [ -f "launcher_requirements.txt" ]; then
        pip install -r launcher_requirements.txt
    fi
fi

# Run the launcher
python3 launcher.py 