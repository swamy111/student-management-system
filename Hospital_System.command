#!/bin/bash
# Hospital Management System - Desktop Launcher for Mac

echo "🏥 Starting Hospital Management System..."
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed!"
    exit 1
fi

# Navigate to app directory
cd "$(dirname "$0")"

# Install Flask if not already installed
echo "📦 Checking dependencies..."
python3 -m pip install flask --quiet

# Start the web server
echo "🚀 Starting Hospital Management System..."
echo "🌐 Opening in your browser..."
echo ""

# Open browser after 2 seconds
(sleep 2 && open http://127.0.0.1:5002) &

# Run the application
python3 app.py
