// Career Booster - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the application
    initApp();
});

function initApp() {
    // Initialize tabs
    initTabs();
    
    // Initialize copy buttons
    initCopyButtons();
    
    // Initialize processing page if we're on it
    if (document.querySelector('.processing-page')) {
        startProcessing();
    }
    
    // Initialize project selection if we're on the results page
    if (document.querySelector('.results-page')) {
        initProjectSelection();
    }
}

function initTabs() {
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Remove active class from all tabs and tab contents
            tabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding tab content
            tab.classList.add('active');
            const tabId = tab.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });
}

function initCopyButtons() {
    const copyButtons = document.querySelectorAll('.copy-btn');
    
    copyButtons.forEach(button => {
        button.addEventListener('click', () => {
            const textToCopy = button.getAttribute('data-copy');
            const textarea = document.createElement('textarea');
            textarea.value = textToCopy;
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);
            
            // Change button text temporarily
            const originalText = button.textContent;
            button.textContent = 'Copied!';
            setTimeout(() => {
                button.textContent = originalText;
            }, 2000);
        });
    });
}

function startProcessing() {
    // Show loading spinner
    const spinner = document.querySelector('.spinner-container');
    spinner.style.display = 'flex';
    
    // Update status message
    const statusMessage = document.querySelector('.status-message');
    statusMessage.textContent = 'Analyzing job posting...';
    
    // First, analyze the job posting
    analyzeJobPosting()
        .then(jobAnalysisSuccess => {
            if (!jobAnalysisSuccess) {
                return false;
            }
            
            // Update status message
            statusMessage.textContent = 'Generating project ideas...';
            
            // Then, generate project ideas
            return generateProjectIdeas();
        })
        .then(success => {
            if (success) {
                // Update status message
                statusMessage.textContent = 'Project ideas generated successfully!';
                
                // Redirect to results page
                setTimeout(() => {
                    window.location.href = '/results';
                }, 1000);
            }
        })
        .catch(error => {
            showError('An error occurred during processing. Please try again.');
            console.error('Error:', error);
            
            // Hide spinner
            spinner.style.display = 'none';
        });
}

function analyzeJobPosting() {
    return fetch('/analyze_job_posting', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showError(data.error);
            return false;
        }
        
        console.log('Job posting analyzed successfully');
        return true;
    })
    .catch(error => {
        showError('An error occurred while analyzing the job posting. Continuing with basic analysis...');
        console.error('Error:', error);
        return true; // Continue with project idea generation even if job analysis fails
    });
}

function generateProjectIdeas() {
    return fetch('/generate_ideas', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showError(data.error);
            return false;
        }
        
        return true;
    })
    .catch(error => {
        showError('An error occurred while generating project ideas. Please try again.');
        console.error('Error:', error);
        return false;
    });
}

function initProjectSelection() {
    const selectProjectBtn = document.querySelector('#select-project-btn');
    const projectTextarea = document.querySelector('#selected-project');
    const timeframeSelect = document.querySelector('#timeframe');
    
    if (selectProjectBtn) {
        selectProjectBtn.addEventListener('click', () => {
            const selectedProject = projectTextarea.value.trim();
            const timeframe = timeframeSelect.value;
            
            if (!selectedProject) {
                showError('Please enter a project idea.');
                return;
            }
            
            // Show loading spinner
            const spinner = document.querySelector('.spinner-container');
            spinner.style.display = 'flex';
            
            // Update status message
            const statusMessage = document.querySelector('.status-message');
            statusMessage.textContent = 'Generating roadmap...';
            
            // Make AJAX request to generate roadmap
            fetch('/generate_roadmap', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    selected_project: selectedProject,
                    timeframe: timeframe
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    showError(data.error);
                    return;
                }
                
                // Update status message
                statusMessage.textContent = 'Roadmap generated successfully!';
                
                // Show roadmap
                const roadmapContainer = document.querySelector('.roadmap-container');
                const roadmapContent = document.querySelector('.roadmap');
                roadmapContent.textContent = data.roadmap;
                roadmapContainer.style.display = 'block';
                
                // Show generate prompts button
                const generatePromptsBtn = document.querySelector('#generate-prompts-btn');
                generatePromptsBtn.style.display = 'block';
                
                // Hide spinner
                spinner.style.display = 'none';
                
                // Scroll to roadmap
                roadmapContainer.scrollIntoView({ behavior: 'smooth' });
            })
            .catch(error => {
                showError('An error occurred while generating the roadmap. Please try again.');
                console.error('Error:', error);
                
                // Hide spinner
                spinner.style.display = 'none';
            });
        });
    }
    
    const generatePromptsBtn = document.querySelector('#generate-prompts-btn');
    if (generatePromptsBtn) {
        generatePromptsBtn.addEventListener('click', () => {
            // Show loading spinner
            const spinner = document.querySelector('.spinner-container');
            spinner.style.display = 'flex';
            
            // Update status message
            const statusMessage = document.querySelector('.status-message');
            statusMessage.textContent = 'Generating prompts...';
            
            // Make AJAX request to generate prompts
            fetch('/generate_prompts', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    showError(data.error);
                    return;
                }
                
                // Update status message
                statusMessage.textContent = 'Prompts generated successfully!';
                
                // Show prompts
                const promptsContainer = document.querySelector('.prompts-container');
                promptsContainer.style.display = 'block';
                
                // Update prompt content
                Object.keys(data.prompts).forEach(platform => {
                    const promptElement = document.querySelector(`#${platform}-prompt`);
                    if (promptElement) {
                        promptElement.textContent = data.prompts[platform];
                        
                        // Update copy button
                        const copyBtn = document.querySelector(`#copy-${platform}-btn`);
                        if (copyBtn) {
                            copyBtn.setAttribute('data-copy', data.prompts[platform]);
                        }
                    }
                });
                
                // Initialize tabs
                initTabs();
                
                // Initialize copy buttons
                initCopyButtons();
                
                // Hide spinner
                spinner.style.display = 'none';
                
                // Scroll to prompts
                promptsContainer.scrollIntoView({ behavior: 'smooth' });
            })
            .catch(error => {
                showError('An error occurred while generating prompts. Please try again.');
                console.error('Error:', error);
                
                // Hide spinner
                spinner.style.display = 'none';
            });
        });
    }
}

function showError(message) {
    // Create alert element
    const alert = document.createElement('div');
    alert.className = 'alert alert-danger';
    alert.textContent = message;
    
    // Add alert to the page
    const container = document.querySelector('.container');
    container.insertBefore(alert, container.firstChild);
    
    // Hide spinner if it exists
    const spinner = document.querySelector('.spinner-container');
    if (spinner) {
        spinner.style.display = 'none';
    }
    
    // Remove alert after 5 seconds
    setTimeout(() => {
        alert.remove();
    }, 5000);
} 