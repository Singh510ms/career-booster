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
        
        // Initialize project cards if they exist
        if (document.querySelector('.project-cards')) {
            initProjectCards();
        }
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
                
                // Show prompts container
                const promptsContainer = document.querySelector('.prompts-container');
                promptsContainer.style.display = 'block';
                
                // Update prompt content for each platform
                updatePromptDisplay('v0-prompt', data.prompts.v0);
                updatePromptDisplay('lovable-prompt', data.prompts.lovable);
                updatePromptDisplay('replit-prompt', data.prompts.replit);
                updatePromptDisplay('generic-prompt', data.prompts.generic);
                
                // Update copy buttons
                updateCopyButtonsWithNewContent();
                
                // Hide spinner
                spinner.style.display = 'none';
                
                // Scroll to prompts
                promptsContainer.scrollIntoView({ behavior: 'smooth' });
                
                // If project cards exist, update prompts with selected project
                const activeProjectCard = document.querySelector('.project-card.active');
                if (activeProjectCard && typeof projectData !== 'undefined') {
                    const projectIndex = parseInt(activeProjectCard.getAttribute('data-project-index'));
                    const selectedProject = projectData[projectIndex];
                    
                    // Store the raw prompts in platformPrompts for future use
                    if (typeof platformPrompts === 'undefined') {
                        window.platformPrompts = {
                            v0: data.prompts.v0 || '',
                            lovable: data.prompts.lovable || '',
                            replit: data.prompts.replit || '',
                            generic: data.prompts.generic || ''
                        };
                    } else {
                        platformPrompts.v0 = data.prompts.v0 || platformPrompts.v0 || '';
                        platformPrompts.lovable = data.prompts.lovable || platformPrompts.lovable || '';
                        platformPrompts.replit = data.prompts.replit || platformPrompts.replit || '';
                        platformPrompts.generic = data.prompts.generic || platformPrompts.generic || '';
                    }
                    
                    // Update prompts with selected project information
                    setTimeout(() => {
                        updatePlatformPrompts(selectedProject);
                    }, 100);
                }
            })
            .catch(error => {
                showError('An error occurred while generating prompts. Please try again.');
                console.error('Error:', error);
                
                // Hide spinner
                spinner.style.display = 'none';
            });
        });
    }
    
    function updatePromptDisplay(elementId, content) {
        const element = document.getElementById(elementId);
        if (element) {
            element.textContent = content || '';
        }
    }
    
    function updateCopyButtonsWithNewContent() {
        const copyButtons = document.querySelectorAll('.copy-btn');
        copyButtons.forEach(button => {
            const targetId = button.id.replace('copy-', '').replace('-btn', '');
            const targetElement = document.getElementById(`${targetId}-prompt`);
            
            if (targetElement) {
                button.setAttribute('data-copy', targetElement.textContent);
            }
        });
    }
}

function initProjectCards() {
    const projectCards = document.querySelectorAll('.project-card');
    const selectedProjectTitle = document.getElementById('selected-project-title');
    const selectedProjectDescription = document.getElementById('selected-project-description');
    const selectedProjectTechStack = document.getElementById('selected-project-tech-stack');
    const selectedProjectUniqueValue = document.getElementById('selected-project-unique-value');
    
    // Select the first project by default
    if (projectCards.length > 0 && typeof projectData !== 'undefined') {
        selectProject(0, projectCards[0]);
    }
    
    projectCards.forEach(card => {
        card.addEventListener('click', function() {
            const projectIndex = parseInt(this.getAttribute('data-project-index'));
            selectProject(projectIndex, this);
        });
    });
    
    function selectProject(index, cardElement) {
        // Remove active class from all cards
        projectCards.forEach(c => c.classList.remove('active'));
        
        // Add active class to selected card
        cardElement.classList.add('active');
        
        // Update project details
        const project = projectData[index];
        selectedProjectTitle.textContent = project.title;
        selectedProjectDescription.textContent = project.description;
        selectedProjectTechStack.textContent = project.tech_stack || 'Not specified';
        selectedProjectUniqueValue.textContent = project.unique_value || 'Not specified';
        
        // Update platform prompts
        updatePlatformPrompts(project);
    }
    
    function updatePlatformPrompts(project) {
        // Generate prompts for each platform
        const lovablePrompt = generateLovablePrompt(project);
        const boltPrompt = generateBoltPrompt(project);
        const replitPrompt = generateReplitPrompt(project);
        
        // Update prompt content
        document.getElementById('lovable-prompt').textContent = lovablePrompt;
        document.getElementById('bolt-prompt').textContent = boltPrompt;
        document.getElementById('replit-prompt').textContent = replitPrompt;
        
        // Update copy buttons
        updateCopyButton('copy-lovable-btn', lovablePrompt);
        updateCopyButton('copy-bolt-btn', boltPrompt);
        updateCopyButton('copy-replit-btn', replitPrompt);
    }
    
    function generateLovablePrompt(project) {
        return `Project Title: ${project.title}

Description:
${project.description}

Tech Stack:
${project.tech_stack || 'Not specified'}

Unique Value:
${project.unique_value || 'Not specified'}`;
    }
    
    function generateBoltPrompt(project) {
        return `Project Title: ${project.title}

Project Overview:
${project.description}

Technology Stack:
${project.tech_stack || 'Not specified'}

Unique Features:
${project.unique_value || 'Not specified'}`;
    }
    
    function generateReplitPrompt(project) {
        return `Project Name: ${project.title}

Project Description:
${project.description}

Required Technologies:
${project.tech_stack || 'Not specified'}

Key Features:
${project.unique_value || 'Not specified'}`;
    }
    
    function updateCopyButton(buttonId, text) {
        const button = document.getElementById(buttonId);
        if (button) {
            button.addEventListener('click', () => {
                navigator.clipboard.writeText(text).then(() => {
                    const originalText = button.textContent;
                    button.textContent = 'Copied!';
                    setTimeout(() => {
                        button.textContent = originalText;
                    }, 2000);
                });
            });
        }
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