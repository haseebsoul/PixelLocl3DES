"""
PixelLock 3DES - Run Script
Simplified script to run the application
"""

import os
import sys
from pathlib import Path

# Add app directory to path
app_dir = Path(__file__).parent / 'app'
sys.path.insert(0, str(app_dir))

# Import and run Flask app
from app import app

if __name__ == '__main__':
    print("=" * 60)
    print("PixelLock 3DES - Secure Image Encryption System")
    print("=" * 60)
    print("\n✓ Starting Flask application...")
    print("\n📱 Access the application at: http://localhost:5000")
    print("\n⚠️  To stop the server, press Ctrl+C\n")
    print("=" * 60)
    
    # Run Flask app with debug enabled
    app.run(debug=True, host='0.0.0.0', port=5000)
