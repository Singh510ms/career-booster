document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const fileUpload = document.querySelector('.file-upload');
    
    // Add drag and drop functionality
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        fileUpload.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ['dragenter', 'dragover'].forEach(eventName => {
        fileUpload.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        fileUpload.addEventListener(eventName, unhighlight, false);
    });
    
    function highlight() {
        fileUpload.classList.add('highlight');
    }
    
    function unhighlight() {
        fileUpload.classList.remove('highlight');
    }
    
    fileUpload.addEventListener('drop', handleDrop, false);
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        const fileInput = document.getElementById('resume');
        
        if (files.length > 0 && files[0].type === 'application/pdf') {
            fileInput.files = files;
            document.getElementById('fileLabel').textContent = files[0].name;
        } else {
            alert('Please upload a PDF file.');
        }
    }
    
    // Form submission
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Validate form
        const fileInput = document.getElementById('resume');
        const jobUrl = document.getElementById('job_url').value;
        
        if (!fileInput.files[0]) {
            alert('Please upload your resume.');
            return;
        }
        
        if (!jobUrl) {
            alert('Please enter a job posting URL.');
            return;
        }
        
        // Create FormData object
        const formData = new FormData(uploadForm);
        
        // Show loading state
        window.location.href = '/processing';
        
        // Submit form
        fetch('/process', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Redirect to results page
            window.location.href = '/results';
        })
        .catch(error => {
            console.error('Error:', error);
            alert('There was an error processing your request. Please try again.');
            window.location.href = '/';
        });
    });
}); 