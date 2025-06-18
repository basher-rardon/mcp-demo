/**
 * Enhanced JSON Formatter for MCP Demo Website
 * Provides consistent, human-readable JSON formatting across all pages
 */

const JSONFormatter = {
    /**
     * Format JSON object for display with syntax highlighting and proper indentation
     * @param {Object} obj - The object to format
     * @param {number} indent - Number of spaces for indentation (default: 2)
     * @returns {string} - HTML formatted JSON string
     */
    format(obj, indent = 2) {
        if (obj === null) return '<span class="json-null">null</span>';
        if (obj === undefined) return '<span class="json-null">undefined</span>';
        
        const json = JSON.stringify(obj, null, indent);
        return this.addSyntaxHighlighting(json);
    },

    /**
     * Add syntax highlighting to JSON string
     * @param {string} json - JSON string to highlight
     * @returns {string} - HTML with syntax highlighting
     */
    addSyntaxHighlighting(json) {
        return json
            // Escape HTML first to prevent XSS
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            // Format JSON keys (property names)
            .replace(/&quot;([^&]+)&quot;\s*:/g, '<span class="json-key">&quot;$1&quot;</span>:')
            // Format string values
            .replace(/:\s*&quot;([^&]*)&quot;/g, ': <span class="json-string">&quot;$1&quot;</span>')
            // Format numbers (integers and floats)
            .replace(/:\s*(-?\d+\.?\d*)/g, ': <span class="json-number">$1</span>')
            // Format booleans
            .replace(/:\s*(true|false)/g, ': <span class="json-boolean">$1</span>')
            // Format null values
            .replace(/:\s*(null)/g, ': <span class="json-null">$1</span>')
            // Format array and object brackets
            .replace(/(\{|\[)/g, '<span class="json-bracket">$1</span>')
            .replace(/(\}|\])/g, '<span class="json-bracket">$1</span>')
            // Format commas at end of lines
            .replace(/,(\s*$)/gm, '<span class="json-comma">,</span>$1')
            // Format array values that aren't objects/strings
            .replace(/^\s*(-?\d+\.?\d*),?$/gm, '<span class="json-number">$&</span>')
            .replace(/^\s*(true|false),?$/gm, '<span class="json-boolean">$&</span>')
            .replace(/^\s*(null),?$/gm, '<span class="json-null">$&</span>');
    },

    /**
     * Format compact JSON (single line) with highlighting
     * @param {Object} obj - The object to format
     * @returns {string} - Compact HTML formatted JSON
     */
    formatCompact(obj) {
        const json = JSON.stringify(obj);
        return this.addSyntaxHighlighting(json);
    },

    /**
     * Create a collapsible JSON viewer
     * @param {Object} obj - The object to display
     * @param {string} title - Title for the collapsible section
     * @param {boolean} expanded - Whether to start expanded (default: false)
     * @returns {string} - HTML for collapsible JSON viewer
     */
    createCollapsible(obj, title, expanded = false) {
        const id = 'json-' + Math.random().toString(36).substring(2, 11);
        const formattedJson = this.format(obj);
        
        return `
            <div class="json-collapsible">
                <div class="json-header" onclick="JSONFormatter.toggle('${id}')">
                    <span class="json-title">${title}</span>
                    <span class="json-toggle ${expanded ? 'expanded' : ''}">▼</span>
                </div>
                <div class="json-body ${expanded ? 'expanded' : ''}" id="${id}">
                    <pre class="json-content">${formattedJson}</pre>
                </div>
            </div>
        `;
    },

    /**
     * Toggle collapsible JSON section
     * @param {string} id - ID of the section to toggle
     */
    toggle(id) {
        const body = document.getElementById(id);
        const toggle = body.previousElementSibling.querySelector('.json-toggle');
        
        if (body.classList.contains('expanded')) {
            body.classList.remove('expanded');
            toggle.classList.remove('expanded');
        } else {
            body.classList.add('expanded');
            toggle.classList.add('expanded');
        }
    },

    /**
     * Pretty print JSON with error handling
     * @param {string} jsonString - JSON string to format
     * @returns {Object} - {formatted: string, valid: boolean, error?: string}
     */
    prettyPrint(jsonString) {
        try {
            const obj = JSON.parse(jsonString);
            return {
                formatted: this.format(obj),
                valid: true
            };
        } catch (error) {
            return {
                formatted: jsonString,
                valid: false,
                error: error.message
            };
        }
    },

    /**
     * Validate and format JSON input
     * @param {string} input - Raw JSON input
     * @returns {Object} - Validation and formatting result
     */
    validateAndFormat(input) {
        if (!input || !input.trim()) {
            return {
                valid: false,
                error: 'Empty input',
                formatted: ''
            };
        }

        try {
            const parsed = JSON.parse(input);
            return {
                valid: true,
                parsed: parsed,
                formatted: this.format(parsed),
                compact: this.formatCompact(parsed)
            };
        } catch (error) {
            return {
                valid: false,
                error: error.message,
                formatted: input // Return original input if invalid
            };
        }
    }
};

// CSS styles for JSON formatting (add to your stylesheet)
const JSON_FORMATTER_CSS = `
    .json-key { 
        color: #3498db; 
        font-weight: 600;
    }
    
    .json-string { 
        color: #2ecc71; 
    }
    
    .json-number { 
        color: #e74c3c; 
        font-weight: 600;
    }
    
    .json-boolean { 
        color: #f39c12; 
        font-weight: 600;
    }
    
    .json-null { 
        color: #95a5a6; 
        font-style: italic;
    }
    
    .json-bracket {
        color: #ecf0f1;
        font-weight: bold;
    }
    
    .json-comma {
        color: #bdc3c7;
    }
    
    .json-collapsible {
        border: 1px solid #dee2e6;
        border-radius: 8px;
        margin: 10px 0;
        overflow: hidden;
    }
    
    .json-header {
        background: #f8f9fa;
        padding: 12px 15px;
        cursor: pointer;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #dee2e6;
        transition: background-color 0.2s ease;
    }
    
    .json-header:hover {
        background: #e9ecef;
    }
    
    .json-title {
        font-weight: 600;
        color: #2c3e50;
    }
    
    .json-toggle {
        transition: transform 0.2s ease;
        color: #6c757d;
        font-size: 0.8em;
    }
    
    .json-toggle.expanded {
        transform: rotate(180deg);
    }
    
    .json-body {
        display: none;
        background: #2c3e50;
        color: #ecf0f1;
    }
    
    .json-body.expanded {
        display: block;
    }
    
    .json-content {
        margin: 0;
        padding: 20px;
        font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
        font-size: 0.85em;
        line-height: 1.6;
        white-space: pre;
        overflow-x: auto;
    }
`;

// Auto-inject CSS if in browser environment
if (typeof document !== 'undefined') {
    const style = document.createElement('style');
    style.textContent = JSON_FORMATTER_CSS;
    document.head.appendChild(style);
}

// Export for use in Node.js or browser
if (typeof module !== 'undefined' && module.exports) {
    module.exports = JSONFormatter;
} else if (typeof window !== 'undefined') {
    window.JSONFormatter = JSONFormatter;
}