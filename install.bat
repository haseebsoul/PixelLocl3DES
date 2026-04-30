@echo off
REM PixelLock 3DES - Installation Script for Windows

echo.
echo ====================================================
echo  PixelLock 3DES - Installation Script
echo ====================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [✓] Python found
python --version

REM Create virtual environment
echo.
echo [*] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [✓] Virtual environment created

REM Activate virtual environment
echo.
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo [✓] Virtual environment activated

REM Install requirements
echo.
echo [*] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [✓] Dependencies installed successfully

REM Create directories
echo.
echo [*] Creating directories...
if not exist app\uploads mkdir app\uploads
if not exist app\encrypted_images mkdir app\encrypted_images
echo [✓] Directories created

REM Display completion message
echo.
echo ====================================================
echo  ✓ Installation Complete!
echo ====================================================
echo.
echo Next steps:
echo 1. Run the application: python run.py
echo 2. Open browser to: http://localhost:5000
echo.
echo To start the application, run:
echo   python run.py
echo.
pause
