#!/bin/bash

echo "================================================"
echo "NSUT Placement Portal - Starting Application"
echo "================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing/updating dependencies..."
pip install -r requirements.txt

echo ""
echo "================================================"
echo "Starting Flask application..."
echo "Access the portal at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo "================================================"
echo ""

python app.py
