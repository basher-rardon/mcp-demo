# MCP Comprehensive Playground

A complete testing environment for the Model Context Protocol (MCP) with all major feature categories implemented as "hello world" examples.

## 🎯 What This Demonstrates

This playground shows every major MCP capability through working examples:

### 🛠️ **Tools** (Function Calls)
- **`add(a, b)`** - Basic tool functionality and parameter validation
- **`fail_on_purpose()`** - Error handling and exception propagation
- **`countdown(n)`** - Streaming responses (simulated)
- **`increment_counter()`** - Stateful server-side operations
- **`get_server_info()`** - Server introspection and capabilities reporting

### 📦 **Resources** (Data Access)
- **`time://current`** - Time-based dynamic content
- **`data://big_text`** - Large context handling (10KB+ text)
- **`image://tiny_png_base64`** - Binary data encoding/handling

### 💬 **Prompts** (Template Generation)
- **`prompt_greet(name)`** - Dynamic prompt template generation

### 📊 **Advanced Features**
- **Comprehensive Logging** - Every request/response with timestamps
- **Real-time Monitoring** - WebSocket-based live updates
- **Error Scenarios** - Intentional failures for testing
- **Performance Metrics** - Response time tracking
- **Export Capabilities** - Log export and data persistence

## 🚀 Quick Start

### Prerequisites

```bash
# Install dependencies
pip install -r requirements_comprehensive.txt

# Or install individually:
pip install mcp fastapi uvicorn websockets aiofiles python-multipart jinja2
```

### Running the Playground

#### Option 1: Command Line Testing
```bash
# Terminal 1: Start the MCP Server
python3 mcp_playground_server.py

# Terminal 2: Test with our original simple client
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | python3 mcp_playground_server.py
```

#### Option 2: Web Interface (Recommended)
```bash
# Terminal 1: Start the MCP Server (if not already running)
python3 mcp_playground_server.py

# Terminal 2: Start the Web Client
python3 mcp_playground_client.py
```

Then open: **http://localhost:8001** in your browser

## 🎮 Using the Web Interface

### 1. **Feature Discovery**
- Click "🔍 Discover All Features" to scan the server
- View tools, resources, and prompts in organized tabs
- See summary statistics and categories

### 2. **Testing Tools**
```json
// Example: Test the add tool
{
  "a": 15,
  "b": 27
}

// Example: Test countdown (streaming)
{
  "n": 5
}

// Example: Test error handling
{
  "message": "Custom error for testing"
}
```

### 3. **Testing Resources**
- Click "📦 Read Resource" for any resource
- See different data types: text, large content, binary
- Monitor response times and sizes

### 4. **Testing Prompts**
```json
// Example: Generate greeting prompt
{
  "name": "Alice"
}
```

### 5. **Monitoring Logs**
- Real-time log updates in the right panel
- Color-coded by operation type
- Export logs to file for analysis

## 🔍 VS Code Setup & Debugging

### 1. **Project Structure**
```
mcp-test/
├── mcp_playground_server.py     # Main MCP server
├── mcp_playground_client.py     # Web client interface
├── requirements_comprehensive.txt
├── README_MCP_Playground.md
└── logs/
    ├── mcp_playground.log       # Server logs
    └── exported_logs_*.json     # Exported session logs
```

### 2. **VS Code Launch Configuration**
Create `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "MCP Playground Server",
            "type": "python",
            "request": "launch",
            "program": "mcp_playground_server.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        },
        {
            "name": "MCP Web Client",
            "type": "python",
            "request": "launch",
            "program": "mcp_playground_client.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        }
    ]
}
```

### 3. **Debugging Workflow**
1. **Set breakpoints** in tool handlers (`handle_call_tool`)
2. **F5** to start the server in debug mode
3. **Ctrl+Shift+`** to open new terminal
4. **Start web client** in the new terminal
5. **Test features** from the web interface
6. **Step through** code at breakpoints

### 4. **Log Analysis**
```bash
# View real-time server logs
tail -f mcp_playground.log

# Search for specific operations
grep "tool_call" mcp_playground.log

# Export logs from web interface
# Click "📁 Export Logs" button
```

## 📚 What Each Feature Demonstrates

### **Basic Operations** (`add` tool)
- **JSON-RPC parameter validation**
- **Type checking** (integer inputs)
- **Simple response formatting**
- **Error handling** for invalid parameters

```python
# Server receives:
{"method": "tools/call", "params": {"name": "add", "arguments": {"a": 5, "b": 3}}}

# Server responds:
{"result": {"content": [{"type": "text", "text": "Adding 5 + 3 = 8"}]}}
```

### **Error Handling** (`fail_on_purpose` tool)
- **Exception propagation** through MCP
- **Custom error messages**
- **Client-side error display**
- **Logging of error scenarios**

### **Streaming Responses** (`countdown` tool)
- **Progressive data delivery** (simulated)
- **Real-time UI updates**
- **Stream event logging**
- **Client-side streaming handling**

⚠️ **Note**: True streaming requires WebSocket implementation. This demo simulates streaming through rapid sequential messages.

### **Stateful Operations** (`increment_counter` tool)
- **Server-side state persistence**
- **Thread-safe operations**
- **State introspection**
- **Concurrent access handling**

### **Large Context** (`big_text` resource)
- **10KB+ text handling**
- **Memory usage patterns**
- **Transfer time monitoring**
- **Context window implications**

### **Binary Data** (`tiny_png_base64` resource)
- **Base64 encoding/decoding**
- **MIME type handling**
- **Binary data visualization**
- **File format support**

### **Dynamic Content** (`time` resource)
- **Real-time data generation**
- **Timestamp consistency**
- **Cache implications**
- **Time zone handling**

### **Template Generation** (`prompt_greet` prompt)
- **Dynamic prompt creation**
- **Parameter substitution**
- **Template reusability**
- **AI integration patterns**

## 🚨 Limitations & Considerations

### **Streaming Implementation**
- **Current**: Simulated through rapid messages
- **Production**: Requires WebSocket or Server-Sent Events
- **Limitation**: Not true real-time streaming

### **Binary Data Handling**
- **Current**: Base64 encoding only
- **Production**: Direct binary transfer protocols
- **Limitation**: Encoding overhead (~33% size increase)

### **Large Context Testing**
- **Current**: 10KB sample text
- **Production**: Multi-MB documents possible
- **Consideration**: Memory and transfer time scaling

### **State Persistence**
- **Current**: In-memory only
- **Production**: Database or file-based persistence
- **Limitation**: State lost on server restart

### **Error Recovery**
- **Current**: Basic exception handling
- **Production**: Retry logic, circuit breakers
- **Enhancement**: Graceful degradation patterns

## 📊 Example Session Log

```json
[
  {
    "timestamp": "2024-01-15T10:30:00.123Z",
    "request_type": "TOOLS",
    "operation": "list_tools",
    "parameters": {},
    "response_time_ms": 15.2,
    "success": true
  },
  {
    "timestamp": "2024-01-15T10:30:15.456Z",
    "request_type": "TOOL_CALL",
    "operation": "call_tool",
    "name": "add",
    "parameters": {"a": 5, "b": 3},
    "response_time_ms": 8.7,
    "success": true
  },
  {
    "timestamp": "2024-01-15T10:30:30.789Z",
    "request_type": "TOOL_CALL",
    "operation": "call_tool",
    "name": "countdown",
    "parameters": {"n": 3},
    "streaming": true,
    "stream_events": [
      {"timestamp": "2024-01-15T10:30:31.000Z", "data": {"count": 3}},
      {"timestamp": "2024-01-15T10:30:32.000Z", "data": {"count": 2}},
      {"timestamp": "2024-01-15T10:30:33.000Z", "data": {"count": 1}}
    ],
    "response_time_ms": 3150.0,
    "success": true
  }
]
```

## 🛠️ Extending the Playground

### **Adding New Tools**
```python
# In mcp_playground_server.py
Tool(
    name="your_new_tool",
    description="Description of what it does",
    inputSchema={
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "Parameter description"}
        },
        "required": ["param1"]
    }
)

# Add handler in handle_call_tool()
elif name == "your_new_tool":
    param1 = arguments.get("param1")
    result = f"Processing: {param1}"
    content = result
```

### **Adding New Resources**
```python
# Add to handle_list_resources()
Resource(
    uri="custom://my_resource",
    name="My Custom Resource",
    description="Custom resource description",
    mimeType="application/json"
)

# Add handler in handle_read_resource()
elif uri == "custom://my_resource":
    content = json.dumps({"custom": "data"})
```

### **Custom Logging**
```python
# Add custom log categories
self.logger.log_custom_event("CUSTOM", "my_operation", {
    "custom_data": "value"
})
```

## 🎓 Learning Outcomes

After exploring this playground, you'll understand:

1. **MCP Protocol Fundamentals**
   - JSON-RPC 2.0 message structure
   - Tool/resource/prompt discovery patterns
   - Parameter validation and typing

2. **Error Handling Strategies**
   - Exception propagation mechanisms
   - Client-side error presentation
   - Debugging techniques

3. **Performance Considerations**
   - Response time monitoring
   - Large data transfer patterns
   - Memory usage implications

4. **Integration Patterns**
   - Client-server communication flows
   - Real-time update mechanisms
   - State management approaches

5. **Production Readiness**
   - Logging and monitoring requirements
   - Scalability considerations
   - Security implications

## 🚀 Next Steps

1. **Explore each feature** systematically
2. **Monitor the logs** to understand protocol flow
3. **Test error scenarios** to see failure handling
4. **Experiment with parameters** to test validation
5. **Export logs** for offline analysis
6. **Extend with custom tools** for your use case

This playground provides a complete foundation for understanding and working with the Model Context Protocol in production environments.