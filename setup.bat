@echo off
REM ============================================
REM Help2Study - Windows Setup Script
REM ============================================
REM This script automates the setup process for Windows
REM It will check requirements, install dependencies, and configure the app
REM ============================================

echo ============================================
echo Help2Study - Automated Setup (Windows)
echo ============================================
echo.

REM Check Python
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

python --version
echo [OK] Python is installed
echo.

REM Check Node.js
echo [2/6] Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed or not in PATH
    echo Please install Node.js 16+ from https://nodejs.org/
    pause
    exit /b 1
)

node --version
npm --version
echo [OK] Node.js and npm are installed
echo.

REM Check for .env file
echo [3/6] Checking environment configuration...
if not exist .env (
    echo [WARNING] .env file not found
    if exist .env.example (
        echo Creating .env from .env.example...
        copy .env.example .env
        echo.
        echo [ACTION REQUIRED] Please edit .env and add your Gemini API key
        echo Get your API key from: https://makersuite.google.com/app/apikey
        echo.
        echo Press any key after you've updated the .env file...
        pause >nul
    ) else (
        echo [ERROR] .env.example not found
        pause
        exit /b 1
    )
) else (
    echo [OK] .env file exists
)
echo.

REM Install backend dependencies
echo [4/6] Installing Python dependencies...
cd backend
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install Python dependencies
    cd ..
    pause
    exit /b 1
)
cd ..
echo [OK] Python dependencies installed
echo.

REM Install frontend dependencies
echo [5/6] Installing Node.js dependencies...
cd frontend
call npm install
if errorlevel 1 (
    echo [ERROR] Failed to install Node.js dependencies
    cd ..
    pause
    exit /b 1
)
cd ..
echo [OK] Node.js dependencies installed
echo.

REM Run migrations
echo [6/6] Setting up database...
cd backend
python manage.py migrate
if errorlevel 1 (
    echo [ERROR] Failed to run database migrations
    cd ..
    pause
    exit /b 1
)
cd ..
echo [OK] Database initialized
echo.

echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo To start the development servers, run:
echo   make dev
echo.
echo Or start them separately:
echo   make dev-backend   (Django on http://localhost:8000)
echo   make dev-frontend  (React on http://localhost:5173)
echo.
echo Note: If 'make' is not available on Windows, you can use:
echo   Backend:  cd backend ^&^& python manage.py runserver
echo   Frontend: cd frontend ^&^& npm run dev
echo.
pause
