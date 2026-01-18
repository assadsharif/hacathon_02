#!/bin/bash
# Start Frontend Server
# Usage: ./start-frontend.sh

cd frontend

echo "🚀 Starting Next.js Frontend Server..."
echo "📍 Server will run on: http://localhost:3000"
echo "🔐 Sign-up page: http://localhost:3000/sign-up"
echo "🔐 Sign-in page: http://localhost:3000/sign-in"
echo ""

# Start Next.js development server
npm run dev
