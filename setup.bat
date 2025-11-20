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
echo IMPORTANT: Before proceeding, make sure you've set PowerShell execution policy.
echo If you haven't done this yet, press Ctrl+C to cancel, then run as Administrator:
echo   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
echo.
echo Press any key to continue with setup...
pause >nul
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
call npm.cmd --version
echo [OK] Node.js and npm are installed
echo.

REM Check for .env file
echo [3/6] Checking environment configuration...
if not exist .env (
    echo [WARNING] Backend .env file not found
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
    echo [OK] Backend .env file exists
)
echo.

REM Check for frontend .env file
echo Checking frontend environment configuration...
if not exist frontend\.env (
    echo [WARNING] Frontend .env file not found
    if exist frontend\.env.example (
        echo Creating frontend\.env from frontend\.env.example...
        copy frontend\.env.example frontend\.env
        echo [OK] Frontend .env file created
    ) else (
        echo [ERROR] frontend\.env.example not found
        pause
        exit /b 1
    )
) else (
    echo [OK] Frontend .env file exists
)
echo.

REM Install backend dependencies
echo [4/6] Setting up Python virtual environment...
cd backend

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        cd ..
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)

REM Activate virtual environment and install dependencies
echo Activating virtual environment and installing dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install Python dependencies
    call deactivate
    cd ..
    pause
    exit /b 1
)
call deactivate

cd ..
echo [OK] Python dependencies installed in virtual environment
echo.

REM Install frontend dependencies
echo [5/6] Installing Node.js dependencies...
echo This may take a few minutes...
cd frontend
call npm.cmd install
if errorlevel 1 (
    echo [ERROR] Failed to install Node.js dependencies
    echo.
    echo Common causes:
    echo 1. PowerShell execution policy not set - Run as Administrator:
    echo    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    echo 2. Network connection issues
    echo 3. npm cache issues - Try: npm cache clean --force
    echo.
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
call venv\Scripts\activate.bat
python manage.py migrate
if errorlevel 1 (
    echo [ERROR] Failed to run database migrations
    call deactivate
    cd ..
    pause
    exit /b 1
)
call deactivate
cd ..
echo [OK] Database initialized
echo.

echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo To start the development servers:
echo.
echo Open TWO separate Command Prompt or PowerShell windows:
echo.
echo   Window 1 - Backend:
echo     cd backend
echo     venv\Scripts\activate.bat
echo     python manage.py runserver
echo.
echo   Window 2 - Frontend:
echo     cd frontend
echo     npm run dev
echo.
echo Then visit: http://localhost:5173
echo.
echo NOTE: The backend now uses a virtual environment (venv)
echo       Remember to activate it with: venv\Scripts\activate.bat
echo.
echo To stop the servers later, press Ctrl+C in each window.
echo.
pause
