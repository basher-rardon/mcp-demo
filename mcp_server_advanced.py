#!/usr/bin/env python3
"""
Advanced MCP Server with Comprehensive Logging and Introspection
"""

import asyncio
import json
import logging
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional, Sequence
from dataclasses import dataclass, asdict
import threading
from collections import deque

try:
    from mcp.server.models import InitializationOptions
    from mcp.server import NotificationOptions, Server
    from mcp.types import (
        Resource, Tool, TextContent, ImageContent, EmbeddedResource,
        LoggingLevel
    )
    import mcp.types as types
    from mcp.server.stdio import stdio_server
except ImportError:
    print("❌ MCP library not found. Install with: pip install mcp")
    sys.exit(1)

try:
    from tabulate import tabulate
    from colorama import init, Fore, Back, Style
    init()  # Initialize colorama
except ImportError:
    print("❌ Required libraries not found. Install with: pip install tabulate colorama")
    sys.exit(1)


@dataclass
class LogEntry:
    """Structured log entry for MCP operations"""
    timestamp: str
    request_type: str
    operation: str
    name: Optional[str]
    parameters: Dict[str, Any]
    request_payload: Dict[str, Any]
    response_payload: Optional[Dict[str, Any]] = None
    response_time_ms: Optional[float] = None
    error: Optional[str] = None
    success: bool = True


class MCPLogger:
    """Advanced logging system for MCP operations"""
    
    def __init__(self, max_memory_logs: int = 1000):
        self.memory_logs: deque = deque(maxlen=max_memory_logs)
        self.lock = threading.Lock()
        
        # Setup file logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('mcp_server.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def log_request(self, request_type: str, operation: str, name: str = None, 
                   parameters: Dict = None, request_payload: Dict = None) -> LogEntry:
        """Log an incoming MCP request"""
        entry = LogEntry(
            timestamp=datetime.now().isoformat(),
            request_type=request_type,
            operation=operation,
            name=name,
            parameters=parameters or {},
            request_payload=request_payload or {}
        )
        
        with self.lock:
            self.memory_logs.append(entry)
        
        # Console output with colors
        print(f"{Fore.CYAN}📥 REQUEST [{entry.timestamp}]{Style.RESET_ALL}")
        print(f"   Type: {Fore.YELLOW}{request_type}{Style.RESET_ALL}")
        print(f"   Operation: {Fore.GREEN}{operation}{Style.RESET_ALL}")
        if name:
            print(f"   Name: {Fore.MAGENTA}{name}{Style.RESET_ALL}")
        if parameters:
            print(f"   Parameters: {json.dumps(parameters, indent=2)}")
        
        self.logger.info(f"REQUEST: {request_type} - {operation} - {name}")
        return entry
    
    def log_response(self, entry: LogEntry, response_payload: Dict = None, 
                    error: str = None, response_time_ms: float = None):
        """Log an MCP response"""
        entry.response_payload = response_payload
        entry.error = error
        entry.success = error is None
        entry.response_time_ms = response_time_ms
        
        # Console output with colors
        status_color = Fore.GREEN if entry.success else Fore.RED
        status_icon = "✅" if entry.success else "❌"
        
        print(f"{status_color}{status_icon} RESPONSE [{entry.timestamp}]{Style.RESET_ALL}")
        if response_time_ms:
            print(f"   Duration: {Fore.CYAN}{response_time_ms:.2f}ms{Style.RESET_ALL}")
        
        if error:
            print(f"   Error: {Fore.RED}{error}{Style.RESET_ALL}")
        elif response_payload:
            print(f"   Response: {json.dumps(response_payload, indent=2)}")
        
        self.logger.info(f"RESPONSE: {entry.operation} - {'SUCCESS' if entry.success else 'ERROR'}")
        print("-" * 80)
    
    def get_logs(self, limit: int = None) -> List[LogEntry]:
        """Get recent logs from memory"""
        with self.lock:
            logs = list(self.memory_logs)
            if limit:
                logs = logs[-limit:]
            return logs
    
    def get_logs_table(self, limit: int = 20) -> str:
        """Get logs formatted as a table"""
        logs = self.get_logs(limit)
        if not logs:
            return "No logs available"
        
        headers = ["Timestamp", "Type", "Operation", "Name", "Success", "Duration (ms)"]
        rows = []
        
        for log in logs:
            rows.append([
                log.timestamp[:19],  # Truncate timestamp
                log.request_type,
                log.operation,
                log.name or "-",
                "✅" if log.success else "❌",
                f"{log.response_time_ms:.2f}" if log.response_time_ms else "-"
            ])
        
        return tabulate(rows, headers=headers, tablefmt="grid")


class AdvancedMCPServer:
    """Advanced MCP Server with logging and introspection capabilities"""
    
    def __init__(self):
        self.server = Server("advanced-mcp-server")
        self.logger = MCPLogger()
        self.registered_tools: Dict[str, Tool] = {}
        self.registered_resources: Dict[str, Resource] = {}
        
        # Register introspection and testing tools
        self._register_introspection_tools()
        self._register_demo_tools()
        self._register_demo_resources()
    
    def _register_introspection_tools(self):
        """Register tools for server introspection and testing"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """List all available tools"""
            start_time = datetime.now()
            entry = self.logger.log_request("TOOLS", "list_tools", request_payload={"method": "tools/list"})
            
            try:
                tools = [
                    Tool(
                        name="get_server_logs",
                        description="Display recent server operation logs in a formatted table",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "limit": {
                                    "type": "integer",
                                    "description": "Number of recent logs to display (default: 20)",
                                    "default": 20
                                }
                            }
                        }
                    ),
                    Tool(
                        name="test_tool",
                        description="Test any registered tool with sample parameters",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "tool_name": {
                                    "type": "string",
                                    "description": "Name of the tool to test"
                                },
                                "parameters": {
                                    "type": "object",
                                    "description": "Parameters to pass to the tool"
                                }
                            },
                            "required": ["tool_name"]
                        }
                    ),
                    Tool(
                        name="hello-world",
                        description="Says hello world - demo tool",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "description": "Name to greet (optional)",
                                    "default": "World"
                                }
                            }
                        }
                    ),
                    Tool(
                        name="calculate",
                        description="Perform basic mathematical calculations",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "expression": {
                                    "type": "string",
                                    "description": "Mathematical expression to evaluate (e.g., '2+2', '10*5')"
                                }
                            },
                            "required": ["expression"]
                        }
                    ),
                    Tool(
                        name="get_system_info",
                        description="Get basic system information",
                        inputSchema={
                            "type": "object",
                            "properties": {}
                        }
                    )
                ]
                
                # Store registered tools
                for tool in tools:
                    self.registered_tools[tool.name] = tool
                
                response_time = (datetime.now() - start_time).total_seconds() * 1000
                self.logger.log_response(entry, {"tools": [t.name for t in tools]}, response_time_ms=response_time)
                
                return tools
                
            except Exception as e:
                self.logger.log_response(entry, error=str(e))
                raise
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict) -> List[types.TextContent | types.ImageContent | types.EmbeddedResource]:
            """Handle tool execution with comprehensive logging"""
            start_time = datetime.now()
            entry = self.logger.log_request(
                "TOOL_CALL", 
                "call_tool", 
                name=name, 
                parameters=arguments,
                request_payload={"method": "tools/call", "params": {"name": name, "arguments": arguments}}
            )
            
            try:
                result = None
                
                if name == "get_server_logs":
                    limit = arguments.get("limit", 20)
                    logs_table = self.logger.get_logs_table(limit)
                    logs_summary = f"Showing {min(limit, len(self.logger.get_logs()))} recent log entries"
                    
                    result = [
                        TextContent(type="text", text=f"## Server Logs\n\n{logs_summary}\n\n```\n{logs_table}\n```")
                    ]
                
                elif name == "test_tool":
                    tool_name = arguments.get("tool_name")
                    test_params = arguments.get("parameters", {})
                    
                    if tool_name in self.registered_tools:
                        # Simulate tool testing (in a real implementation, you'd call the actual tool)
                        test_result = f"Testing tool '{tool_name}' with parameters: {json.dumps(test_params, indent=2)}"
                        result = [TextContent(type="text", text=test_result)]
                    else:
                        available_tools = list(self.registered_tools.keys())
                        result = [TextContent(type="text", text=f"Tool '{tool_name}' not found. Available tools: {available_tools}")]
                
                elif name == "hello-world":
                    name_param = arguments.get("name", "World")
                    greeting = f"Hello, {name_param}! 🌍"
                    result = [TextContent(type="text", text=greeting)]
                
                elif name == "calculate":
                    expression = arguments.get("expression", "")
                    try:
                        # Safe evaluation of basic math expressions
                        allowed_chars = set("0123456789+-*/.() ")
                        if all(c in allowed_chars for c in expression):
                            calc_result = eval(expression)
                            result = [TextContent(type="text", text=f"{expression} = {calc_result}")]
                        else:
                            result = [TextContent(type="text", text="Invalid expression. Only basic math operations allowed.")]
                    except Exception as calc_error:
                        result = [TextContent(type="text", text=f"Calculation error: {str(calc_error)}")]
                
                elif name == "get_system_info":
                    import platform
                    import os
                    
                    info = {
                        "platform": platform.platform(),
                        "python_version": platform.python_version(),
                        "working_directory": os.getcwd(),
                        "timestamp": datetime.now().isoformat()
                    }
                    result = [TextContent(type="text", text=f"## System Information\n\n```json\n{json.dumps(info, indent=2)}\n```")]
                
                else:
                    result = [TextContent(type="text", text=f"Unknown tool: {name}")]
                
                response_time = (datetime.now() - start_time).total_seconds() * 1000
                self.logger.log_response(entry, {"result": "success"}, response_time_ms=response_time)
                
                return result
                
            except Exception as e:
                response_time = (datetime.now() - start_time).total_seconds() * 1000
                self.logger.log_response(entry, error=str(e), response_time_ms=response_time)
                return [TextContent(type="text", text=f"Error executing tool '{name}': {str(e)}")]
    
    def _register_demo_tools(self):
        """Register demonstration tools"""
        pass  # Tools are registered in the list_tools handler
    
    def _register_demo_resources(self):
        """Register demonstration resources"""
        
        @self.server.list_resources()
        async def handle_list_resources() -> List[Resource]:
            """List all available resources"""
            start_time = datetime.now()
            entry = self.logger.log_request("RESOURCES", "list_resources", request_payload={"method": "resources/list"})
            
            try:
                resources = [
                    Resource(
                        uri="demo://server-info",
                        name="Server Information",
                        description="Basic information about this MCP server",
                        mimeType="application/json"
                    ),
                    Resource(
                        uri="demo://logs",
                        name="Server Logs",
                        description="Recent server operation logs",
                        mimeType="text/plain"
                    )
                ]
                
                # Store registered resources
                for resource in resources:
                    self.registered_resources[resource.uri] = resource
                
                response_time = (datetime.now() - start_time).total_seconds() * 1000
                self.logger.log_response(entry, {"resources": [r.uri for r in resources]}, response_time_ms=response_time)
                
                return resources
                
            except Exception as e:
                self.logger.log_response(entry, error=str(e))
                raise
        
        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> str:
            """Read resource content with logging"""
            start_time = datetime.now()
            entry = self.logger.log_request(
                "RESOURCE_READ", 
                "read_resource", 
                name=uri,
                request_payload={"method": "resources/read", "params": {"uri": uri}}
            )
            
            try:
                if uri == "demo://server-info":
                    info = {
                        "server_name": "Advanced MCP Server",
                        "version": "1.0.0",
                        "tools_registered": len(self.registered_tools),
                        "resources_registered": len(self.registered_resources),
                        "uptime": datetime.now().isoformat(),
                        "logs_in_memory": len(self.logger.get_logs())
                    }
                    content = json.dumps(info, indent=2)
                
                elif uri == "demo://logs":
                    content = self.logger.get_logs_table(50)
                
                else:
                    content = f"Resource not found: {uri}"
                
                response_time = (datetime.now() - start_time).total_seconds() * 1000
                self.logger.log_response(entry, {"content_length": len(content)}, response_time_ms=response_time)
                
                return content
                
            except Exception as e:
                response_time = (datetime.now() - start_time).total_seconds() * 1000
                self.logger.log_response(entry, error=str(e), response_time_ms=response_time)
                return f"Error reading resource '{uri}': {str(e)}"
    
    def display_startup_info(self):
        """Display server capabilities on startup"""
        print(f"\n{Fore.GREEN}🚀 Advanced MCP Server Starting...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}={'='*80}{Style.RESET_ALL}")
        
        # Display registered tools
        print(f"\n{Fore.YELLOW}📋 REGISTERED TOOLS:{Style.RESET_ALL}")
        if self.registered_tools:
            tool_data = []
            for name, tool in self.registered_tools.items():
                tool_data.append([name, tool.description])
            print(tabulate(tool_data, headers=["Tool Name", "Description"], tablefmt="grid"))
        else:
            print("No tools registered yet.")
        
        # Display registered resources
        print(f"\n{Fore.YELLOW}📦 REGISTERED RESOURCES:{Style.RESET_ALL}")
        if self.registered_resources:
            resource_data = []
            for uri, resource in self.registered_resources.items():
                resource_data.append([resource.name, uri, resource.description])
            print(tabulate(resource_data, headers=["Name", "URI", "Description"], tablefmt="grid"))
        else:
            print("No resources registered yet.")
        
        print(f"\n{Fore.GREEN}✅ Server ready for connections!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
    
    async def run(self):
        """Run the MCP server"""
        # Initialize and display startup info
        await self.server.request_handler.list_tools()  # Trigger tool registration
        await self.server.request_handler.list_resources()  # Trigger resource registration
        self.display_startup_info()
        
        # Run the server
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="advanced-mcp-server",
                    server_version="1.0.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={}
                    )
                )
            )


def main():
    """Main entry point"""
    print(f"{Fore.MAGENTA}Advanced MCP Server with Comprehensive Logging{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}================================================{Style.RESET_ALL}")
    
    server = AdvancedMCPServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()