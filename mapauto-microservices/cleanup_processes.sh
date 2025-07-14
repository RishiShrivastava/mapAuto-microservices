#!/bin/bash

# Cleanup script for mapAuto microservices
# This script safely stops all running processes and cleans up temporary files

echo "Cleaning up mapAuto microservices..."

# Kill all uvicorn processes
echo "Stopping uvicorn services..."
pkill -f "uvicorn.*main:app" || true

# Kill any hanging nmap processes
echo "Stopping nmap processes..."
pkill -f "nmap" || true

# Clean up temporary XML files
echo "Cleaning temporary files..."
rm -f /tmp/OSScan_*.xml
rm -f /tmp/WAFPortScan_*.xml

# Wait a moment for processes to terminate
sleep 2

# Check if any processes are still running
echo "Checking for remaining processes..."
REMAINING_UVICORN=$(ps aux | grep -c "uvicorn.*main:app" || echo "0")
REMAINING_NMAP=$(ps aux | grep -c "nmap" || echo "0")

if [ "$REMAINING_UVICORN" -gt 1 ]; then
    echo "Warning: Some uvicorn processes may still be running"
fi

if [ "$REMAINING_NMAP" -gt 1 ]; then
    echo "Warning: Some nmap processes may still be running"
fi

echo "Cleanup complete!"
