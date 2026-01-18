#!/bin/bash
# Start Backend Server
# Usage: ./start-backend.sh

cd backend

echo "🚀 Starting FastAPI Backend Server..."
echo "📍 Server will run on: http://127.0.0.1:8000"
echo "📚 API Documentation: http://127.0.0.1:8000/docs"
echo ""

# Activate virtual environment and start server
./venv/bin/uvicorn main:app --reload --host 127.0.0.1 --port 8000
