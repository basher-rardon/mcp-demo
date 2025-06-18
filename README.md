# MCP Demo Website

Interactive demonstrations of the Model Context Protocol (MCP) featuring educational guides, agent workflows, and comprehensive testing environments.

🌐 **Live Demo**: [View on GitHub Pages](https://basher-rardon.github.io/mcp-demo/)

## 🎯 Demo Pages

### 1. 🎓 MCP vs REST Interactive Guide
**File**: `mcp_demo_interactive.html`

Educational comparison showing the key differences between MCP and REST protocols through interactive examples.

**Features:**
- Side-by-side protocol comparisons
- Interactive concept demonstrations  
- Real-time JSON-RPC message logging
- Educational tooltips and explanations

**Best for**: Understanding MCP fundamentals and how it differs from traditional REST APIs.

### 2. 🤖 Agent Conversation Demo  
**File**: `agent_conversation_demo.html`

Realistic simulation of AI agent workflows using MCP for tool discovery, execution, and prompt management.

**Features:**
- Complete agent workflow simulation
- Multi-step tool discovery and execution
- Prompt template integration
- Real-time conversation and protocol logging
- Mock user data and scenarios

**Best for**: Seeing how MCP works in real AI agent scenarios with realistic data flows.

### 3. 🔬 MCP Comprehensive Playground
**File**: `mcp_demo_standalone.html`

Complete testing environment for all MCP features with live protocol logging and interactive controls.

**Features:**
- Tool testing with parameter validation
- Resource management and reading
- Prompt template execution
- Error simulation and handling
- Export capabilities for logs and data
- Real-time protocol monitoring

**Best for**: Testing MCP implementations, debugging protocols, and exploring all MCP capabilities.

## 🚀 Quick Start

### Option 1: GitHub Pages (Recommended)
Visit the live demos at: **https://basher-rardon.github.io/mcp-demo/**

### Option 2: Local Development
```bash
# Clone the repository
git clone https://github.com/basher-rardon/mcp-demo.git
cd mcp-demo

# Serve locally (any HTTP server works)
python3 -m http.server 8080
# or
npx serve .
# or
php -S localhost:8080

# Open in browser
open http://localhost:8080
```

## 📚 What You'll Learn

- **MCP Protocol Fundamentals**: JSON-RPC 2.0 structure, message types, and flows
- **Tool Management**: Discovery, registration, and execution patterns
- **Resource Handling**: URI-based access, content types, and data streaming  
- **Prompt Templates**: Dynamic generation and parameter substitution
- **Error Handling**: Exception propagation and graceful failure modes
- **Performance Monitoring**: Response times, logging, and debugging techniques

## 🏗️ Repository Structure

```
mcp-demo/
├── index.html                     # Homepage with demo links
├── mcp_demo_interactive.html      # MCP vs REST educational guide
├── agent_conversation_demo.html   # AI agent workflow simulation  
├── mcp_demo_standalone.html       # Comprehensive MCP playground
├── mcp_server_advanced.py         # Python MCP server implementation
├── mcp_playground_server.py       # Extended MCP server with web features
└── README.md                      # This file
```

## 🖥️ Running Actual MCP Servers

The repository includes two Python MCP server implementations for real protocol testing:

### Basic MCP Server
**File**: `mcp_server_advanced.py`

A production-ready MCP server with comprehensive logging and testing capabilities.

```bash
# Install dependencies
pip install mcp tabulate colorama

# Run the server
python3 mcp_server_advanced.py
```

**Features:**
- Tool discovery and execution
- Resource management  
- Real-time logging with colors
- Built-in introspection tools
- File-based log persistence

### Extended MCP Server  
**File**: `mcp_playground_server.py`

Enhanced server with web interface and advanced testing features.

```bash
# Install dependencies  
pip install mcp fastapi uvicorn websockets aiofiles

# Run the server
python3 mcp_playground_server.py
```

**Features:**
- Web-based testing interface
- Real-time WebSocket updates
- Advanced tool simulations
- Binary data handling
- Export and monitoring capabilities

### Testing the Servers

Both servers can be tested with any MCP-compatible client or the provided test utilities:

```bash
# Test basic connectivity
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | python3 mcp_server_advanced.py

# Use the MCP SDK (recommended)
pip install mcp
# Then connect with your preferred MCP client
```

## 🛠️ Development Setup

### VS Code Configuration
Create `.vscode/launch.json` for debugging:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "MCP Server",
            "type": "python", 
            "request": "launch",
            "program": "mcp_server_advanced.py",
            "console": "integratedTerminal"
        },
        {
            "name": "Extended MCP Server",
            "type": "python",
            "request": "launch", 
            "program": "mcp_playground_server.py",
            "console": "integratedTerminal"
        }
    ]
}
```

### Dependencies

For the HTML demos: **None required** - they're self-contained with mock data.

For the Python servers:
```bash
# Basic server
pip install mcp tabulate colorama

# Extended server  
pip install mcp fastapi uvicorn websockets aiofiles
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Test your changes with the demo pages
4. Submit a pull request

## 📖 Learn More

- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [MCP SDK Documentation](https://github.com/modelcontextprotocol/python-sdk)
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)

## 📄 License

MIT License - feel free to use these demos for learning and development.

---

**Built with the Model Context Protocol | Ready for GitHub Pages**