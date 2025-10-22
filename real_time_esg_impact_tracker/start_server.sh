#!/bin/bash
# Start the ESG Impact Tracker Server

cd /workspace/real_time_esg_impact_tracker

echo "Starting ESG Impact Tracker Server..."
echo "Server will be available at http://localhost:5000"
echo ""

python3 -m backend.app
