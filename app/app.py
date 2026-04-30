"""
PixelLock 3DES - Secure Image Encryption & Decryption System
Main Flask Application
"""

from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from crypto_handler import CryptoHandler
from hash_handler import HashHandler
import os
import base64
from pathlib import Path

# Initialize Flask app
app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ENCRYPTED_FOLDER = os.path.join(os.path.dirname(__file__), 'encrypted_images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'tiff'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ENCRYPTED_FOLDER'] = ENCRYPTED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ENCRYPTED_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/generate-key', methods=['POST'])
def generate_key():
    """Generate a new 3DES key"""
    try:
        key = CryptoHandler.generate_key()
        return jsonify({
            'success': True,
            'key': key,
            'message': 'Key generated successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error generating key: {str(e)}'
        }), 500


@app.route('/api/encrypt', methods=['POST'])
def encrypt_image():
    """Encrypt an uploaded image"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'message': 'No file provided'
            }), 400
        
        file = request.files['file']
        key = request.form.get('key')
        
        if not key:
            return jsonify({
                'success': False,
                'message': 'No encryption key provided'
            }), 400
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'message': 'No file selected'
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'message': 'File type not allowed. Supported: ' + ', '.join(ALLOWED_EXTENSIONS)
            }), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        upload_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(upload_path)
        
        # Generate hash of original image
        hash_result = HashHandler.generate_hash(upload_path)
        
        # Encrypt image
        encrypt_result = CryptoHandler.encrypt_image(upload_path, key)
        
        if encrypt_result['success']:
            # Generate encrypted filename
            encrypted_filename = f"encrypted_{filename}.enc"
            encrypted_path = os.path.join(ENCRYPTED_FOLDER, encrypted_filename)
            
            # Decode and save encrypted data
            encrypted_data = base64.b64decode(encrypt_result['encrypted_data'])
            with open(encrypted_path, 'wb') as f:
                f.write(encrypted_data)
            
            # Clean up uploaded file
            if os.path.exists(upload_path):
                os.remove(upload_path)
            
            return jsonify({
                'success': True,
                'encrypted_data': encrypt_result['encrypted_data'],
                'encrypted_filename': encrypted_filename,
                'original_hash': hash_result['hash'],
                'file_size': encrypt_result['file_size'],
                'encrypted_size': encrypt_result['encrypted_size'],
                'message': 'Image encrypted successfully'
            })
        else:
            return jsonify(encrypt_result), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Encryption error: {str(e)}'
        }), 500


@app.route('/api/decrypt', methods=['POST'])
def decrypt_image():
    """Decrypt an encrypted image"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        encrypted_data = data.get('encrypted_data')
        key = data.get('key')
        
        if not encrypted_data or not key:
            return jsonify({
                'success': False,
                'message': 'Missing encrypted data or key'
            }), 400
        
        # Decrypt image
        decrypt_result = CryptoHandler.decrypt_image(encrypted_data, key)
        
        if decrypt_result['success']:
            # Generate hash of decrypted image
            decrypted_bytes = base64.b64decode(decrypt_result['decrypted_data'])
            hash_result = HashHandler.generate_hash_from_data(decrypted_bytes)
            
            return jsonify({
                'success': True,
                'decrypted_data': decrypt_result['decrypted_data'],
                'decrypted_hash': hash_result['hash'],
                'file_size': decrypt_result['file_size'],
                'message': 'Image decrypted successfully'
            })
        else:
            return jsonify(decrypt_result), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Decryption error: {str(e)}'
        }), 500


@app.route('/api/verify-hash', methods=['POST'])
def verify_hash():
    """Verify image integrity using hash"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        image_data = data.get('image_data')
        provided_hash = data.get('hash')
        
        if not image_data or not provided_hash:
            return jsonify({
                'success': False,
                'message': 'Missing image data or hash'
            }), 400
        
        # Decode image data
        image_bytes = base64.b64decode(image_data)
        
        # Verify hash
        verify_result = HashHandler.verify_hash_data(image_bytes, provided_hash)
        
        return jsonify(verify_result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Hash verification error: {str(e)}'
        }), 500


@app.route('/api/generate-hash', methods=['POST'])
def generate_hash():
    """Generate hash for image data"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        image_data = data.get('image_data')
        
        if not image_data:
            return jsonify({
                'success': False,
                'message': 'No image data provided'
            }), 400
        
        # Decode image data
        image_bytes = base64.b64decode(image_data)
        
        # Generate hash
        hash_result = HashHandler.generate_hash_from_data(image_bytes)
        
        return jsonify(hash_result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Hash generation error: {str(e)}'
        }), 500


@app.route('/api/file-info', methods=['POST'])
def get_file_info():
    """Get file information"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        image_data = data.get('image_data')
        
        if not image_data:
            return jsonify({
                'success': False,
                'message': 'No image data provided'
            }), 400
        
        # Decode image data
        image_bytes = base64.b64decode(image_data)
        
        # Get multiple hashes
        hashes = HashHandler.generate_multiple_hashes.__code__
        
        return jsonify({
            'success': True,
            'file_size': len(image_bytes),
            'size_kb': round(len(image_bytes) / 1024, 2),
            'size_mb': round(len(image_bytes) / (1024 * 1024), 2)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error getting file info: {str(e)}'
        }), 500


@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({
        'success': False,
        'message': 'File size exceeds maximum allowed size (50MB)'
    }), 413


@app.errorhandler(404)
def not_found(e):
    """Handle 404 error"""
    return jsonify({
        'success': False,
        'message': 'Resource not found'
    }), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 error"""
    return jsonify({
        'success': False,
        'message': 'Internal server error'
    }), 500


if __name__ == '__main__':
    # Run the Flask app
    # Set debug=False for production
    app.run(debug=True, host='0.0.0.0', port=5000)
