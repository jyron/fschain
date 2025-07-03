#!/bin/bash

echo "Starting Financial Index API locally..."
echo "The API will be available at: http://localhost:8000"
echo "Press Ctrl+C to stop the server"
echo ""

cd index_api
uvicorn main:app --reload --host 0.0.0.0 --port 8000 