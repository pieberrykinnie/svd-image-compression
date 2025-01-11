const form = document.querySelector('form');
const output = document.querySelector('#comparison');
const loading = document.querySelector('#loading');
const qualityInput = document.querySelector('#quality');
const qualityValue = document.querySelector('#quality-value');
const originalImage = document.querySelector('#original-image');
const compressedImage = document.querySelector('#compressed-image');
const originalSize = document.querySelector('#original-size');
const compressedSize = document.querySelector('#compressed-size');

// Update quality value display
qualityInput.addEventListener('input', (e) => {
    qualityValue.textContent = e.target.value;
});

// Handle file selection
document.querySelector('#image').addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        originalImage.src = URL.createObjectURL(file);
        originalSize.textContent = formatFileSize(file.size);
        output.classList.remove('hidden');
    }
});

// Handle form submission
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    loading.classList.remove('hidden');
    
    const formData = new FormData(form);
    
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        compressedImage.src = data.compressed_path;
        compressedSize.textContent = data.compressed_size;
        output.classList.remove('hidden');
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while compressing the image.');
    } finally {
        loading.classList.add('hidden');
    }
});

// Handle drag and drop
const uploadLabel = document.querySelector('.upload-label');

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    uploadLabel.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
    uploadLabel.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
    uploadLabel.addEventListener(eventName, unhighlight, false);
});

function highlight(e) {
    uploadLabel.classList.add('highlight');
}

function unhighlight(e) {
    uploadLabel.classList.remove('highlight');
}

uploadLabel.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    const dt = e.dataTransfer;
    const file = dt.files[0];
    document.querySelector('#image').files = dt.files;
    originalImage.src = URL.createObjectURL(file);
    originalSize.textContent = formatFileSize(file.size);
    output.classList.remove('hidden');
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}