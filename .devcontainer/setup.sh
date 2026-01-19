#!/bin/bash

echo "=========================================="
echo "Setting up Todo App - Full Stack"
echo "=========================================="

# Setup Backend
echo ""
echo "📦 Setting up Backend (FastAPI)..."
cd backend
pip install -r requirements.txt
cp .env.example .env 2>/dev/null || echo "Using existing .env"
cd ..

# Setup Frontend
echo ""
echo "📦 Setting up Frontend (Next.js)..."
cd frontend
npm install
cp .env.local.example .env.local 2>/dev/null || echo "Using existing .env.local"
cd ..

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "To run the application:"
echo ""
echo "  Terminal 1 - Backend:"
echo "    cd backend && uvicorn main:app --reload --host 0.0.0.0"
echo ""
echo "  Terminal 2 - Frontend:"
echo "    cd frontend && npm run dev"
echo ""
echo "  Phase I (CLI):"
echo "    python main.py"
echo ""
echo "=========================================="
