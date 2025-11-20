# MCP Weather Server for Karachi

A collection of Model Context Protocol (MCP) servers that fetch current weather data for Karachi, Pakistan using the Open-Meteo API.

## What is MCP?

**Model Context Protocol (MCP)** is an open protocol that standardizes how applications provide context to Large Language Models (LLMs). It enables seamless integration between LLM applications (like Claude Desktop, IDEs, or AI tools) and external data sources or tools.

### Key Concepts

- **MCP Server**: A program that exposes specific capabilities (tools, resources, prompts) to MCP clients
- **MCP Client**: An application (like Claude Desktop) that connects to MCP servers to access their capabilities
- **Transport Types**:
  - **stdio (command-based)**: Server runs as a subprocess, communicates via standard input/output
  - **HTTP with SSE**: Server runs as an HTTP service, uses Server-Sent Events for communication

### Benefits

- Standardized way to extend LLM capabilities
- Connect LLMs to databases, APIs, file systems, and more
- Reusable across different MCP-compatible applications
- Secure, controlled access to external resources

## Available Implementations

This repository provides two MCP server implementations:

### 1. [HTTP Server (Python)](./http/)

**Type**: HTTP with Server-Sent Events (SSE)
**Language**: Python
**Port**: 8003
**Best for**: Running as a standalone service, multiple clients, production deployments

```json
{
  "mcpServers": {
    "weather": {
      "transport": "http",
      "url": "http://localhost:8003/sse",
      "description": "Karachi weather data from Open-Meteo API"
    }
  }
}
```

[→ View HTTP Implementation Details](./http/)

### 2. [Command Server (Node.js)](./command/)

**Type**: stdio (command-based)
**Language**: TypeScript/Node.js
**Best for**: Local development, single client, simpler setup

```json
{
  "mcpServers": {
    "weather": {
      "command": "node",
      "args": ["/path/to/command/dist/index.js"]
    }
  }
}
```

[→ View Command Implementation Details](./command/)

## Features

Both implementations provide:

- Current weather conditions for Karachi, Pakistan
- Temperature, humidity, wind speed, and precipitation data
- Human-readable weather condition descriptions
- Free API (Open-Meteo) - no API key required

## Tool Available

Both servers expose the same tool:

- **`get_karachi_weather`**: Fetches current weather conditions for Karachi

### Example Response

```json
{
  "location": "Karachi, Pakistan",
  "timestamp": "2025-01-20T10:30",
  "temperature": "22.5°C",
  "feels_like": "21.8°C",
  "humidity": "65%",
  "wind_speed": "15.2 km/h",
  "precipitation": "0 mm",
  "conditions": "Partly cloudy",
  "weather_code": 2
}
```

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

**Command Server (Node.js)**:
```bash
cd command
npm install
npm run build
npm start
```

## Learn More

- [MCP Documentation](https://modelcontextprotocol.io/)
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [Anthropic MCP Guide](https://docs.anthropic.com/claude/docs/model-context-protocol)
- [Open-Meteo API](https://open-meteo.com/)

## License

MIT
