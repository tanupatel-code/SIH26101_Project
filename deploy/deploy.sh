#!/usr/bin/env bash
# ========================================================
# StatSkill AI — Linux / Cloud VPS Production Deploy Script
# ========================================================
set -euo pipefail

echo "=================================================="
echo " Starting StatSkill AI Production Deployment"
echo "=================================================="

# Check if Docker is available
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null || docker compose version &> /dev/null; then
    echo ">> Docker detected. Deploying with Docker Compose..."
    docker compose down --remove-orphans || true
    docker compose up --build -d
    echo ">> Deployment completed successfully via Docker!"
    echo ">> Backend running at: http://localhost:8000"
    echo ">> Frontend running at: http://localhost:80"
    exit 0
fi

echo ">> Docker not detected. Proceeding with Bare-Metal / Systemd Deployment..."

# 1. Setup Backend
echo ">> Setting up Python virtual environment..."
cd backend
python3 -m venv venv || python3.12 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cd ..

# 2. Build Frontend
echo ">> Building Frontend distribution..."
cd frontend
npm ci || npm install
npm run build
cd ..

echo "=================================================="
echo " Bare-metal build complete!"
echo " Start backend: cd backend && source venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000"
echo " Serve frontend: Configure Nginx to serve frontend/dist"
echo "=================================================="
