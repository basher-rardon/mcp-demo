#!/usr/bin/env python3
"""
MCP Comprehensive Playground Server
==================================

This server implements all major MCP feature categories:
- Tools (basic, stateful, streaming, error handling)
- Resources (time, large data, binary content)
- Prompts (template generation)
- Comprehensive logging and error handling

Features demonstrated:
1. Basic arithmetic (add tool)
2. Error handling (fail_on_purpose tool)
3. Streaming responses (countdown tool)
4. Stateful operations (increment_counter tool)
5. Time-based resources (get_time resource)
6. Large context handling (big_text resource)
7. Binary data handling (get_image_base64 resource)
8. Server introspection (get_server_info tool)
9. Prompt templates (prompt_greet prompt)
"""

import asyncio
import json
import logging
import sys
import time
import base64
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Sequence
from dataclasses import dataclass, asdict
import threading
from collections import deque
from io import StringIO

# MCP imports - using fallback for demo if not installed
try:
    from mcp.server.models import InitializationOptions
    from mcp.server import NotificationOptions, Server
    from mcp.types import (
        Resource, Tool, TextContent, ImageContent, EmbeddedResource,
        LoggingLevel, Prompt
    )
    import mcp.types as types
    from mcp.server.stdio import stdio_server
    MCP_AVAILABLE = True
except ImportError:
    print("⚠️  MCP library not found. Run: pip install mcp")
    MCP_AVAILABLE = False


@dataclass
class LogEntry:
    """Comprehensive log entry for all MCP operations"""
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
    streaming: bool = False
    stream_events: List[Dict] = None


class ComprehensiveLogger:
    """Advanced logging system with real-time capabilities"""
    
    def __init__(self, max_memory_logs: int = 2000):
        self.memory_logs: deque = deque(maxlen=max_memory_logs)
        self.lock = threading.Lock()
        self.log_callbacks = []  # For real-time updates
        
        # Setup comprehensive logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # File handler
        file_handler = logging.FileHandler('mcp_playground.log')
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def add_callback(self, callback):
        """Add callback for real-time log updates"""
        self.log_callbacks.append(callback)
    
    def log_request(self, request_type: str, operation: str, name: str = None, 
                   parameters: Dict = None, request_payload: Dict = None) -> LogEntry:
        """Log an incoming MCP request"""
        entry = LogEntry(
            timestamp=datetime.now(timezone.utc).isoformat(),
            request_type=request_type,
            operation=operation,
            name=name,
            parameters=parameters or {},
            request_payload=request_payload or {},
            stream_events=[]
        )
        
        with self.lock:
            self.memory_logs.append(entry)
        
        # Console output
        print(f"📥 REQUEST [{entry.timestamp}] {request_type} - {operation}")
        if name:
            print(f"   Name: {name}")
        if parameters:
            print(f"   Params: {json.dumps(parameters, indent=2)}")
        
        self.logger.info(f"REQUEST: {request_type} - {operation} - {name}")
        
        # Notify callbacks
        for callback in self.log_callbacks:
            try:
                callback(entry)
            except Exception as e:
                print(f"Log callback error: {e}")
        
        return entry
    
    def log_response(self, entry: LogEntry, response_payload: Dict = None, 
                    error: str = None, response_time_ms: float = None):
        """Log an MCP response"""
        entry.response_payload = response_payload
        entry.error = error
        entry.success = error is None
        entry.response_time_ms = response_time_ms
        
        # Console output
        status = "✅" if entry.success else "❌"
        print(f"{status} RESPONSE [{entry.timestamp}] {entry.operation}")
        if response_time_ms:
            print(f"   Duration: {response_time_ms:.2f}ms")
        if error:
            print(f"   Error: {error}")
        
        self.logger.info(f"RESPONSE: {entry.operation} - {'SUCCESS' if entry.success else 'ERROR'}")
        
        # Notify callbacks
        for callback in self.log_callbacks:
            try:
                callback(entry)
            except Exception as e:
                print(f"Log callback error: {e}")
    
    def log_stream_event(self, entry: LogEntry, event_data: Dict):
        """Log a streaming event"""
        entry.streaming = True
        entry.stream_events.append({
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'data': event_data
        })
        
        print(f"🔄 STREAM [{entry.timestamp}] {entry.operation} - {event_data}")
        self.logger.info(f"STREAM: {entry.operation} - {json.dumps(event_data)}")
        
        # Notify callbacks
        for callback in self.log_callbacks:
            try:
                callback(entry)
            except Exception as e:
                print(f"Log callback error: {e}")
    
    def get_logs(self, limit: int = None) -> List[LogEntry]:
        """Get recent logs from memory"""
        with self.lock:
            logs = list(self.memory_logs)
            if limit:
                logs = logs[-limit:]
            return logs
    
    def export_logs(self, filename: str = None) -> str:
        """Export logs to JSON file"""
        if not filename:
            filename = f"mcp_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        logs = self.get_logs()
        logs_data = [asdict(log) for log in logs]
        
        with open(filename, 'w') as f:
            json.dump(logs_data, f, indent=2, default=str)
        
        return filename


class MCPPlaygroundServer:
    """Comprehensive MCP Server demonstrating all major features"""
    
    def __init__(self):
        if not MCP_AVAILABLE:
            raise ImportError("MCP library not available. Install with: pip install mcp")
        
        self.server = Server("mcp-playground-server")
        self.logger = ComprehensiveLogger()
        self.start_time = datetime.now(timezone.utc)
        
        # Stateful data
        self.counter = 0
        self.counter_lock = threading.Lock()
        
        # Register all features
        self._register_tools()
        self._register_resources()
        self._register_prompts()
        
        print("🚀 MCP Playground Server initialized with comprehensive features")
    
    def _register_tools(self):
        """Register all demonstration tools"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """List all available tools"""
            start_time = time.time()
            entry = self.logger.log_request("TOOLS", "list_tools", 
                                           request_payload={"method": "tools/list"})
            
            try:
                tools = [
                    Tool(
                        name="add",
                        description="Add two numbers together - demonstrates basic tool functionality",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "a": {"type": "integer", "description": "First number"},
                                "b": {"type": "integer", "description": "Second number"}
                            },
                            "required": ["a", "b"]
                        }
                    ),
                    Tool(
                        name="fail_on_purpose",
                        description="Always fails - demonstrates error handling in MCP",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "message": {
                                    "type": "string", 
                                    "description": "Custom error message (optional)",
                                    "default": "Intentional test error"
                                }
                            }
                        }
                    ),
                    Tool(
                        name="countdown",
                        description="Stream countdown from N to 1 - demonstrates streaming responses",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "n": {
                                    "type": "integer",
                                    "description": "Number to count down from",
                                    "minimum": 1,
                                    "maximum": 10,
                                    "default": 5
                                }
                            },
                            "required": ["n"]
                        }
                    ),
                    Tool(
                        name="increment_counter",
                        description="Increment server-side counter - demonstrates stateful operations",
                        inputSchema={
                            "type": "object",
                            "properties": {}
                        }
                    ),
                    Tool(
                        name="get_server_info",
                        description="Get server information - demonstrates introspection capabilities",
                        inputSchema={
                            "type": "object",
                            "properties": {}
                        }
                    )
                ]
                
                response_time = (time.time() - start_time) * 1000
                self.logger.log_response(entry, {"tools": [t.name for t in tools]}, 
                                       response_time_ms=response_time)
                
                return tools
                
            except Exception as e:
                self.logger.log_response(entry, error=str(e))
                raise
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict) -> List[types.TextContent]:
            """Handle tool execution with comprehensive logging"""
            start_time = time.time()
            entry = self.logger.log_request(
                "TOOL_CALL", "call_tool", name=name, parameters=arguments,
                request_payload={"method": "tools/call", "params": {"name": name, "arguments": arguments}}
            )
            
            try:
                if name == "add":
                    a = arguments.get("a", 0)
                    b = arguments.get("b", 0)
                    result = a + b
                    content = f"Adding {a} + {b} = {result}"
                    
                elif name == "fail_on_purpose":
                    error_msg = arguments.get("message", "Intentional test error")
                    raise Exception(error_msg)
                    
                elif name == "countdown":
                    n = arguments.get("n", 5)
                    # For demo purposes, we'll return a summary instead of true streaming
                    # True streaming would require WebSocket or SSE implementation
                    countdown_text = []
                    for i in range(n, 0, -1):
                        countdown_text.append(f"Countdown: {i}")
                        # Log each streaming event
                        self.logger.log_stream_event(entry, {"count": i, "remaining": i-1})
                        await asyncio.sleep(0.1)  # Simulate delay
                    
                    content = "\\n".join(countdown_text) + "\\nCountdown complete!"
                    
                elif name == "increment_counter":
                    with self.counter_lock:
                        self.counter += 1
                        current_count = self.counter
                    content = f"Counter incremented to: {current_count}"
                    
                elif name == "get_server_info":
                    uptime = datetime.now(timezone.utc) - self.start_time
                    info = {
                        "server_name": "MCP Playground Server",
                        "version": "1.0.0",
                        "uptime_seconds": int(uptime.total_seconds()),
                        "uptime_human": str(uptime).split('.')[0],
                        "features": {
                            "tools": 5,
                            "resources": 3,
                            "prompts": 1,
                            "streaming": "Simulated",
                            "stateful": True,
                            "error_handling": True
                        },
                        "current_counter": self.counter,
                        "logs_in_memory": len(self.logger.get_logs())
                    }
                    content = f"Server Information:\\n{json.dumps(info, indent=2)}"
                    
                else:
                    raise Exception(f"Unknown tool: {name}")
                
                response_time = (time.time() - start_time) * 1000
                self.logger.log_response(entry, {"result": "success"}, 
                                       response_time_ms=response_time)
                
                return [types.TextContent(type="text", text=content)]
                
            except Exception as e:
                response_time = (time.time() - start_time) * 1000
                self.logger.log_response(entry, error=str(e), 
                                       response_time_ms=response_time)
                return [types.TextContent(type="text", text=f"Error: {str(e)}")]
    
    def _register_resources(self):
        """Register all demonstration resources"""
        
        @self.server.list_resources()
        async def handle_list_resources() -> List[Resource]:
            """List all available resources"""
            start_time = time.time()
            entry = self.logger.log_request("RESOURCES", "list_resources", 
                                           request_payload={"method": "resources/list"})
            
            try:
                resources = [
                    Resource(
                        uri="time://current",
                        name="Current Server Time",
                        description="Returns the current server time in ISO format",
                        mimeType="text/plain"
                    ),
                    Resource(
                        uri="data://big_text",
                        name="Large Text Data",
                        description="Returns a large text string for context window testing (10KB+)",
                        mimeType="text/plain"
                    ),
                    Resource(
                        uri="image://tiny_png_base64",
                        name="Tiny PNG Image (Base64)",
                        description="Returns a small PNG image encoded as base64 for binary handling demo",
                        mimeType="image/png"
                    )
                ]
                
                response_time = (time.time() - start_time) * 1000
                self.logger.log_response(entry, {"resources": [r.uri for r in resources]}, 
                                       response_time_ms=response_time)
                
                return resources
                
            except Exception as e:
                self.logger.log_response(entry, error=str(e))
                raise
        
        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> str:
            """Read resource content with comprehensive logging"""
            start_time = time.time()
            entry = self.logger.log_request(
                "RESOURCE_READ", "read_resource", name=uri,
                request_payload={"method": "resources/read", "params": {"uri": uri}}
            )
            
            try:
                if uri == "time://current":
                    content = datetime.now(timezone.utc).isoformat()
                    
                elif uri == "data://big_text":
                    # Generate a large text string (approximately 10KB)
                    lorem_base = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""
                    
                    # Repeat to create ~10KB of text
                    repetitions = 10000 // len(lorem_base) + 1
                    content = f"=== LARGE TEXT RESOURCE FOR CONTEXT TESTING ===\\n"
                    content += f"Generated at: {datetime.now(timezone.utc).isoformat()}\\n"
                    content += f"Size: ~{len(lorem_base) * repetitions} characters\\n"
                    content += "="*50 + "\\n\\n"
                    content += (lorem_base + "\\n\\n") * repetitions
                    content += "\\n=== END OF LARGE TEXT RESOURCE ==="
                    
                elif uri == "image://tiny_png_base64":
                    # Create a tiny 8x8 PNG image (red square)
                    # This is a minimal PNG file in base64
                    tiny_png_b64 = """iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAAdgAAAHYBTnsmCAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAABESURBVBiVY/z//z8DAwMDw3+cYP///wwMDAyM/3GC////MzAwMDD+xwn+//8PxijO+Y8D/P//nwEbwKmAEVcBTgVYFQAAAAD//2JgYGAAAAAA//9iYGBgAAAAAP//YmBgYAAAAAD//2JgYGAAAAAA//9iYGBgAAAAAP//YmBgYAAAAAD//w=="""
                    content = f"data:image/png;base64,{tiny_png_b64}"
                    
                else:
                    raise Exception(f"Unknown resource URI: {uri}")
                
                response_time = (time.time() - start_time) * 1000
                self.logger.log_response(entry, {"content_length": len(content)}, 
                                       response_time_ms=response_time)
                
                return content
                
            except Exception as e:
                response_time = (time.time() - start_time) * 1000
                self.logger.log_response(entry, error=str(e), 
                                       response_time_ms=response_time)
                return f"Error reading resource '{uri}': {str(e)}"
    
    def _register_prompts(self):
        """Register all demonstration prompts"""
        
        @self.server.list_prompts()
        async def handle_list_prompts() -> List[Prompt]:
            """List all available prompts"""
            start_time = time.time()
            entry = self.logger.log_request("PROMPTS", "list_prompts", 
                                           request_payload={"method": "prompts/list"})
            
            try:
                prompts = [
                    Prompt(
                        name="prompt_greet",
                        description="Generate a friendly greeting prompt for a given name",
                        arguments=[
                            {
                                "name": "name",
                                "description": "The name of the person to greet",
                                "required": True
                            }
                        ]
                    )
                ]
                
                response_time = (time.time() - start_time) * 1000
                self.logger.log_response(entry, {"prompts": [p.name for p in prompts]}, 
                                       response_time_ms=response_time)
                
                return prompts
                
            except Exception as e:
                self.logger.log_response(entry, error=str(e))
                raise
        
        @self.server.get_prompt()
        async def handle_get_prompt(name: str, arguments: dict) -> types.GetPromptResult:
            """Handle prompt generation with logging"""
            start_time = time.time()
            entry = self.logger.log_request(
                "PROMPT_GET", "get_prompt", name=name, parameters=arguments,
                request_payload={"method": "prompts/get", "params": {"name": name, "arguments": arguments}}
            )
            
            try:
                if name == "prompt_greet":
                    target_name = arguments.get("name", "World")
                    prompt_text = f"Write a friendly greeting for {target_name}."
                    
                    result = types.GetPromptResult(
                        description=f"Greeting prompt for {target_name}",
                        messages=[
                            types.PromptMessage(
                                role=types.Role.user,
                                content=types.TextContent(type="text", text=prompt_text)
                            )
                        ]
                    )
                    
                    response_time = (time.time() - start_time) * 1000
                    self.logger.log_response(entry, {"prompt_generated": True}, 
                                           response_time_ms=response_time)
                    
                    return result
                    
                else:
                    raise Exception(f"Unknown prompt: {name}")
                    
            except Exception as e:
                response_time = (time.time() - start_time) * 1000
                self.logger.log_response(entry, error=str(e), 
                                       response_time_ms=response_time)
                raise
    
    def get_comprehensive_logs(self, limit: int = 100) -> List[Dict]:
        """Get logs formatted for web interface"""
        logs = self.logger.get_logs(limit)
        return [asdict(log) for log in logs]
    
    def export_logs(self, filename: str = None) -> str:
        """Export logs to file"""
        return self.logger.export_logs(filename)
    
    async def run(self):
        """Run the MCP playground server"""
        print("🎮 Starting MCP Playground Server...")
        print("="*60)
        print("Features available:")
        print("📊 Tools: add, fail_on_purpose, countdown, increment_counter, get_server_info")
        print("📦 Resources: current_time, big_text, tiny_png_base64")
        print("💬 Prompts: prompt_greet")
        print("📝 Comprehensive logging with export capabilities")
        print("="*60)
        
        # Initialize server capabilities
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="mcp-playground-server",
                    server_version="1.0.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={}
                    )
                )
            )


def main():
    """Main entry point"""
    if not MCP_AVAILABLE:
        print("❌ MCP library not available. Install with:")
        print("   pip install mcp")
        sys.exit(1)
    
    print("🎮 MCP Comprehensive Playground Server")
    print("=====================================")
    
    server = MCPPlaygroundServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()