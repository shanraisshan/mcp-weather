# MCP Weather Server for Karachi (Streamable HTTP)

A Python-based Model Context Protocol (MCP) server that fetches current weather data for Karachi, Pakistan using the Open-Meteo API. Built with FastMCP 2.3+ using the modern Streamable HTTP transport.

## Features

- **Streamable HTTP** MCP server (modern MCP standard)
- Compatible with Google Antigravity IDE, Claude Desktop, Claude Code CLI, Augment Code, and VS Code Copilot
- Get current weather conditions for Karachi
- Returns temperature, humidity, wind speed, precipitation, and weather conditions
- Uses free Open-Meteo API (no API key required)
- Built with FastMCP 2.3+ for optimal performance

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
      "serverUrl": "http://localhost:8003/mcp",
      "description": "Karachi weather data from Open-Meteo API"
    }
  }
}
```

**Note**: This uses the modern Streamable HTTP transport. Make sure you're running the server with FastMCP 2.3+ and `transport="http"` (which is the default in this project).

### For Claude Code CLI

Claude Code supports HTTP MCP servers with three configuration scopes. Make sure the server is running before adding it.

**Prerequisites**:
- Claude Code CLI installed
- FastMCP 2.3+ installed: `pip install --upgrade fastmcp`
- Server running: `python3 server.py` (on `http://localhost:8003`)

**Method 1: Using CLI Command (Recommended)**

First, make sure the MCP server is running:
```bash
python3 server.py
```

Then add the MCP server using the Claude CLI:

```bash
# Local scope (default - personal development)
claude mcp add weather http://localhost:8003/mcp

# Project scope (shared via .mcp.json in project root)
claude mcp add weather --scope project http://localhost:8003/mcp

# User scope (available across all projects)
claude mcp add weather --scope user http://localhost:8003/mcp
```

**Note**: This uses Streamable HTTP transport. Make sure your server is running with FastMCP 2.3+ and `transport="http"`.

**Method 2: Manual Configuration (Project Scope)**

Create `.mcp.json` in your project root:

```json
{
  "mcpServers": {
    "weather": {
      "url": "http://localhost:8003/mcp"
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
   - **Connection type**: `HTTP` (or `Streamable HTTP` if available)
   - **Base URL**: `http://localhost:8003/mcp`
7. Click **Save**

**Method 2: JSON Import**

1. Open Augment Settings (gear icon)
2. Click **"Import from JSON"** in the MCP section
3. Paste this configuration:

```json
{
  "mcpServers": {
    "weather": {
      "url": "http://localhost:8003/mcp"
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
   - **Type**: `http` (Streamable HTTP)
   - **URL**: `http://localhost:8003/mcp`

**Method 2: Manual Configuration**

Create or edit `.vscode/mcp.json` in your workspace:

```json
{
  "servers": {
    "weather": {
      "type": "http",
      "url": "http://localhost:8003/mcp"
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

### For Google Antigravity IDE

Google Antigravity is an agent-first IDE powered by Gemini 3 Pro. It supports MCP servers through both STDIO (local processes) and Streamable HTTP (remote servers) transports.

**Prerequisites**:
- Google Antigravity IDE installed (Public Preview)
- FastMCP 2.3+ installed: `pip install --upgrade fastmcp`
- Server running: `python3 server.py` (on `http://localhost:8003`)

**Step-by-Step Configuration**:

1. **Install/Update FastMCP**:
   ```bash
   # Activate your virtual environment first
   source venv/bin/activate  # On macOS/Linux
   # venv\Scripts\activate  # On Windows

   # Upgrade to FastMCP 2.3+ (required for Streamable HTTP)
   pip install --upgrade fastmcp
   ```

2. **Start the MCP Server**:
   ```bash
   python3 server.py
   ```
   Ensure the server is running on `http://localhost:8003`

3. **Open MCP Configuration in Antigravity**:
   - Click on the **Agent** session in your workspace
   - Select the **"..."** (more options) dropdown at the top of the editor's side panel
   - Choose **"MCP Servers"** to open the MCP Store

4. **Add Custom MCP Server**:
   - Click **"Manage MCP Servers"** at the top of the MCP Store
   - Select **"View raw config"** in the main tab
   - This opens the `mcp_config.json` file for editing

5. **Configure the Weather Server**:

   Add this configuration to your `mcp_config.json`:

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

   **Alternative: If you have multiple MCP servers already configured**:

   ```json
   {
     "mcpServers": {
       "firebase-mcp-server": {
         "command": "npx",
         "args": ["-y", "firebase-tools@14.20.0", "mcp"]
       },
       "weather": {
         "serverUrl": "http://localhost:8003/mcp",
         "description": "Karachi weather data from Open-Meteo API"
       }
     }
   }
   ```

6. **Save the Configuration**:
   - Save the `mcp_config.json` file
   - Antigravity will automatically detect and load the new MCP server
   - Click **Refresh** in the "Manage MCP servers" panel to reload the configuration

**Usage with Gemini 3 Agent**:

Once configured, the Gemini 3 agent in Antigravity can automatically discover and use the weather tool:

1. Open a new chat with the Gemini 3 agent
2. The `get_karachi_weather` tool will be available in the agent's tool picker
3. Ask questions like:
   - "What's the current weather in Karachi?"
   - "Check the weather conditions in Karachi"
   - "Tell me the temperature and humidity in Karachi"
4. The Gemini 3 agent will automatically call the MCP server to fetch real-time weather data

**Verification**:

1. After saving the configuration, go back to **MCP Servers** in the Agent pane
2. Verify that "weather" appears in the list of configured servers
3. Check that the server status shows as "Connected" or "Running"
4. Test by asking the Gemini 3 agent: "What's the weather in Karachi?"

**Troubleshooting**:

- **Server not connecting**: Ensure `python3 server.py` is running and accessible at `http://localhost:8003`
- **Tool not appearing**: Refresh the MCP configuration by restarting Antigravity or reloading the window
- **Gemini 3 not using the tool**: Explicitly mention "Check the weather in Karachi" to prompt tool usage
- **Configuration errors**: Validate your JSON syntax in `mcp_config.json` - missing commas or brackets can cause issues
- **Port conflicts**: If port 8003 is in use, modify `server.py` to use a different port and update the `serverUrl` accordingly

**Configuration Scopes**:

Google Antigravity uses a single global `mcp_config.json` file accessed through the "View raw config" option. All MCP servers configured here are available across all projects within Antigravity.

**Transport Support**:

| Transport Type | Use Case | Configuration Key |
|----------------|----------|-------------------|
| **STDIO** | Local command-based servers | `"command"` + `"args"` |
| **Streamable HTTP** | Remote or localhost HTTP servers (recommended) | `"serverUrl"` |

**Important Notes**:
- This server uses **Streamable HTTP** (FastMCP 2.3+), the new MCP standard recommended for all deployments
- The correct URL is `http://localhost:8003/mcp` (FastMCP's Streamable HTTP endpoint)
- Antigravity automatically negotiates the Streamable HTTP protocol with compatible servers
- Make sure to upgrade FastMCP to version 2.3+ for Streamable HTTP support

**Security Note**: Only add MCP servers from trusted sources, as they can execute code and access data within your Antigravity environment.

### For Other MCP Clients

Connect to the Streamable HTTP server at:
- **Base URL**: `http://localhost:8003/mcp`
- **Transport**: Streamable HTTP (MCP standard)
- **Requires**: FastMCP 2.3+ or compatible MCP client with Streamable HTTP support

The server provides one tool:

- `get_karachi_weather`: Fetches current weather for Karachi

**Legacy Support**: If you encounter a client that doesn't support Streamable HTTP yet, you can temporarily run the server with SSE by modifying `server.py` line 110 to use `transport="sse"` and updating client URLs to `http://localhost:8003/sse`. However, Streamable HTTP is the modern standard and is recommended for all deployments.

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

- Built with FastMCP 2.3+ (Python MCP framework)
- Uses **Streamable HTTP** transport (modern MCP standard)
- Async/await for efficient HTTP requests
- Runs on uvicorn ASGI server
- Compatible with all modern MCP clients including Google Antigravity IDE

**Legacy Client Compatibility**: This server uses Streamable HTTP (the modern MCP standard). If you need to support an older client that requires the deprecated SSE transport, modify `server.py` line 110 to use `transport="sse"` instead of `transport="http"`, and update all client configurations to use `http://localhost:8003/sse` as the endpoint. Note that SSE is deprecated and Streamable HTTP should be used for all new deployments.
