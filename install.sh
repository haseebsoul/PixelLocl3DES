#!/bin/bash
# PixelLock 3DES - Installation Script for macOS/Linux

echo ""
echo "===================================================="
echo "  PixelLock 3DES - Installation Script"
echo "===================================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

echo "[✓] Python found"
python3 --version

# Create virtual environment
echo ""
echo "[*] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

echo "[✓] Virtual environment created"

# Activate virtual environment
echo ""
echo "[*] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi

echo "[✓] Virtual environment activated"

# Install requirements
echo ""
echo "[*] Installing Python dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo "[✓] Dependencies installed successfully"

# Create directories
echo ""
echo "[*] Creating directories..."
mkdir -p app/uploads
mkdir -p app/encrypted_images
echo "[✓] Directories created"

# Display completion message
echo ""
echo "===================================================="
echo "  ✓ Installation Complete!"
echo "===================================================="
echo ""
echo "Next steps:"
echo "1. Run the application: python run.py"
echo "2. Open browser to: http://localhost:5000"
echo ""
echo "To start the application, run:"
echo "  python run.py"
echo ""
