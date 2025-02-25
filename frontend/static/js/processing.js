document.addEventListener('DOMContentLoaded', function() {
    // Set the first step as active
    const step1 = document.getElementById('step1');
    step1.classList.add('active');
    
    // Simulate the processing steps
    setTimeout(() => {
        // Complete step 1 and start step 2
        step1.classList.remove('active');
        step1.classList.add('completed');
        
        const step2 = document.getElementById('step2');
        step2.classList.add('active');
        
        setTimeout(() => {
            // Complete step 2 and start step 3
            step2.classList.remove('active');
            step2.classList.add('completed');
            
            const step3 = document.getElementById('step3');
            step3.classList.add('active');
            
            // Start generating results
            generateResults();
        }, 3000);
    }, 3000);
    
    // Function to generate results
    function generateResults() {
        fetch('/generate_results')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Complete step 3
                    const step3 = document.getElementById('step3');
                    step3.classList.remove('active');
                    step3.classList.add('completed');
                    
                    // Update message and show actions
                    document.getElementById('processingMessage').innerHTML = '<p>All done! Your project ideas and roadmap are ready.</p>';
                    document.getElementById('processingActions').style.display = 'flex';
                } else {
                    // Show error message
                    document.getElementById('processingMessage').innerHTML = `<p class="error-message">${data.message}</p>`;
                    document.getElementById('processingActions').style.display = 'flex';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('processingMessage').innerHTML = '<p class="error-message">There was an error generating your results. Please try again.</p>';
                document.getElementById('processingActions').style.display = 'flex';
            });
    }
    
    // Handle start over button
    document.getElementById('startOverBtn').addEventListener('click', function() {
        window.location.href = '/clear_session';
    });
}); 