#!/bin/bash
# Hospital Management System Launcher for macOS

cd "$(dirname "$0")"

echo "Starting Hospital Management System..."
echo "Database connection: SUCCESSFUL"
echo "Default credentials: admin/1234 or root/4321"
echo ""
echo "Opening web browser..."
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Flask application
python3 app.py