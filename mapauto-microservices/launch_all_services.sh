#!/bin/bash

# Launch all microservices script
echo "Starting all microservices..."

# Change to the mapauto-microservices directory
cd /home/kali/Documents/mapauto/mapAuto/mapauto-microservices

# Start nmapall_service on port 8000
echo "Starting nmapall_service on port 8000..."
cd nmapall_service
uvicorn main:app --host 0.0.0.0 --port 8000 &
NMAPALL_PID=$!
echo "nmapall_service started with PID: $NMAPALL_PID"

# Start nmapscanner_service on port 8001
echo "Starting nmapscanner_service on port 8001..."
cd ../nmapscanner_service
uvicorn main:app --host 0.0.0.0 --port 8001 &
NMAPSCANNER_PID=$!
echo "nmapscanner_service started with PID: $NMAPSCANNER_PID"

# Start osscan_service on port 8002
echo "Starting osscan_service on port 8002..."
cd ../osscan_service
uvicorn main:app --host 0.0.0.0 --port 8002 &
OSSCAN_PID=$!
echo "osscan_service started with PID: $OSSCAN_PID"

# Start portxmlparser_service on port 8003
echo "Starting portxmlparser_service on port 8003..."
cd ../portxmlparser_service
uvicorn main:app --host 0.0.0.0 --port 8003 &
PORTXML_PID=$!
echo "portxmlparser_service started with PID: $PORTXML_PID"

# Start autonessus_service on port 8004
echo "Starting autonessus_service on port 8004..."
cd ../autonessus_service
uvicorn main:app --host 0.0.0.0 --port 8004 &
AUTONESSUS_PID=$!
echo "autonessus_service started with PID: $AUTONESSUS_PID"

echo ""
echo "All microservices are starting..."
echo "Services and their ports:"
echo "- nmapall_service: http://localhost:8000"
echo "- nmapscanner_service: http://localhost:8001"
echo "- osscan_service: http://localhost:8002"
echo "- portxmlparser_service: http://localhost:8003"
echo "- autonessus_service: http://localhost:8004"
echo ""
echo "PIDs: $NMAPALL_PID $NMAPSCANNER_PID $OSSCAN_PID $PORTXML_PID $AUTONESSUS_PID"
echo ""
echo "To stop all services, run: kill $NMAPALL_PID $NMAPSCANNER_PID $OSSCAN_PID $PORTXML_PID $AUTONESSUS_PID"
echo ""
echo "Wait a few seconds for services to start, then test with:"
echo "curl http://localhost:8000/status"
echo "curl http://localhost:8001/status"
echo "curl http://localhost:8002/status"
echo "curl http://localhost:8003/status"
echo "curl http://localhost:8004/status"

# Keep the script running to show logs
wait
