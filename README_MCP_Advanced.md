# Advanced MCP Server with Comprehensive Logging & Testing

This project provides an advanced Model Context Protocol (MCP) server implementation with comprehensive logging, introspection capabilities, and testing tools.

## 🚀 Features

### Core Capabilities
- **Tool Discovery & Execution**: Register and execute tools with full parameter validation
- **Resource Management**: Serve and manage resources with URI-based access
- **Comprehensive Logging**: Real-time logging of all MCP operations with timestamps, parameters, and response times
- **Server Introspection**: Built-in tools to examine server state and capabilities
- **Testing Framework**: Complete client-side testing suite for validation

### Advanced Logging System
- **Real-time Console Output**: Color-coded logs with request/response tracking
- **File Logging**: Persistent logs written to `mcp_server.log`
- **Memory-based Log Storage**: In-memory deque for fast log retrieval
- **Structured Log Entries**: Detailed logging with timestamps, parameters, and performance metrics

### Built-in Tools
1. **hello-world**: Demo greeting tool with optional name parameter
2. **calculate**: Safe mathematical expression evaluator
3. **get_system_info**: System information retrieval
4. **get_server_logs**: Display recent server logs in formatted tables
5. **test_tool**: Test any registered tool with sample parameters

### Built-in Resources
1. **demo://server-info**: JSON server metadata and statistics
2. **demo://logs**: Recent server logs in table format

## 📋 Requirements

Create a `requirements.txt` file with the following dependencies:

```
mcp>=1.0.0
tabulate>=0.9.0
colorama>=0.4.6
```

## 🛠️ Installation & Setup

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Or install individually
pip install mcp tabulate colorama
```

### 2. File Structure

Your project should have these files:
```
mcp-test/
├── mcp_server_advanced.py    # Advanced MCP server
├── mcp_client_test.py        # Test client
├── requirements.txt          # Python dependencies
├── README_MCP_Advanced.md    # This documentation
└── mcp_server.log           # Generated log file
```

## 🎯 Usage Instructions

### Running the Server

#### Method 1: Direct Execution
```bash
python3 mcp_server_advanced.py
```

#### Method 2: VS Code Integration
1. Open the project folder in VS Code
2. Open the terminal (View → Terminal)
3. Run: `python3 mcp_server_advanced.py`

The server will display:
- Startup banner with registered tools and resources
- Real-time colored logging output
- Connection status and request/response details

### Testing with the Test Client

#### Comprehensive Testing (Recommended)
```bash
python3 mcp_client_test.py --mode comprehensive
```

This will:
1. Connect to the server
2. Discover all tools and resources
3. Test each tool with sample parameters
4. Read all available resources
5. Display results in formatted tables

#### Interactive Testing Mode
```bash
python3 mcp_client_test.py --mode interactive
```

Interactive commands:
- `list` - Show all available tools and resources
- `tool <name> [json_args]` - Test a specific tool
- `resource <uri>` - Read a specific resource
- `quit` - Exit

#### Example Interactive Session
```
mcp-test> list
Available Tools:
  - hello-world: Says hello world - demo tool
  - calculate: Perform basic mathematical calculations
  - get_system_info: Get basic system information

mcp-test> tool hello-world {"name": "Claude"}
🧪 Testing tool: hello-world
Arguments: {"name": "Claude"}
✅ Tool executed successfully
Duration: 12.34ms
Response: Hello, Claude! 🌍

mcp-test> tool calculate {"expression": "2+2*3"}
🧪 Testing tool: calculate
Arguments: {"expression": "2+2*3"}
✅ Tool executed successfully  
Duration: 8.76ms
Response: 2+2*3 = 8

mcp-test> resource demo://server-info
📖 Reading resource: demo://server-info
✅ Resource read successfully
Duration: 5.21ms
Content: {
  "server_name": "Advanced MCP Server",
  "version": "1.0.0",
  "tools_registered": 5,
  "resources_registered": 2,
  "uptime": "2024-01-15T10:30:45.123456",
  "logs_in_memory": 15
}
```

## 🔍 Understanding the Logs

### Console Output Format

**Request Logging:**
```
📥 REQUEST [2024-01-15T10:30:45.123456]
   Type: TOOL_CALL
   Operation: call_tool
   Name: hello-world
   Parameters: {"name": "Claude"}
```

**Response Logging:**
```
✅ RESPONSE [2024-01-15T10:30:45.234567]
   Duration: 12.34ms
   Response: {"result": "success"}
────────────────────────────────────────────────────────────────────────────────
```

### Log File Format
The `mcp_server.log` file contains structured logs:
```
2024-01-15 10:30:45,123 - INFO - REQUEST: TOOL_CALL - call_tool - hello-world
2024-01-15 10:30:45,234 - INFO - RESPONSE: call_tool - SUCCESS
```

### In-Memory Log Access
Use the built-in `get_server_logs` tool to view recent operations:

```bash
# Via test client
mcp-test> tool get_server_logs {"limit": 20}

# Or programmatically via MCP call
```

## 🧪 Testing & Debugging Workflow

### 1. Basic Server Validation
```bash
# Start server and verify startup
python3 mcp_server_advanced.py
```
Look for:
- ✅ Green startup messages
- 📋 Tool registration table
- 📦 Resource registration table
- No error messages

### 2. Capability Discovery
```bash
# Test discovery
python3 mcp_client_test.py --mode comprehensive
```
Verify:
- All expected tools are listed
- All expected resources are available
- No connection errors

### 3. Individual Tool Testing
```bash
# Interactive testing
python3 mcp_client_test.py --mode interactive
```
Test each tool individually:
- Verify parameter handling
- Check response formats
- Monitor performance metrics

### 4. Log Analysis
Monitor these aspects:
- **Response Times**: Should be <100ms for simple operations
- **Error Rates**: Should be 0% for valid requests
- **Parameter Validation**: Invalid parameters should be handled gracefully

## 🔧 VS Code Setup & Debugging

### 1. Python Environment
```bash
# Verify Python version
python3 --version  # Should be 3.8+

# Verify dependencies
python3 -c "import mcp, tabulate, colorama; print('All dependencies available')"
```

### 2. VS Code Launch Configuration
Create `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "MCP Server",
            "type": "python",
            "request": "launch",
            "program": "mcp_server_advanced.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        },
        {
            "name": "MCP Client Test",
            "type": "python",
            "request": "launch",
            "program": "mcp_client_test.py",
            "args": ["--mode", "comprehensive"],
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        }
    ]
}
```

### 3. Running in VS Code
1. **F5** or **Run → Start Debugging** to launch the server
2. Use **Ctrl+Shift+`** to open a new terminal
3. Run the test client in the new terminal

### 4. Debugging Tips
- Set breakpoints in tool handlers for step-through debugging
- Use the integrated terminal to monitor real-time logs
- Check the `mcp_server.log` file for persistent logging
- Use the `get_server_logs` tool to inspect operation history

## 📊 Understanding MCP Protocol Flow

### Tool Discovery Flow
```
Client → tools/list → Server
Server → {tools: [...]} → Client
```

### Tool Execution Flow  
```
Client → tools/call {name, arguments} → Server
Server → {content: [...]} → Client
```

### Resource Access Flow
```
Client → resources/list → Server
Server → {resources: [...]} → Client
Client → resources/read {uri} → Server
Server → {contents: [...]} → Client
```

## 🎓 Learning & Development Benefits

This advanced MCP server helps you:

1. **Understand MCP Protocol**: See JSON-RPC messages in real-time
2. **Debug Issues**: Comprehensive logging shows exactly what's happening
3. **Test Tools**: Validate tool behavior before integration
4. **Monitor Performance**: Track response times and identify bottlenecks
5. **Learn Patterns**: See how tools and resources should be structured

## 🚨 Troubleshooting

### Common Issues

**"No module named 'mcp'"**
```bash
pip install mcp
```

**Connection refused errors**
- Ensure server is running before starting client
- Check for port conflicts

**Import errors**
```bash
pip install tabulate colorama
```

**Server startup failures**
- Check Python version (3.8+ required)
- Verify all dependencies are installed
- Check file permissions

### Getting Help

1. Check the `mcp_server.log` file for detailed error messages
2. Run the test client to validate server functionality
3. Use the `get_server_logs` tool to inspect recent operations
4. Enable debug logging by modifying the logging level in the server code

## 🎯 Next Steps

Once you have the basic server running:

1. **Add Custom Tools**: Implement your own tools following the existing patterns
2. **Add Custom Resources**: Create domain-specific resources
3. **Integrate with Applications**: Connect your MCP server to real applications
4. **Scale Up**: Add database backends, authentication, or distributed capabilities

The comprehensive logging and testing framework makes it easy to validate any additions and understand how they integrate with the MCP protocol.