document.addEventListener('DOMContentLoaded', function() {
    const progressBar = document.getElementById('progress-bar');
    const statusMessage = document.getElementById('status-message');
    const errorContainer = document.getElementById('error-container');
    const errorMessage = document.getElementById('error-message');
    
    // Start progress animation
    progressBar.style.width = '0%';
    setTimeout(() => {
        progressBar.style.animation = 'progress 30s linear forwards';
    }, 500);
    
    // Update status messages over time
    const messages = [
        { time: 0, text: 'Initializing agents...' },
        { time: 3000, text: 'Analyzing resume...' },
        { time: 8000, text: 'Fetching job description...' },
        { time: 12000, text: 'Generating project ideas...' },
        { time: 20000, text: 'Creating platform prompts...' },
        { time: 28000, text: 'Finalizing results...' }
    ];
    
    messages.forEach(msg => {
        setTimeout(() => {
            statusMessage.textContent = msg.text;
        }, msg.time);
    });
    
    // Make AJAX call to generate results
    fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || 'An unknown error occurred');
            });
        }
        return response.json();
    })
    .then(data => {
        // Success! Redirect to results page
        window.location.href = '/results';
    })
    .catch(error => {
        // Show error message
        progressBar.style.animation = 'none';
        progressBar.style.width = '100%';
        progressBar.classList.remove('progress-bar-animated', 'progress-bar-striped', 'bg-primary');
        progressBar.classList.add('bg-danger');
        
        errorContainer.classList.remove('d-none');
        errorMessage.textContent = error.message || 'An error occurred while processing your request.';
        
        statusMessage.textContent = 'Error occurred';
    });
}); 