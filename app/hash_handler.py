"""
Hash Handler Module
Handles hash generation and verification for integrity checking
"""

import hashlib
import os


class HashHandler:
    """
    Handles hash generation and verification using SHA-256
    Ensures integrity of images
    """
    
    @staticmethod
    def generate_hash(file_path):
        """
        Generate SHA-256 hash of a file
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary with hash value and metadata
        """
        try:
            sha256_hash = hashlib.sha256()
            
            # Read file in chunks to handle large files
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    sha256_hash.update(chunk)
            
            hash_value = sha256_hash.hexdigest()
            
            return {
                'success': True,
                'hash': hash_value,
                'algorithm': 'SHA-256',
                'message': 'Hash generated successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Hash generation failed: {str(e)}'
            }
    
    @staticmethod
    def generate_hash_from_data(data):
        """
        Generate SHA-256 hash from binary data
        
        Args:
            data: Binary data
            
        Returns:
            Dictionary with hash value
        """
        try:
            if isinstance(data, str):
                data = data.encode('utf-8')
            
            sha256_hash = hashlib.sha256(data).hexdigest()
            
            return {
                'success': True,
                'hash': sha256_hash,
                'algorithm': 'SHA-256',
                'message': 'Hash generated successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Hash generation failed: {str(e)}'
            }
    
    @staticmethod
    def verify_hash(file_path, provided_hash):
        """
        Verify if a file matches the provided hash
        
        Args:
            file_path: Path to the file
            provided_hash: Hash to compare against
            
        Returns:
            Dictionary with verification result
        """
        try:
            result = HashHandler.generate_hash(file_path)
            
            if not result['success']:
                return result
            
            calculated_hash = result['hash']
            matches = calculated_hash.lower() == provided_hash.lower()
            
            return {
                'success': True,
                'matches': matches,
                'calculated_hash': calculated_hash,
                'provided_hash': provided_hash,
                'message': 'Hash verified successfully' if matches else 'Hash mismatch: File integrity compromised'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Hash verification failed: {str(e)}'
            }
    
    @staticmethod
    def verify_hash_data(data, provided_hash):
        """
        Verify if binary data matches the provided hash
        
        Args:
            data: Binary data
            provided_hash: Hash to compare against
            
        Returns:
            Dictionary with verification result
        """
        try:
            result = HashHandler.generate_hash_from_data(data)
            
            if not result['success']:
                return result
            
            calculated_hash = result['hash']
            matches = calculated_hash.lower() == provided_hash.lower()
            
            return {
                'success': True,
                'matches': matches,
                'calculated_hash': calculated_hash,
                'provided_hash': provided_hash,
                'message': 'Integrity verified successfully' if matches else 'Integrity check failed'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Integrity verification failed: {str(e)}'
            }
    
    @staticmethod
    def generate_multiple_hashes(file_path):
        """
        Generate multiple hash types for a file
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary with multiple hash values
        """
        try:
            sha256_hash = hashlib.sha256()
            sha1_hash = hashlib.sha1()
            md5_hash = hashlib.md5()
            
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    sha256_hash.update(chunk)
                    sha1_hash.update(chunk)
                    md5_hash.update(chunk)
            
            return {
                'success': True,
                'SHA-256': sha256_hash.hexdigest(),
                'SHA-1': sha1_hash.hexdigest(),
                'MD5': md5_hash.hexdigest(),
                'message': 'All hashes generated successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Multi-hash generation failed: {str(e)}'
            }
