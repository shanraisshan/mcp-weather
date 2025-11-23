# MCP Weather Server for Karachi

A collection of Model Context Protocol (MCP) servers that fetch current weather data for Karachi, Pakistan using the Open-Meteo API.

## What is MCP?

**Model Context Protocol (MCP)** is an open protocol that standardizes how applications provide context to Large Language Models (LLMs). It enables seamless integration between LLM applications (like Claude Desktop, IDEs, or AI tools) and external data sources or tools.

### Deployment 

Render -> shayanrais.gt

![](/!/render.png)

### Key Concepts

- **MCP Server**: A program that exposes specific capabilities (tools, resources, prompts) to MCP clients
- **MCP Client**: An application (like Claude Desktop) that connects to MCP servers to access their capabilities
- **Transport Types**:
  - **stdio (command-based)**: Server runs as a subprocess, communicates via standard input/output
  - **Streamable HTTP**: Server runs as an HTTP service, uses the modern MCP protocol for communication

## Available Implementations

This repository provides two MCP server implementations:

### 1. [HTTP Server (Python)](./http/)

**Type**: Streamable HTTP (FastMCP 2.3+)
**Language**: Python
**Port**: 8003

```json
{
  "mcpServers": {
    "weather": {
      "serverUrl": "http://localhost:8003/mcp",
      "description": "Karachi weather data from Open-Meteo API"
    }
  }
}
```

[→ View HTTP Implementation Details](./http/)

### 2. [Command Server (Python)](./command/)

**Type**: stdio (command-based)
**Language**: Python

```json
{
  "mcpServers": {
    "weather": {
      "command": "python3",
      "args": ["/absolute/path/to/command/server.py"]
    }
  }
}
```

[→ View Command Implementation Details](./command/)

## Tool Available

Both servers expose the same tool:

- **`get_karachi_weather`**: Fetches current weather conditions for Karachi

## Quick Start

Choose the implementation that best fits your needs:

**HTTP Server (Python)**:
```bash
cd http
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip3 install -r requirements.txt
python3 server.py
```

**Command Server (Python)**:
```bash
cd command
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip3 install -r requirements.txt
python3 server.py
```
