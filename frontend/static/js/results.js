document.addEventListener('DOMContentLoaded', function() {
    // Initialize Prism.js syntax highlighting
    if (typeof Prism !== 'undefined') {
        Prism.highlightAll();
    }
    
    // Format any markdown content in the page
    formatMarkdown();
    
    // Format markdown text in elements with the markdown-content class
    function formatMarkdown() {
        // Convert markdown-style lists to HTML lists
        const markdownContents = document.querySelectorAll('.markdown-content p');
        
        markdownContents.forEach(content => {
            const text = content.innerHTML;
            
            // Process the content if it's not empty
            if (text && text.trim()) {
                // Format bullet lists
                let formattedText = formatBulletLists(text);
                
                // Format numbered lists
                formattedText = formatNumberedLists(formattedText);
                
                // Format inline markdown
                formattedText = formatInlineMarkdown(formattedText);
                
                // Update the content if it was changed
                if (formattedText !== text) {
                    content.innerHTML = formattedText;
                }
            }
        });
    }
    
    // Format bullet lists (*, -, +)
    function formatBulletLists(text) {
        if (!text.match(/^[\s]*[*\-+][\s]+/m)) {
            return text;
        }
        
        // Split by newlines
        let lines = text.split(/\n/);
        let inList = false;
        let formattedLines = [];
        
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            // Check if line starts with a bullet
            if (line.match(/^[\s]*[*\-+][\s]+/)) {
                // If not in a list, start one
                if (!inList) {
                    formattedLines.push('<ul>');
                    inList = true;
                }
                // Add list item
                formattedLines.push('<li>' + line.replace(/^[\s]*[*\-+][\s]+/, '') + '</li>');
            } else {
                // If in a list, end it
                if (inList) {
                    formattedLines.push('</ul>');
                    inList = false;
                }
                formattedLines.push(line);
            }
        }
        
        // If still in a list at the end, close it
        if (inList) {
            formattedLines.push('</ul>');
        }
        
        return formattedLines.join('\n');
    }
    
    // Format numbered lists (1., 2., etc.)
    function formatNumberedLists(text) {
        if (!text.match(/^[\s]*\d+\.[\s]+/m)) {
            return text;
        }
        
        // Split by newlines
        let lines = text.split(/\n/);
        let inList = false;
        let formattedLines = [];
        
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            // Check if line starts with a number
            if (line.match(/^[\s]*\d+\.[\s]+/)) {
                // If not in a list, start one
                if (!inList) {
                    formattedLines.push('<ol>');
                    inList = true;
                }
                // Add list item
                formattedLines.push('<li>' + line.replace(/^[\s]*\d+\.[\s]+/, '') + '</li>');
            } else {
                // If in a list, end it
                if (inList) {
                    formattedLines.push('</ol>');
                    inList = false;
                }
                formattedLines.push(line);
            }
        }
        
        // If still in a list at the end, close it
        if (inList) {
            formattedLines.push('</ol>');
        }
        
        return formattedLines.join('\n');
    }
    
    // Format inline markdown (bold, italic, code)
    function formatInlineMarkdown(text) {
        return text
            // Format bold text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            // Format italic text
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            // Format code blocks
            .replace(/`(.*?)`/g, '<code>$1</code>')
            // Format headers
            .replace(/^#{3}\s+(.*)$/gm, '<h3>$1</h3>')
            .replace(/^#{2}\s+(.*)$/gm, '<h2>$1</h2>')
            .replace(/^#{1}\s+(.*)$/gm, '<h1>$1</h1>');
    }
}); 