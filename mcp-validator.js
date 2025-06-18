/**
 * MCP (Model Context Protocol) Request/Response Validator
 * Based on JSON-RPC 2.0 specification and MCP protocol requirements
 * 
 * This validator ensures all MCP messages conform to the official specification
 * and provides detailed error reporting for non-compliant messages.
 */

class MCPValidator {
    constructor() {
        this.errors = [];
        this.warnings = [];
    }

    /**
     * Validate any MCP message (request or response)
     */
    validate(message, messageType = 'unknown') {
        this.errors = [];
        this.warnings = [];

        if (!message || typeof message !== 'object') {
            this.addError('Message must be a valid object');
            return this.getValidationResult();
        }

        // Validate JSON-RPC 2.0 base structure
        this.validateJsonRpcBase(message);

        // Determine message type and validate accordingly
        if (message.method) {
            this.validateRequest(message);
        } else if (message.result !== undefined) {
            this.validateResponse(message);
        } else if (message.error !== undefined) {
            this.validateErrorResponse(message);
        } else {
            this.addError('Message must be either a request (with method) or response (with result/error)');
        }

        return this.getValidationResult();
    }

    /**
     * Validate JSON-RPC 2.0 base structure
     */
    validateJsonRpcBase(message) {
        // Required: jsonrpc version
        if (message.jsonrpc !== '2.0') {
            this.addError('jsonrpc field must be exactly "2.0"');
        }

        // Required: id field (for requests and responses, not notifications)
        if (message.id === undefined && message.method && !this.isNotification(message)) {
            this.addError('id field is required for requests and responses');
        }

        // Validate id type
        if (message.id !== undefined) {
            const idType = typeof message.id;
            if (idType !== 'string' && idType !== 'number' && message.id !== null) {
                this.addError('id must be a string, number, or null');
            }
        }
    }

    /**
     * Validate MCP request message
     */
    validateRequest(message) {
        // Required: method field
        if (typeof message.method !== 'string') {
            this.addError('method field must be a string');
            return;
        }

        // Validate specific MCP methods
        const method = message.method;
        
        if (method.startsWith('tools/')) {
            this.validateToolsRequest(message);
        } else if (method.startsWith('resources/')) {
            this.validateResourcesRequest(message);
        } else if (method.startsWith('prompts/')) {
            this.validatePromptsRequest(message);
        } else {
            this.addWarning(`Unknown MCP method: ${method}`);
        }

        // Validate params if present
        if (message.params !== undefined && typeof message.params !== 'object') {
            this.addError('params field must be an object or array');
        }
    }

    /**
     * Validate MCP response message
     */
    validateResponse(message) {
        if (message.result === undefined) {
            this.addError('result field is required in response');
            return;
        }

        // Validate response based on the method (if we can infer it)
        // For demo purposes, we'll validate common response patterns
        this.validateResponseResult(message.result);
    }

    /**
     * Validate error response
     */
    validateErrorResponse(message) {
        const error = message.error;
        
        if (!error || typeof error !== 'object') {
            this.addError('error field must be an object');
            return;
        }

        // Required: code field
        if (typeof error.code !== 'number') {
            this.addError('error.code must be a number');
        }

        // Required: message field
        if (typeof error.message !== 'string') {
            this.addError('error.message must be a string');
        }

        // Optional: data field can be any type
    }

    /**
     * Validate tools-related requests
     */
    validateToolsRequest(message) {
        const method = message.method;
        const params = message.params || {};

        switch (method) {
            case 'tools/list':
                // No specific params required
                break;
                
            case 'tools/call':
                if (typeof params.name !== 'string') {
                    this.addError('tools/call requires params.name as string');
                }
                if (params.arguments !== undefined && typeof params.arguments !== 'object') {
                    this.addError('tools/call params.arguments must be an object');
                }
                break;
                
            default:
                this.addWarning(`Unknown tools method: ${method}`);
        }
    }

    /**
     * Validate resources-related requests
     */
    validateResourcesRequest(message) {
        const method = message.method;
        const params = message.params || {};

        switch (method) {
            case 'resources/list':
                // No specific params required
                break;
                
            case 'resources/read':
                if (typeof params.uri !== 'string') {
                    this.addError('resources/read requires params.uri as string');
                }
                break;
                
            default:
                this.addWarning(`Unknown resources method: ${method}`);
        }
    }

    /**
     * Validate prompts-related requests
     */
    validatePromptsRequest(message) {
        const method = message.method;
        const params = message.params || {};

        switch (method) {
            case 'prompts/list':
                // No specific params required
                break;
                
            case 'prompts/get':
                if (typeof params.name !== 'string') {
                    this.addError('prompts/get requires params.name as string');
                }
                if (params.arguments !== undefined && typeof params.arguments !== 'object') {
                    this.addError('prompts/get params.arguments must be an object');
                }
                break;
                
            default:
                this.addWarning(`Unknown prompts method: ${method}`);
        }
    }

    /**
     * Validate response result based on common MCP patterns
     */
    validateResponseResult(result) {
        if (typeof result !== 'object' || result === null) {
            this.addError('result must be an object');
            return;
        }

        // Check for common MCP response patterns
        if (result.tools) {
            this.validateToolsList(result.tools);
        }
        
        if (result.resources) {
            this.validateResourcesList(result.resources);
        }
        
        if (result.prompts) {
            this.validatePromptsList(result.prompts);
        }
        
        // Note: content arrays are used for Claude-specific plugin messaging,
        // not standard MCP. For standard MCP, tools/call responses should use direct result format.
        if (result.content) {
            this.addWarning('Using content array format - this may be Claude plugin format, not standard MCP');
            this.validateContentArray(result.content);
        }
        
        if (result.contents) {
            this.validateContentsArray(result.contents);
        }
        
        if (result.messages) {
            this.validateMessagesArray(result.messages);
        }
    }

    /**
     * Validate tools list response
     */
    validateToolsList(tools) {
        if (!Array.isArray(tools)) {
            this.addError('tools must be an array');
            return;
        }

        tools.forEach((tool, index) => {
            if (typeof tool.name !== 'string') {
                this.addError(`tools[${index}].name must be a string`);
            }
            if (typeof tool.description !== 'string') {
                this.addError(`tools[${index}].description must be a string`);
            }
            if (tool.inputSchema && typeof tool.inputSchema !== 'object') {
                this.addError(`tools[${index}].inputSchema must be an object`);
            }
        });
    }

    /**
     * Validate resources list response
     */
    validateResourcesList(resources) {
        if (!Array.isArray(resources)) {
            this.addError('resources must be an array');
            return;
        }

        resources.forEach((resource, index) => {
            if (typeof resource.uri !== 'string') {
                this.addError(`resources[${index}].uri must be a string`);
            }
            if (resource.name && typeof resource.name !== 'string') {
                this.addError(`resources[${index}].name must be a string`);
            }
            if (resource.mimeType && typeof resource.mimeType !== 'string') {
                this.addError(`resources[${index}].mimeType must be a string`);
            }
        });
    }

    /**
     * Validate prompts list response
     */
    validatePromptsList(prompts) {
        if (!Array.isArray(prompts)) {
            this.addError('prompts must be an array');
            return;
        }

        prompts.forEach((prompt, index) => {
            if (typeof prompt.name !== 'string') {
                this.addError(`prompts[${index}].name must be a string`);
            }
            if (typeof prompt.description !== 'string') {
                this.addError(`prompts[${index}].description must be a string`);
            }
            if (prompt.arguments && !Array.isArray(prompt.arguments)) {
                this.addError(`prompts[${index}].arguments must be an array`);
            }
        });
    }

    /**
     * Validate content array (for tools/call responses)
     */
    validateContentArray(content) {
        if (!Array.isArray(content)) {
            this.addError('content must be an array');
            return;
        }

        content.forEach((item, index) => {
            if (typeof item !== 'object') {
                this.addError(`content[${index}] must be an object`);
                return;
            }
            
            if (typeof item.type !== 'string') {
                this.addError(`content[${index}].type must be a string`);
            }
            
            // Validate based on content type
            switch (item.type) {
                case 'text':
                    if (typeof item.text !== 'string') {
                        this.addError(`content[${index}].text must be a string for type 'text'`);
                    }
                    break;
                case 'image':
                    if (typeof item.data !== 'string') {
                        this.addError(`content[${index}].data must be a string for type 'image'`);
                    }
                    if (typeof item.mimeType !== 'string') {
                        this.addError(`content[${index}].mimeType must be a string for type 'image'`);
                    }
                    break;
                default:
                    this.addWarning(`Unknown content type: ${item.type}`);
            }
        });
    }

    /**
     * Validate contents array (for resources/read responses)
     */
    validateContentsArray(contents) {
        if (!Array.isArray(contents)) {
            this.addError('contents must be an array');
            return;
        }

        contents.forEach((item, index) => {
            if (typeof item !== 'object') {
                this.addError(`contents[${index}] must be an object`);
                return;
            }
            
            if (typeof item.uri !== 'string') {
                this.addError(`contents[${index}].uri must be a string`);
            }
            
            if (item.mimeType && typeof item.mimeType !== 'string') {
                this.addError(`contents[${index}].mimeType must be a string`);
            }
            
            // Must have either text or blob content
            if (item.text === undefined && item.blob === undefined) {
                this.addError(`contents[${index}] must have either 'text' or 'blob' field`);
            }
            
            if (item.text !== undefined && typeof item.text !== 'string') {
                this.addError(`contents[${index}].text must be a string`);
            }
        });
    }

    /**
     * Validate messages array (for prompts/get responses)
     */
    validateMessagesArray(messages) {
        if (!Array.isArray(messages)) {
            this.addError('messages must be an array');
            return;
        }

        messages.forEach((message, index) => {
            if (typeof message !== 'object') {
                this.addError(`messages[${index}] must be an object`);
                return;
            }
            
            if (typeof message.role !== 'string') {
                this.addError(`messages[${index}].role must be a string`);
            }
            
            if (!['system', 'user', 'assistant'].includes(message.role)) {
                this.addWarning(`messages[${index}].role should be 'system', 'user', or 'assistant'`);
            }
            
            if (typeof message.content !== 'object') {
                this.addError(`messages[${index}].content must be an object`);
            } else {
                this.validateContentItem(message.content, `messages[${index}].content`);
            }
        });
    }

    /**
     * Validate individual content item
     */
    validateContentItem(content, path) {
        if (typeof content.type !== 'string') {
            this.addError(`${path}.type must be a string`);
        }
        
        if (content.type === 'text' && typeof content.text !== 'string') {
            this.addError(`${path}.text must be a string for type 'text'`);
        }
    }

    /**
     * Check if message is a notification (no response expected)
     */
    isNotification(message) {
        return message.method && message.id === undefined;
    }

    /**
     * Add validation error
     */
    addError(message) {
        this.errors.push(message);
    }

    /**
     * Add validation warning
     */
    addWarning(message) {
        this.warnings.push(message);
    }

    /**
     * Get validation result
     */
    getValidationResult() {
        return {
            valid: this.errors.length === 0,
            errors: this.errors,
            warnings: this.warnings
        };
    }

    /**
     * Validate multiple messages (batch)
     */
    validateBatch(messages) {
        const results = [];
        
        if (!Array.isArray(messages)) {
            return {
                valid: false,
                errors: ['Batch must be an array'],
                warnings: [],
                results: []
            };
        }

        messages.forEach((message, index) => {
            const result = this.validate(message, `batch[${index}]`);
            results.push({
                index,
                ...result
            });
        });

        const allValid = results.every(r => r.valid);
        const allErrors = results.flatMap(r => r.errors);
        const allWarnings = results.flatMap(r => r.warnings);

        return {
            valid: allValid,
            errors: allErrors,
            warnings: allWarnings,
            results
        };
    }
}

/**
 * Utility functions for common validation tasks
 */
const MCPValidatorUtils = {
    /**
     * Create example valid MCP messages
     */
    createExamples() {
        return {
            toolsListRequest: {
                jsonrpc: "2.0",
                id: 1,
                method: "tools/list",
                params: {}
            },
            
            toolsListResponse: {
                jsonrpc: "2.0",
                id: 1,
                result: {
                    tools: [
                        {
                            name: "calculator",
                            description: "Perform mathematical calculations",
                            inputSchema: {
                                type: "object",
                                properties: {
                                    expression: { type: "string" }
                                },
                                required: ["expression"]
                            }
                        }
                    ]
                }
            },
            
            toolsCallRequest: {
                jsonrpc: "2.0",
                id: 2,
                method: "tools/call",
                params: {
                    name: "calculator",
                    arguments: {
                        expression: "2 + 2"
                    }
                }
            },
            
            toolsCallResponse: {
                jsonrpc: "2.0",
                id: 2,
                result: {
                    value: 4,
                    expression: "2 + 2"
                }
            },
            
            resourcesReadRequest: {
                jsonrpc: "2.0",
                id: 3,
                method: "resources/read",
                params: {
                    uri: "file://example.txt"
                }
            },
            
            resourcesReadResponse: {
                jsonrpc: "2.0",
                id: 3,
                result: {
                    contents: [
                        {
                            uri: "file://example.txt",
                            mimeType: "text/plain",
                            text: "Hello, world!"
                        }
                    ]
                }
            },
            
            promptsGetRequest: {
                jsonrpc: "2.0",
                id: 4,
                method: "prompts/get",
                params: {
                    name: "greeting",
                    arguments: {
                        name: "World"
                    }
                }
            },
            
            promptsGetResponse: {
                jsonrpc: "2.0",
                id: 4,
                result: {
                    description: "A friendly greeting",
                    messages: [
                        {
                            role: "user",
                            content: {
                                type: "text",
                                text: "Say hello to World"
                            }
                        }
                    ]
                }
            },
            
            errorResponse: {
                jsonrpc: "2.0",
                id: 5,
                error: {
                    code: -32602,
                    message: "Invalid params",
                    data: {
                        parameter: "expression",
                        expected: "string",
                        received: "number"
                    }
                }
            }
        };
    },
    
    /**
     * Test the validator with example messages
     */
    runTests() {
        const validator = new MCPValidator();
        const examples = this.createExamples();
        const results = {};
        
        Object.entries(examples).forEach(([name, message]) => {
            results[name] = validator.validate(message);
        });
        
        return results;
    }
};

// Export for use in Node.js or browser
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { MCPValidator, MCPValidatorUtils };
} else if (typeof window !== 'undefined') {
    window.MCPValidator = MCPValidator;
    window.MCPValidatorUtils = MCPValidatorUtils;
}