# MCP Weather Server for Karachi (HTTP)

A Python-based Model Context Protocol (MCP) HTTP server that fetches current weather data for Karachi, Pakistan using the Open-Meteo API.

## Features

- HTTP-based MCP server (not command-line based)
- Get current weather conditions for Karachi
- Returns temperature, humidity, wind speed, precipitation, and weather conditions
- Uses free Open-Meteo API (no API key required)

## Installation

```bash
# Create a virtual environment (recommended)
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install Python dependencies
pip3 install -r requirements.txt
```

## Running the Server

```bash
# Make sure your virtual environment is activated first
python3 server.py
```

The server will start on `http://localhost:8003`

## Usage in Your Project

### For Claude Desktop

Add this configuration to your Claude Desktop config file:

**MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

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

### For Claude Code CLI

**Method 1: Using CLI Command (Recommended)**

First, make sure the MCP server is running:
```bash
python3 server.py
```

Then add the MCP server using the Claude CLI:
```bash
claude mcp add --transport http weather "http://localhost:8003/sse"
```

**Method 2: Manual Configuration**

Alternatively, create or edit the MCP configuration file:

**MacOS/Linux**: `~/.config/claude-code/mcp.json`

**Windows**: `%APPDATA%\claude-code\mcp.json`

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

**Usage**:
1. Make sure the MCP server is running (`python3 server.py`)
2. The `get_karachi_weather` tool will be available automatically in Claude Code CLI
3. Ask Claude: "What's the weather in Karachi?" and it will use the MCP tool

**Verify Installation**:
```bash
claude mcp list
```

### For Other MCP Clients

Connect to the HTTP server at:
- **Base URL**: `http://localhost:8003`
- **SSE Endpoint**: `http://localhost:8003/sse`

The server provides one tool:

- `get_karachi_weather`: Fetches current weather for Karachi

## Example Response

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

## API Used

This server uses the free [Open-Meteo API](https://open-meteo.com/) which requires no API key.

## Technical Details

- Built with Python MCP SDK
- Uses Server-Sent Events (SSE) for communication
- Async/await for efficient HTTP requests
- Runs on uvicorn ASGI server
