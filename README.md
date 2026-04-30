# PixelLock 3DES - Secure Image Encryption & Decryption System

## Overview

**PixelLock 3DES** is a comprehensive web-based image encryption and decryption system designed to ensure confidentiality and integrity of visual data. It leverages the **Triple DES (3DES)** encryption algorithm and **SHA-256** hashing to provide military-grade security for sensitive images.

## Project Purpose

With rising concerns about data leakage, identity misuse, and unauthorized image manipulation, PixelLock 3DES serves as:
- A practical demonstration of applying cryptographic techniques to real-world multimedia content
- A secure mechanism for storing and transferring image files while maintaining confidentiality
- An academic project showcasing Information Security principles

## Key Features

### 🔐 Security Features
- **Triple DES (3DES) Encryption**: 192-bit keys (24 bytes) for strong confidentiality
- **CBC Mode**: Cipher Block Chaining with random initialization vectors (IVs)
- **SHA-256 Hashing**: Integrity verification and authenticity checking
- **Secure Key Generation**: Cryptographically secure random key generation
- **Padding**: PKCS7 padding for robust encryption

### 🎨 User Interface
- **Modern Web-Based UI**: Built with HTML5, CSS3, and Vanilla JavaScript
- **Dark Theme**: Eye-friendly interface with professional design
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Real-time Feedback**: Immediate notifications and visual feedback

### ⚙️ Core Functionality
1. **Image Encryption**: Convert plaintext images to encrypted format
2. **Image Decryption**: Recover original images using correct keys
3. **Hash Generation**: Generate SHA-256 hashes for integrity verification
4. **Hash Verification**: Verify image authenticity and detect tampering
5. **Multi-Hash Support**: Generate SHA-256, SHA-1, and MD5 hashes

## System Architecture

```
PixelLock-3DES/
├── app/
│   ├── app.py                    # Flask application (main backend)
│   ├── crypto_handler.py         # 3DES encryption/decryption logic
│   ├── hash_handler.py           # Hash generation and verification
│   ├── templates/
│   │   └── index.html            # Main web interface
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css         # Styling
│   │   └── js/
│   │       └── script.js         # Frontend logic
│   ├── uploads/                  # Temporary upload folder
│   └── encrypted_images/         # Encrypted image storage
├── requirements.txt              # Python dependencies
└── README.md                     # Documentation
```

## Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend Framework** | Flask (Python) |
| **Encryption** | PyCryptodome (3DES) |
| **Hashing** | hashlib (SHA-256, SHA-1, MD5) |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Server** | Werkzeug (Flask's WSGI server) |
| **UI Framework** | Custom CSS with FontAwesome icons |

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- A modern web browser

### Step 1: Clone/Download Repository
```bash
# Navigate to the project directory
cd path/to/PixelLock-3DES
```

### Step 2: Create Virtual Environment (Optional but Recommended)
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
# Navigate to the app directory
cd app

# Run Flask application
python app.py
```

The application will start on `http://localhost:5000`

## Usage Guide

### 🔒 Encrypting an Image

1. **Generate or Provide Key**
   - Click "Generate New Key" to create a new encryption key
   - Save the key securely (you'll need it to decrypt)

2. **Select Image**
   - Upload an image (PNG, JPG, GIF, BMP, WebP, TIFF)
   - Maximum file size: 50MB

3. **Encrypt**
   - Click "Encrypt Image" button
   - Wait for the encryption process to complete

4. **Save Results**
   - Download the encrypted file or copy the encrypted data
   - Store the encryption key and encrypted data securely

### 🔓 Decrypting an Image

1. **Provide Key and Data**
   - Paste your decryption key
   - Paste the encrypted image data (Base64)

2. **Decrypt**
   - Click "Decrypt Image" button
   - System will decrypt and display the image

3. **Download**
   - View the decrypted image preview
   - Download the decrypted image file

### ✅ Verifying Image Integrity

1. **Select Image**
   - Upload the image you want to verify

2. **Provide Expected Hash**
   - Paste the expected SHA-256 hash value

3. **Verify**
   - Click "Verify Integrity" button
   - System confirms if hash matches

## Security Specifications

### 3DES Algorithm Details
- **Key Size**: 192 bits (24 bytes)
- **Block Size**: 64 bits (8 bytes)
- **Mode**: Cipher Block Chaining (CBC)
- **IV**: Random 64-bit initialization vector
- **Padding**: PKCS7

### SHA-256 Hash
- **Output**: 256 bits (32 bytes / 64 hex characters)
- **Purpose**: Integrity verification and authenticity checking

### Security Best Practices
1. **Key Management**
   - Generate new keys for each encryption
   - Store keys in secure, separate locations
   - Never share keys over insecure channels

2. **File Handling**
   - Use secure file upload mechanisms
   - Implement proper access controls
   - Regularly audit file access logs

3. **Communication**
   - Use HTTPS for all communications (in production)
   - Encrypt keys before transmission
   - Use secure channels for key exchange

## API Endpoints

### POST /api/generate-key
Generate a new 3DES encryption key.

**Response:**
```json
{
    "success": true,
    "key": "base64_encoded_key",
    "message": "Key generated successfully"
}
```

### POST /api/encrypt
Encrypt an image file.

**Form Data:**
- `file`: Image file (multipart/form-data)
- `key`: Base64-encoded encryption key

**Response:**
```json
{
    "success": true,
    "encrypted_data": "base64_encoded_encrypted_data",
    "original_hash": "sha256_hash",
    "file_size": 12345,
    "encrypted_size": 12352
}
```

### POST /api/decrypt
Decrypt an encrypted image.

**JSON Body:**
```json
{
    "encrypted_data": "base64_encoded_encrypted_data",
    "key": "base64_encoded_key"
}
```

**Response:**
```json
{
    "success": true,
    "decrypted_data": "base64_encoded_image_data",
    "decrypted_hash": "sha256_hash",
    "file_size": 12345
}
```

### POST /api/verify-hash
Verify image integrity using hash.

**JSON Body:**
```json
{
    "image_data": "base64_encoded_image",
    "hash": "expected_sha256_hash"
}
```

**Response:**
```json
{
    "success": true,
    "matches": true,
    "calculated_hash": "calculated_hash",
    "provided_hash": "provided_hash"
}
```

### POST /api/generate-hash
Generate hash for image data.

**JSON Body:**
```json
{
    "image_data": "base64_encoded_image"
}
```

**Response:**
```json
{
    "success": true,
    "hash": "sha256_hash",
    "algorithm": "SHA-256"
}
```

## Error Handling

The system provides comprehensive error handling:

| Error Code | Meaning |
|-----------|---------|
| 400 | Bad Request - Invalid input or missing parameters |
| 404 | Not Found - Resource does not exist |
| 413 | Payload Too Large - File exceeds 50MB limit |
| 500 | Internal Server Error - Server-side processing error |

## File Size Limitations

- **Maximum File Size**: 50MB per image
- **Supported Formats**: PNG, JPG/JPEG, GIF, BMP, WebP, TIFF

## Performance Considerations

- **Encryption Time**: Varies with image size (typically < 1 second for most images)
- **Memory Usage**: Approximately 2-3x the image size during processing
- **Network**: Large files should use compression for faster transmission

## Deployment

### Development Server
```bash
python app.py
```

### Production Deployment

For production use, consider:

1. **Use Production WSGI Server**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

2. **Enable HTTPS**
```bash
# Use a reverse proxy like Nginx with SSL
```

3. **Environment Configuration**
```bash
# Create .env file
FLASK_ENV=production
DEBUG=False
SECRET_KEY=your_secret_key
```

4. **Security Headers**
   - Set proper CORS policies
   - Implement rate limiting
   - Add security headers (CSP, X-Frame-Options, etc.)

## Testing

### Manual Testing
1. Generate a key
2. Encrypt a test image
3. Decrypt using the same key
4. Verify hash matches original

### Test Image Formats
- PNG (8-bit, 24-bit, 32-bit)
- JPEG (baseline, progressive)
- GIF (static, animated)
- BMP
- WebP
- TIFF

## Troubleshooting

### Issue: "Key must be 24 bytes"
**Solution**: Generate a new key using the application.

### Issue: "Decryption failed"
**Possible Causes:**
- Wrong decryption key used
- Encrypted data corrupted
- Invalid Base64 format

### Issue: "Hash mismatch"
**Meaning**: Image integrity may be compromised or wrong hash provided.

### Issue: "File too large"
**Solution**: Reduce image file size or compression (under 50MB limit).

## Limitations

1. **Key Management**: Keys are stored as Base64 in memory
2. **File Size**: Limited to 50MB per image
3. **Processing Speed**: Large files may take longer to process
4. **Single Key Use**: Each encryption uses its own key

## Future Enhancements

- [ ] Support for batch processing
- [ ] User authentication and account management
- [ ] Cloud storage integration
- [ ] Advanced key management with KMS
- [ ] Video encryption support
- [ ] Mobile app development
- [ ] GPU acceleration for faster processing
- [ ] Web Worker implementation for background processing

## Security Audit

This system implements standard cryptographic practices:
- ✅ 3DES with 192-bit keys
- ✅ CBC mode with random IVs
- ✅ PKCS7 padding
- ✅ SHA-256 integrity verification
- ✅ Secure random number generation

## References

- [NIST SP 800-38A - Recommendation for Block Cipher Modes](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38a.pdf)
- [Triple DES (3DES) Standard](https://en.wikipedia.org/wiki/Triple_DES)
- [SHA-256 Standard](https://en.wikipedia.org/wiki/SHA-2)
- [PyCryptodome Documentation](https://pycryptodome.readthedocs.io/)
- [OWASP Cryptographic Failures](https://owasp.org/Top10/A02_2021-Cryptographic_Failures/)

## Code Examples

### Encrypting an Image Programmatically

```python
from crypto_handler import CryptoHandler
from hash_handler import HashHandler

# Generate key
key = CryptoHandler.generate_key()

# Encrypt image
result = CryptoHandler.encrypt_image_file(
    input_path='image.png',
    output_path='encrypted_image.enc',
    key_str=key
)

# Generate hash
hash_result = HashHandler.generate_hash('image.png')
print(f"Hash: {hash_result['hash']}")
```

### Decrypting an Image Programmatically

```python
from crypto_handler import CryptoHandler

# Decrypt image
result = CryptoHandler.decrypt_image_file(
    input_path='encrypted_image.enc',
    output_path='decrypted_image.png',
    key_str=key
)
```

### Verifying Image Integrity

```python
from hash_handler import HashHandler

# Verify hash
result = HashHandler.verify_hash(
    file_path='image.png',
    provided_hash='expected_hash_value'
)

if result['matches']:
    print("Image integrity verified!")
else:
    print("Integrity check failed!")
```

## Contributing

To contribute to PixelLock 3DES:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is provided under the MIT License - see LICENSE file for details.

## Author

**PixelLock 3DES Development Team**
- Information Security Course Project
- December 2025

## Support

For issues, questions, or suggestions:
- Check the Troubleshooting section
- Review the API documentation
- Examine the code comments

## Acknowledgments

- PyCryptodome library developers
- Flask framework creators
- FontAwesome icon library
- Academic advisors and reviewers

---

**Note**: This system is designed for educational and demonstration purposes. For production use with sensitive data, additional security measures and professional review are recommended.

**Last Updated**: December 18, 2025
**Version**: 1.0.0
