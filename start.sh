#!/bin/bash
# Start script for Railway deployment

# Build Next.js frontend
echo "Building frontend..."
cd web
npm install
npm run build
cd ..

# Start FastAPI backend
echo "Starting FastAPI server..."
uvicorn api_server:app --host 0.0.0.0 --port ${PORT:-8000}