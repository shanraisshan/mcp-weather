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

Claude Code supports HTTP MCP servers with three configuration scopes. Make sure the server is running before adding it.

**Prerequisites**:
- Claude Code CLI installed
- Server running: `python3 server.py` (on `http://localhost:8003`)

**Method 1: Using CLI Command (Recommended)**

First, make sure the MCP server is running:
```bash
python3 server.py
```

Then add the MCP server using the Claude CLI:

```bash
# Local scope (default - personal development)
claude mcp add --transport sse weather http://localhost:8003/sse

# Project scope (shared via .mcp.json in project root)
claude mcp add --transport sse weather --scope project http://localhost:8003/sse

# User scope (available across all projects)
claude mcp add --transport sse weather --scope user http://localhost:8003/sse
```

**Note**: Use SSE transport for Claude CLI. HTTP transport is not currently supported by the Claude CLI.

**Method 2: Manual Configuration (Project Scope)**

Create `.mcp.json` in your project root:

```json
{
  "mcpServers": {
    "weather": {
      "type": "sse",
      "url": "http://localhost:8003/sse"
    }
  }
}
```

Also in .claude/settings.json:
```json
{
  "enableAllProjectMcpServers": true
}
```

This configuration will be shared with your team via version control.

**Configuration Scopes**:

| Scope | Use Case | Location |
|-------|----------|----------|
| **Local** | Personal development, experimental configs | User settings |
| **Project** | Team-shared configuration | `.mcp.json` in project root |
| **User** | Personal utilities across all projects | User settings |

**Scope Precedence**: Local > Project > User

**Usage**:
1. Make sure the MCP server is running: `python3 server.py`
2. The `get_karachi_weather` tool will be available automatically
3. Ask Claude: "What's the weather in Karachi?"
4. Or use slash command in Claude Code: `/mcp` to view available tools

**Management Commands**:
```bash
# List all configured servers
claude mcp list

# Get details for specific server
claude mcp get weather

# Remove a server
claude mcp remove weather

# Check server status (within Claude Code)
/mcp
```

**Verification**:
```bash
claude mcp list
```

You should see "weather" in the list of configured servers.

### For Augment Code

Augment Code supports MCP servers and provides three methods to configure them. Make sure the HTTP server is running on `http://localhost:8003` before configuration.

**Prerequisites**:
- Augment Code extension installed in VS Code
- Server running: `python3 server.py`

**Method 1: Settings Panel (Recommended)**

1. Open the Augment panel in VS Code
2. Click the **options menu** (hamburger icon) in the upper right
3. Select **Settings**
4. Scroll to the **MCP servers** section
5. Click **"+ Add remote MCP"**
6. Fill in the configuration:
   - **Name**: `weather`
   - **Connection type**: `SSE`
   - **Base URL**: `http://localhost:8003/sse`
7. Click **Save**

**Method 2: JSON Import**

1. Open Augment Settings (gear icon)
2. Click **"Import from JSON"** in the MCP section
3. Paste this configuration:

```json
{
  "mcpServers": {
    "weather": {
      "url": "http://localhost:8003/sse",
      "type": "sse"
    }
  }
}
```

4. Click **Save**

**Usage with Augment Code**:

1. The `get_karachi_weather` tool will be available in Augment Agent
2. Ask questions like:
   - "What's the current weather in Karachi?"
   - "Check the weather conditions in Karachi"
   - "Tell me the temperature in Karachi"

**Verification**:

- Check the MCP servers list in Settings to confirm "weather" appears
- Look for the weather tool in Augment Agent's available tools

**Note**: Ensure the HTTP server (`python3 server.py`) is running before using the tool.

### For VSCode GitHub Copilot

GitHub Copilot in VSCode supports MCP servers starting from **VS Code 1.102**. This enables Copilot to access real-time weather data.

**Prerequisites**:
- VS Code 1.102 or later
- GitHub Copilot subscription
- MCP support enabled in your organization (if applicable)
- Server running: `python3 server.py`

**Method 1: Via Command Palette (Recommended)**

1. Make sure the server is running: `python3 server.py`
2. Open Command Palette (Ctrl/Cmd + Shift + P)
3. Run command: **"MCP: Add Server"**
4. Choose **"Workspace"** or **"Global"** scope
5. Fill in the configuration:
   - **Name**: `weather`
   - **Type**: `http` or `sse`
   - **URL**: `http://localhost:8003/sse`

**Method 2: Manual Configuration**

Create or edit `.vscode/mcp.json` in your workspace:

```json
{
  "servers": {
    "weather": {
      "type": "sse",
      "url": "http://localhost:8003/sse"
    }
  }
}
```

**For global configuration**, use Command Palette: **"MCP: Open User Configuration"**

**Usage with GitHub Copilot**:

1. Ensure the server is running: `python3 server.py`
2. Open GitHub Copilot Chat (Ctrl/Cmd + Alt + I)
3. Enable **Agent Mode** if available
4. The `get_karachi_weather` tool will be available in the tool picker
5. Ask questions like:
   - "What's the current weather in Karachi?"
   - "Check the weather conditions"
   - "Tell me the temperature in Karachi"

**Verification**:

1. Run Command Palette: **"MCP: List Servers"**
2. Verify "weather" appears in the list with status "Running"
3. Open Copilot Chat and check the tool picker for `get_karachi_weather`

**Troubleshooting**:

- Ensure the HTTP server is running before using Copilot
- Run **"MCP: List Servers"** → Select "weather" → Click "Show Output" to view logs
- Use **"MCP: Reset Cached Tools"** to refresh tool discovery
- Restart VS Code after configuration changes
- If trust dialog appears, confirm you trust the server before proceeding

**Security Note**: VS Code will display a trust confirmation when adding the server. Only add MCP servers from trusted sources as they can execute code on your machine.

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
