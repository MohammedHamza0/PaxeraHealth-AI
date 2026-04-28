let currentFile = null;
let originalImageUrl = null;
let maskImageUrl = null;

const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-upload');
const predictBtn = document.getElementById('predict-btn');

// Get base API URL - use same origin (backend serves both frontend and API)
const API_BASE_URL = window.location.origin;

async function loadTestImage() {
    try {
        console.log(`Attempting to fetch test image from: ${API_BASE_URL}/test_image.png`);
        const response = await fetch(`${API_BASE_URL}/test_image.png`);
        console.log(`Response status: ${response.status}`);
        
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Failed to fetch test image (${response.status}): ${errorText}`);
        }
        
        const blob = await response.blob();
        const file = new File([blob], 'test_image.png', { type: 'image/png' });

        // Use DataTransfer to mock the file input
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        fileInput.files = dataTransfer.files;

        handleFileSelect({ target: fileInput });
    } catch (e) {
        console.error('Failed to load test image:', e);
        alert(`Failed to load test image: ${e.message}\n\nMake sure the backend server is running and accessible.`);
    }
}

// Drag and drop setup
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => {
        dropZone.classList.add('border-paxera-orange', 'bg-paxera-orange/10');
    });
});

['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => {
        dropZone.classList.remove('border-paxera-orange', 'bg-paxera-orange/10');
    });
});

dropZone.addEventListener('drop', (e) => {
    const dt = e.dataTransfer;
    const files = dt.files;
    if (files.length > 0) {
        fileInput.files = files;
        handleFileSelect({ target: fileInput });
    }
});

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (!file) return;

    if (!file.type.startsWith('image/')) {
        alert('Please select an image file.');
        return;
    }

    currentFile = file;

    if (originalImageUrl) {
        URL.revokeObjectURL(originalImageUrl);
    }

    originalImageUrl = URL.createObjectURL(file);

    // Update preview with original image
    document.getElementById('original-img').src = originalImageUrl;
    document.getElementById('overlay-original').src = originalImageUrl;

    // Update UI state
    document.getElementById('empty-state').classList.add('hidden');
    document.getElementById('results-view').classList.remove('hidden');

    // Clear previous mask if any
    document.getElementById('mask-img').src = '';
    document.getElementById('overlay-mask').src = '';

    // Enable button
    predictBtn.disabled = false;

    // Update drop zone text
    dropZone.querySelector('.text-paxera-orange').textContent = file.name;
}

function toggleView(viewType) {
    const splitView = document.getElementById('split-view');
    const overlayView = document.getElementById('overlay-view');

    if (viewType === 'split') {
        splitView.classList.remove('hidden');
        overlayView.classList.add('hidden');
    } else {
        splitView.classList.add('hidden');
        overlayView.classList.remove('hidden');
    }
}

async function runPrediction() {
    if (!currentFile) return;

    const modelType = document.querySelector('input[name="model_type"]:checked').value;

    const formData = new FormData();
    formData.append('file', currentFile);
    formData.append('model_type', modelType);

    // Show loading
    const loadingState = document.getElementById('loading-state');
    loadingState.classList.remove('hidden');
    loadingState.style.display = 'flex';
    predictBtn.disabled = true;

    try {
        console.log(`Sending prediction request to: ${API_BASE_URL}/predict with model_type: ${modelType}`);
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            body: formData
        });

        console.log(`Response status: ${response.status}`);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error(`Error response: ${errorText}`);
            throw new Error(`Prediction failed (${response.status}): ${errorText}`);
        }

        const blob = await response.blob();
        
        // Revoke previous mask URL to prevent memory leaks
        if (maskImageUrl) {
            URL.revokeObjectURL(maskImageUrl);
        }
        
        maskImageUrl = URL.createObjectURL(blob);

        document.getElementById('mask-img').src = maskImageUrl;
        document.getElementById('overlay-mask').src = maskImageUrl;

    } catch (error) {
        console.error('Error:', error);
        alert(`Error: ${error.message}`);
    } finally {
        // Hide loading
        loadingState.classList.add('hidden');
        loadingState.style.display = 'none';
        predictBtn.disabled = false;
    }
}
