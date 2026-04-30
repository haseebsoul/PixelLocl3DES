"""
Cryptographic Handler Module
Handles 3DES encryption and decryption of image files
"""

from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
import os


class CryptoHandler:
    """
    Handles encryption and decryption using 3DES algorithm
    """
    
    # 3DES requires a 24-byte key (192 bits)
    KEY_SIZE = 24
    # DES3 block size
    BLOCK_SIZE = DES3.block_size
    
    def __init__(self):
        pass
    
    @staticmethod
    def generate_key():
        """
        Generate a random 3DES key (24 bytes)
        Returns the key in base64 format for easy storage
        """
        key = get_random_bytes(CryptoHandler.KEY_SIZE)
        return base64.b64encode(key).decode('utf-8')
    
    @staticmethod
    def validate_key(key_str):
        """
        Validate and decode a base64-encoded key
        Ensures it's the correct size for 3DES
        """
        try:
            key = base64.b64decode(key_str)
            if len(key) != CryptoHandler.KEY_SIZE:
                raise ValueError(f"Key must be {CryptoHandler.KEY_SIZE} bytes")
            return key
        except Exception as e:
            raise ValueError(f"Invalid key format: {str(e)}")
    
    @staticmethod
    def encrypt_image(image_path, key_str, output_path=None):
        """
        Encrypt an image file using 3DES
        
        Args:
            image_path: Path to the image file
            key_str: Base64-encoded 3DES key
            output_path: Optional path for encrypted output
            
        Returns:
            Dictionary with encrypted data and metadata
        """
        try:
            # Validate and decode key
            key = CryptoHandler.validate_key(key_str)
            
            # Read image file
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # Generate random IV
            iv = get_random_bytes(CryptoHandler.BLOCK_SIZE)
            
            # Create cipher
            cipher = DES3.new(key, DES3.MODE_CBC, iv)
            
            # Pad and encrypt
            padded_data = pad(image_data, CryptoHandler.BLOCK_SIZE)
            encrypted_data = cipher.encrypt(padded_data)
            
            # Combine IV + encrypted data for transmission
            encrypted_output = iv + encrypted_data
            
            # Save encrypted file if output path provided
            if output_path:
                with open(output_path, 'wb') as f:
                    f.write(encrypted_output)
            
            return {
                'success': True,
                'encrypted_data': base64.b64encode(encrypted_output).decode('utf-8'),
                'file_size': len(image_data),
                'encrypted_size': len(encrypted_output),
                'message': 'Image encrypted successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Encryption failed: {str(e)}'
            }
    
    @staticmethod
    def decrypt_image(encrypted_data_b64, key_str, output_path=None):
        """
        Decrypt an image file using 3DES
        
        Args:
            encrypted_data_b64: Base64-encoded encrypted data (IV + encrypted image)
            key_str: Base64-encoded 3DES key
            output_path: Optional path to save decrypted image
            
        Returns:
            Dictionary with decrypted data and metadata
        """
        try:
            # Validate and decode key
            key = CryptoHandler.validate_key(key_str)
            
            # Decode encrypted data
            encrypted_output = base64.b64decode(encrypted_data_b64)
            
            # Extract IV and encrypted data
            iv = encrypted_output[:CryptoHandler.BLOCK_SIZE]
            encrypted_data = encrypted_output[CryptoHandler.BLOCK_SIZE:]
            
            # Create cipher
            cipher = DES3.new(key, DES3.MODE_CBC, iv)
            
            # Decrypt and unpad
            decrypted_padded = cipher.decrypt(encrypted_data)
            decrypted_data = unpad(decrypted_padded, CryptoHandler.BLOCK_SIZE)
            
            # Save decrypted file if output path provided
            if output_path:
                with open(output_path, 'wb') as f:
                    f.write(decrypted_data)
            
            return {
                'success': True,
                'decrypted_data': base64.b64encode(decrypted_data).decode('utf-8'),
                'file_size': len(decrypted_data),
                'message': 'Image decrypted successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Decryption failed: {str(e)}'
            }
    
    @staticmethod
    def encrypt_image_file(input_path, output_path, key_str):
        """
        Encrypt an image file and save encrypted version
        """
        return CryptoHandler.encrypt_image(input_path, key_str, output_path)
    
    @staticmethod
    def decrypt_image_file(input_path, output_path, key_str):
        """
        Decrypt an image file and save decrypted version
        """
        try:
            with open(input_path, 'rb') as f:
                encrypted_output = f.read()
            
            key = CryptoHandler.validate_key(key_str)
            
            # Extract IV and encrypted data
            iv = encrypted_output[:CryptoHandler.BLOCK_SIZE]
            encrypted_data = encrypted_output[CryptoHandler.BLOCK_SIZE:]
            
            # Create cipher
            cipher = DES3.new(key, DES3.MODE_CBC, iv)
            
            # Decrypt and unpad
            decrypted_padded = cipher.decrypt(encrypted_data)
            decrypted_data = unpad(decrypted_padded, CryptoHandler.BLOCK_SIZE)
            
            # Save decrypted file
            with open(output_path, 'wb') as f:
                f.write(decrypted_data)
            
            return {
                'success': True,
                'file_size': len(decrypted_data),
                'message': 'Image decrypted successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Decryption failed: {str(e)}'
            }
