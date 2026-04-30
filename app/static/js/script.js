// ================================================
// PixelLock 3DES - Frontend Script
// ================================================

// State Management
const state = {
    currentFile: null,
    currentFileVerify: null,
    encryptedData: null,
    decryptedData: null
};

// DOM Elements
const elements = {
    // Tab buttons
    tabButtons: document.querySelectorAll('.tab-button'),
    
    // Encryption Elements
    generateKeyBtn: document.getElementById('generateKeyBtn'),
    encryptionKey: document.getElementById('encryptionKey'),
    copyKeyBtn: document.getElementById('copyKeyBtn'),
    fileUploadArea: document.getElementById('fileUploadArea'),
    encryptImageInput: document.getElementById('encryptImageInput'),
    uploadedFileName: document.getElementById('uploadedFileName'),
    fileName: document.getElementById('fileName'),
    encryptBtn: document.getElementById('encryptBtn'),
    encryptResults: document.getElementById('encryptResults'),
    encryptedDataOutput: document.getElementById('encryptedDataOutput'),
    downloadEncryptedBtn: document.getElementById('downloadEncryptedBtn'),
    copyEncryptedBtn: document.getElementById('copyEncryptedBtn'),
    
    // Decryption Elements
    decryptionKey: document.getElementById('decryptionKey'),
    encryptedDataInput: document.getElementById('encryptedDataInput'),
    decryptBtn: document.getElementById('decryptBtn'),
    decryptResults: document.getElementById('decryptResults'),
    decryptedImagePreview: document.getElementById('decryptedImagePreview'),
    downloadDecryptedBtn: document.getElementById('downloadDecryptedBtn'),
    
    // Verification Elements
    fileUploadAreaVerify: document.getElementById('fileUploadAreaVerify'),
    verifyImageInput: document.getElementById('verifyImageInput'),
    uploadedFileNameVerify: document.getElementById('uploadedFileNameVerify'),
    fileNameVerify: document.getElementById('fileNameVerify'),
    expectedHash: document.getElementById('expectedHash'),
    verifyBtn: document.getElementById('verifyBtn'),
    verifyResults: document.getElementById('verifyResults'),
    
    // Notifications
    notification: document.getElementById('notification'),
    loadingSpinner: document.getElementById('loadingSpinner')
};

// ================================================
// Utility Functions
// ================================================

function showNotification(message, type = 'success') {
    const notification = elements.notification;
    notification.textContent = message;
    notification.className = `notification ${type}`;
    notification.style.display = 'block';
    
    setTimeout(() => {
        notification.style.display = 'none';
    }, 4000);
}

function showLoadingSpinner(show = true) {
    elements.loadingSpinner.style.display = show ? 'flex' : 'none';
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard!', 'success');
    }).catch(() => {
        showNotification('Failed to copy to clipboard', 'error');
    });
}

function downloadFile(dataUrl, filename) {
    const link = document.createElement('a');
    link.href = dataUrl;
    link.download = filename;
    link.click();
}

// ================================================
// Tab Navigation
// ================================================

elements.tabButtons.forEach(button => {
    button.addEventListener('click', () => {
        // Remove active class from all buttons and contents
        elements.tabButtons.forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        
        // Add active class to clicked button and corresponding content
        button.classList.add('active');
        const tabName = button.getAttribute('data-tab');
        document.getElementById(tabName).classList.add('active');
    });
});

// ================================================
// Key Management
// ================================================

elements.generateKeyBtn.addEventListener('click', async () => {
    showLoadingSpinner(true);
    try {
        const response = await fetch('/api/generate-key', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            elements.encryptionKey.value = data.key;
            showNotification('Key generated successfully!', 'success');
        } else {
            showNotification(data.message, 'error');
        }
    } catch (error) {
        showNotification('Error generating key: ' + error.message, 'error');
    } finally {
        showLoadingSpinner(false);
    }
});

elements.copyKeyBtn.addEventListener('click', () => {
    const key = elements.encryptionKey.value;
    if (key) {
        copyToClipboard(key);
    } else {
        showNotification('No key to copy', 'warning');
    }
});

// ================================================
// File Upload Handling
// ================================================

function setupFileUploadArea(uploadArea, fileInput) {
    uploadArea.addEventListener('click', () => fileInput.click());
    
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.background = 'rgba(37, 99, 235, 0.15)';
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.background = 'rgba(37, 99, 235, 0.05)';
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.background = 'rgba(37, 99, 235, 0.05)';
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            fileInput.dispatchEvent(new Event('change'));
        }
    });
}

setupFileUploadArea(elements.fileUploadArea, elements.encryptImageInput);
setupFileUploadArea(elements.fileUploadAreaVerify, elements.verifyImageInput);

elements.encryptImageInput.addEventListener('change', function() {
    if (this.files.length > 0) {
        state.currentFile = this.files[0];
        elements.fileName.textContent = this.files[0].name;
        elements.uploadedFileName.style.display = 'block';
        elements.encryptBtn.disabled = false;
    }
});

elements.verifyImageInput.addEventListener('change', function() {
    if (this.files.length > 0) {
        state.currentFileVerify = this.files[0];
        elements.fileNameVerify.textContent = this.files[0].name;
        elements.uploadedFileNameVerify.style.display = 'block';
        elements.verifyBtn.disabled = false;
    }
});

// ================================================
// Encryption
// ================================================

elements.encryptBtn.addEventListener('click', async () => {
    const key = elements.encryptionKey.value;
    
    if (!key) {
        showNotification('Please generate or provide an encryption key', 'warning');
        return;
    }
    
    if (!state.currentFile) {
        showNotification('Please select an image file', 'warning');
        return;
    }
    
    showLoadingSpinner(true);
    
    try {
        const formData = new FormData();
        formData.append('file', state.currentFile);
        formData.append('key', key);
        
        const response = await fetch('/api/encrypt', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            state.encryptedData = data.encrypted_data;
            
            // Display results
            document.getElementById('originalSize').textContent = formatFileSize(data.file_size);
            document.getElementById('encryptedSize').textContent = formatFileSize(data.encrypted_size);
            document.getElementById('encryptedHash').textContent = data.original_hash;
            elements.encryptedDataOutput.value = data.encrypted_data;
            
            elements.encryptResults.style.display = 'block';
            showNotification('Image encrypted successfully!', 'success');
        } else {
            showNotification(data.message, 'error');
        }
    } catch (error) {
        showNotification('Encryption error: ' + error.message, 'error');
    } finally {
        showLoadingSpinner(false);
    }
});

elements.copyEncryptedBtn.addEventListener('click', () => {
    if (state.encryptedData) {
        copyToClipboard(state.encryptedData);
    } else {
        showNotification('No encrypted data to copy', 'warning');
    }
});

elements.downloadEncryptedBtn.addEventListener('click', () => {
    if (state.encryptedData) {
        const blob = new Blob([state.encryptedData], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        downloadFile(url, 'encrypted_image.txt');
        URL.revokeObjectURL(url);
    } else {
        showNotification('No encrypted data to download', 'warning');
    }
});

// ================================================
// Decryption
// ================================================

elements.decryptBtn.addEventListener('click', async () => {
    const key = elements.decryptionKey.value;
    const encryptedData = elements.encryptedDataInput.value;
    
    if (!key) {
        showNotification('Please provide a decryption key', 'warning');
        return;
    }
    
    if (!encryptedData) {
        showNotification('Please provide encrypted data', 'warning');
        return;
    }
    
    showLoadingSpinner(true);
    
    try {
        const response = await fetch('/api/decrypt', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                encrypted_data: encryptedData,
                key: key
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            state.decryptedData = data.decrypted_data;
            
            // Display results
            document.getElementById('decryptedSize').textContent = formatFileSize(data.file_size);
            document.getElementById('decryptedHash').textContent = data.decrypted_hash;
            
            // Display image preview
            const imageUrl = 'data:image/png;base64,' + data.decrypted_data;
            elements.decryptedImagePreview.src = imageUrl;
            
            elements.decryptResults.style.display = 'block';
            showNotification('Image decrypted successfully!', 'success');
        } else {
            showNotification(data.message, 'error');
        }
    } catch (error) {
        showNotification('Decryption error: ' + error.message, 'error');
    } finally {
        showLoadingSpinner(false);
    }
});

elements.downloadDecryptedBtn.addEventListener('click', () => {
    if (state.decryptedData) {
        const byteCharacters = atob(state.decryptedData);
        const byteNumbers = new Array(byteCharacters.length);
        for (let i = 0; i < byteCharacters.length; i++) {
            byteNumbers[i] = byteCharacters.charCodeAt(i);
        }
        const byteArray = new Uint8Array(byteNumbers);
        const blob = new Blob([byteArray], { type: 'image/png' });
        const url = URL.createObjectURL(blob);
        downloadFile(url, 'decrypted_image.png');
        URL.revokeObjectURL(url);
    } else {
        showNotification('No decrypted image to download', 'warning');
    }
});

// ================================================
// Hash Verification
// ================================================

elements.verifyBtn.addEventListener('click', async () => {
    const expectedHash = elements.expectedHash.value;
    
    if (!state.currentFileVerify) {
        showNotification('Please select an image file', 'warning');
        return;
    }
    
    if (!expectedHash) {
        showNotification('Please provide an expected hash', 'warning');
        return;
    }
    
    showLoadingSpinner(true);
    
    try {
        const fileReader = new FileReader();
        
        fileReader.onload = async (e) => {
            const arrayBuffer = e.target.result;
            const byteArray = new Uint8Array(arrayBuffer);
            let binaryString = '';
            
            for (let i = 0; i < byteArray.byteLength; i++) {
                binaryString += String.fromCharCode(byteArray[i]);
            }
            
            const base64Data = btoa(binaryString);
            
            try {
                const response = await fetch('/api/verify-hash', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        image_data: base64Data,
                        hash: expectedHash
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    const verificationStatus = document.getElementById('verificationStatus');
                    
                    if (data.matches) {
                        verificationStatus.className = 'verification-status success';
                        verificationStatus.innerHTML = '<i class="fas fa-check-circle"></i> Image integrity verified! Hash matches.';
                    } else {
                        verificationStatus.className = 'verification-status failed';
                        verificationStatus.innerHTML = '<i class="fas fa-times-circle"></i> Integrity check failed! Hash does not match.';
                    }
                    
                    document.getElementById('calculatedHash').textContent = data.calculated_hash;
                    document.getElementById('displayedHash').textContent = data.provided_hash;
                    
                    elements.verifyResults.style.display = 'block';
                    
                    if (data.matches) {
                        showNotification('Hash verification successful!', 'success');
                    } else {
                        showNotification('Hash verification failed!', 'error');
                    }
                } else {
                    showNotification(data.message, 'error');
                }
            } catch (error) {
                showNotification('Hash verification error: ' + error.message, 'error');
            } finally {
                showLoadingSpinner(false);
            }
        };
        
        fileReader.readAsArrayBuffer(state.currentFileVerify);
    } catch (error) {
        showNotification('File reading error: ' + error.message, 'error');
        showLoadingSpinner(false);
    }
});

// ================================================
// Initialize
// ================================================

document.addEventListener('DOMContentLoaded', () => {
    showNotification('Welcome to PixelLock 3DES!', 'success');
});
