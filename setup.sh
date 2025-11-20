#!/bin/bash
# ============================================
# Help2Study - macOS/Linux Setup Script
# ============================================
# This script automates the setup process for Unix-based systems
# It will check requirements, install dependencies, and configure the app
# ============================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "============================================"
echo "Help2Study - Automated Setup (macOS/Linux)"
echo "============================================"
echo ""

# Function to check version
check_version() {
    local cmd=$1
    local required=$2
    local name=$3

    if ! command -v "$cmd" &> /dev/null; then
        echo -e "${RED}[ERROR]${NC} $name is not installed or not in PATH"
        return 1
    fi

    return 0
}

# Check Python
echo -e "${BLUE}[1/6]${NC} Checking Python installation..."
if ! check_version "python3" "3.8" "Python"; then
    echo "Please install Python 3.8+ from:"
    echo "  - macOS: brew install python3 (or download from python.org)"
    echo "  - Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "  - Fedora: sudo dnf install python3 python3-pip"
    exit 1
fi

python3 --version
echo -e "${GREEN}[OK]${NC} Python is installed"
echo ""

# Check Node.js
echo -e "${BLUE}[2/6]${NC} Checking Node.js installation..."
if ! check_version "node" "16" "Node.js"; then
    echo "Please install Node.js 16+ from:"
    echo "  - macOS: brew install node (or download from nodejs.org)"
    echo "  - Ubuntu/Debian: curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt-get install -y nodejs"
    echo "  - Fedora: sudo dnf install nodejs"
    exit 1
fi

node --version
npm --version
echo -e "${GREEN}[OK]${NC} Node.js and npm are installed"
echo ""

# Check for .env file
echo -e "${BLUE}[3/6]${NC} Checking environment configuration..."
if [ ! -f .env ]; then
    echo -e "${YELLOW}[WARNING]${NC} Backend .env file not found"
    if [ -f .env.example ]; then
        echo "Creating .env from .env.example..."
        cp .env.example .env
        echo ""
        echo -e "${YELLOW}[ACTION REQUIRED]${NC} Please edit .env and add your Gemini API key"
        echo "Get your API key from: https://makersuite.google.com/app/apikey"
        echo ""
        read -p "Press Enter after you've updated the .env file..."
    else
        echo -e "${RED}[ERROR]${NC} .env.example not found"
        exit 1
    fi
else
    echo -e "${GREEN}[OK]${NC} Backend .env file exists"
fi
echo ""

# Check for frontend .env file
echo "Checking frontend environment configuration..."
if [ ! -f frontend/.env ]; then
    echo -e "${YELLOW}[WARNING]${NC} Frontend .env file not found"
    if [ -f frontend/.env.example ]; then
        echo "Creating frontend/.env from frontend/.env.example..."
        cp frontend/.env.example frontend/.env
        echo -e "${GREEN}[OK]${NC} Frontend .env file created"
    else
        echo -e "${RED}[ERROR]${NC} frontend/.env.example not found"
        exit 1
    fi
else
    echo -e "${GREEN}[OK]${NC} Frontend .env file exists"
fi
echo ""

# Install backend dependencies
echo -e "${BLUE}[4/6]${NC} Setting up Python virtual environment..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}[OK]${NC} Virtual environment created"
else
    echo -e "${GREEN}[OK]${NC} Virtual environment already exists"
fi

# Activate virtual environment and install dependencies
echo "Activating virtual environment and installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

cd ..
echo -e "${GREEN}[OK]${NC} Python dependencies installed in virtual environment"
echo ""

# Install frontend dependencies
echo -e "${BLUE}[5/6]${NC} Installing Node.js dependencies..."
cd frontend
npm install
cd ..
echo -e "${GREEN}[OK]${NC} Node.js dependencies installed"
echo ""

# Run migrations
echo -e "${BLUE}[6/6]${NC} Setting up database..."
cd backend
source venv/bin/activate
python manage.py migrate
deactivate
cd ..
echo -e "${GREEN}[OK]${NC} Database initialized"
echo ""

echo "============================================"
echo "Setup Complete!"
echo "============================================"
echo ""
echo "To start the development servers, run:"
echo "  make dev"
echo ""
echo "Or start them separately:"
echo "  make dev-backend   (Django on http://localhost:8000)"
echo "  make dev-frontend  (React on http://localhost:5173)"
echo ""
echo -e "${YELLOW}Note:${NC} The backend now uses a virtual environment (venv)"
echo "If running backend manually: cd backend && source venv/bin/activate && python manage.py runserver"
echo ""
echo "Happy coding!"
echo ""
