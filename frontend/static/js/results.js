document.addEventListener('DOMContentLoaded', function() {
    // Tab functionality
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons and panes
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabPanes.forEach(pane => pane.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');
            
            // Show corresponding tab pane
            const tabId = this.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });
    
    // Prompt tab functionality
    const promptTabButtons = document.querySelectorAll('.prompt-tab-button');
    const promptTabPanes = document.querySelectorAll('.prompt-tab-pane');
    
    promptTabButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons and panes
            promptTabButtons.forEach(btn => btn.classList.remove('active'));
            promptTabPanes.forEach(pane => pane.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');
            
            // Show corresponding tab pane
            const tabId = this.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });
    
    // Copy to clipboard functionality
    document.querySelectorAll('.copy-btn').forEach(button => {
        button.addEventListener('click', function() {
            const contentId = this.getAttribute('data-content');
            const content = document.getElementById(contentId).textContent;
            
            navigator.clipboard.writeText(content)
                .then(() => {
                    // Show success message
                    const originalText = this.innerHTML;
                    this.innerHTML = '<i class="fas fa-check"></i> Copied!';
                    
                    // Reset button text after 2 seconds
                    setTimeout(() => {
                        this.innerHTML = originalText;
                    }, 2000);
                })
                .catch(err => {
                    console.error('Failed to copy text: ', err);
                    alert('Failed to copy text. Please try again.');
                });
        });
    });
    
    // Download functionality
    document.querySelectorAll('.download-btn').forEach(button => {
        button.addEventListener('click', function() {
            const platform = this.getAttribute('data-platform');
            window.location.href = `/download/${platform}`;
        });
    });
    
    // Start over button
    document.getElementById('startOverBtn').addEventListener('click', function() {
        window.location.href = '/clear_session';
    });

    // Apply syntax highlighting to code blocks
    document.querySelectorAll('pre code').forEach((block) => {
        hljs.highlightElement(block);
    });

    // Make table of contents if it exists
    const toc = document.querySelector('.table-of-contents');
    if (toc) {
        const headings = document.querySelectorAll('.markdown-content h2, .markdown-content h3');
        if (headings.length > 0) {
            const tocList = document.createElement('ul');
            headings.forEach((heading) => {
                const id = heading.textContent.toLowerCase().replace(/\s+/g, '-');
                heading.id = id;
                
                const listItem = document.createElement('li');
                const link = document.createElement('a');
                link.href = `#${id}`;
                link.textContent = heading.textContent;
                link.classList.add(heading.tagName.toLowerCase());
                
                listItem.appendChild(link);
                tocList.appendChild(listItem);
            });
            toc.appendChild(tocList);
        }
    }
}); 