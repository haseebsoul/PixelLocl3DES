"""
Test Suite for PixelLock 3DES
Run tests using: python -m pytest tests.py -v
"""

import unittest
import sys
from pathlib import Path
from io import BytesIO
from PIL import Image

# Add app directory to path
app_dir = Path(__file__).parent / 'app'
sys.path.insert(0, str(app_dir))

from crypto_handler import CryptoHandler
from hash_handler import HashHandler


class TestCryptoHandler(unittest.TestCase):
    """Test cases for CryptoHandler"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.crypto = CryptoHandler()
    
    def test_generate_key(self):
        """Test key generation"""
        key = CryptoHandler.generate_key()
        self.assertIsNotNone(key)
        self.assertIsInstance(key, str)
        # Decode and check length
        decoded = __import__('base64').b64decode(key)
        self.assertEqual(len(decoded), 24)
    
    def test_validate_key(self):
        """Test key validation"""
        key = CryptoHandler.generate_key()
        validated_key = CryptoHandler.validate_key(key)
        self.assertIsNotNone(validated_key)
        self.assertEqual(len(validated_key), 24)
    
    def test_validate_key_invalid(self):
        """Test invalid key validation"""
        with self.assertRaises(ValueError):
            CryptoHandler.validate_key("invalid_key")
    
    def create_test_image(self):
        """Create a simple test image"""
        img = Image.new('RGB', (100, 100), color='red')
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        return img_byte_arr.getvalue()
    
    def test_encrypt_decrypt_cycle(self):
        """Test full encrypt-decrypt cycle"""
        key = CryptoHandler.generate_key()
        
        # Create test image
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp.write(self.create_test_image())
            tmp_path = tmp.name
        
        try:
            # Encrypt
            encrypt_result = CryptoHandler.encrypt_image(tmp_path, key)
            self.assertTrue(encrypt_result['success'])
            
            # Decrypt
            decrypt_result = CryptoHandler.decrypt_image(
                encrypt_result['encrypted_data'], 
                key
            )
            self.assertTrue(decrypt_result['success'])
            
        finally:
            import os
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


class TestHashHandler(unittest.TestCase):
    """Test cases for HashHandler"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.hash_handler = HashHandler()
    
    def create_test_image(self):
        """Create a simple test image"""
        img = Image.new('RGB', (100, 100), color='blue')
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        return img_byte_arr.getvalue()
    
    def test_generate_hash(self):
        """Test hash generation"""
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp.write(self.create_test_image())
            tmp_path = tmp.name
        
        try:
            result = HashHandler.generate_hash(tmp_path)
            self.assertTrue(result['success'])
            self.assertIn('hash', result)
            self.assertEqual(result['algorithm'], 'SHA-256')
        finally:
            import os
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    def test_generate_hash_from_data(self):
        """Test hash generation from data"""
        data = b"test data"
        result = HashHandler.generate_hash_from_data(data)
        self.assertTrue(result['success'])
        self.assertIn('hash', result)
        self.assertEqual(len(result['hash']), 64)  # SHA-256 produces 64 hex chars
    
    def test_verify_hash_match(self):
        """Test hash verification with matching hash"""
        data = b"test data"
        hash_result = HashHandler.generate_hash_from_data(data)
        
        verify_result = HashHandler.verify_hash_data(
            data, 
            hash_result['hash']
        )
        self.assertTrue(verify_result['success'])
        self.assertTrue(verify_result['matches'])
    
    def test_verify_hash_mismatch(self):
        """Test hash verification with non-matching hash"""
        data = b"test data"
        wrong_hash = "0" * 64
        
        verify_result = HashHandler.verify_hash_data(data, wrong_hash)
        self.assertTrue(verify_result['success'])
        self.assertFalse(verify_result['matches'])


class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_full_workflow(self):
        """Test complete encryption-decryption-verification workflow"""
        # Generate key
        key = CryptoHandler.generate_key()
        self.assertIsNotNone(key)
        
        # Generate test data
        test_data = b"test image data"
        
        # Generate hash of original
        hash_result = HashHandler.generate_hash_from_data(test_data)
        original_hash = hash_result['hash']
        self.assertTrue(hash_result['success'])
        
        # Verify hash
        verify_result = HashHandler.verify_hash_data(test_data, original_hash)
        self.assertTrue(verify_result['matches'])


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
