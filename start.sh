#!/bin/bash
# Start script for Railway deployment - Backend only

# Frontend is deployed separately on Vercel
echo "Starting CrewBuilder API server..."

# Start FastAPI backend
uvicorn api_server:app --host 0.0.0.0 --port ${PORT:-8000}