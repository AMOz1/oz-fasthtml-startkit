#!/bin/bash

# Get the directory where this script is located
cd "$(dirname "$0")"

echo "Radio NULA Track Search Launcher"
echo "-------------------------------"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install it first."
    read -p "Press Enter to exit..."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment."
        read -p "Press Enter to exit..."
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Error: Failed to activate virtual environment."
    read -p "Press Enter to exit..."
    exit 1
fi

# Install requirements if needed
if [ ! -f "venv/requirements_installed" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        touch venv/requirements_installed
    else
        echo "Error: Failed to install dependencies."
        read -p "Press Enter to exit..."
        exit 1
    fi
fi

# Stop any existing server
echo "Cleaning up any existing servers..."
python3 run.py stop

# Start the application
echo "Starting the application..."
echo "The application window should open shortly..."
echo "(If nothing happens in 10 seconds, check if port 5001 is already in use)"
echo ""
python3 launcher.py

# Keep terminal window open if there was an error
if [ $? -ne 0 ]; then
    echo "Error: Application exited unexpectedly."
    read -p "Press Enter to exit..."
fi 