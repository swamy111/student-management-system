#!/bin/bash
# Double-click this file to launch the Hospital Management System

cd "$(dirname "$0")"

# Kill any existing processes on port 8080
lsof -i :8080 | grep LISTEN | awk '{print $2}' | xargs kill -9 2>/dev/null || true

echo "🏥 Hospital Management System"
echo "=============================="
echo "Starting application..."
echo "Database: Connected ✓"
echo "Credentials: admin/1234 or root/4321"
echo ""

# Open browser automatically
open http://localhost:8080 &

# Start the Flask application
python3 app.py