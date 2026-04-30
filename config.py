# Configuration file for PixelLock 3DES

# Flask Configuration
DEBUG = True
TESTING = False
SECRET_KEY = 'your-secret-key-change-in-production'

# Upload Configuration
UPLOAD_FOLDER = 'app/uploads'
ENCRYPTED_FOLDER = 'app/encrypted_images'
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# Allowed Extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'tiff'}

# Server Configuration
HOST = '0.0.0.0'
PORT = 5000

# Encryption Configuration
ENCRYPTION_ALGORITHM = '3DES'
KEY_SIZE = 24  # 192 bits
BLOCK_SIZE = 8  # 64 bits

# Hashing Configuration
HASH_ALGORITHM = 'SHA-256'
