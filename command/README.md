# MCP Weather Server for Karachi (Command)

A Python-based Model Context Protocol (MCP) command server that fetches current weather data for Karachi, Pakistan using the Open-Meteo API.

## Features

- Command-based MCP server using stdio transport
- Get current weather conditions for Karachi
- Returns temperature, humidity, wind speed, precipitation, and weather conditions
- Uses free Open-Meteo API (no API key required)
- Built with FastMCP for simplified MCP server development

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

The server will run using stdio transport (standard input/output) for communication with MCP clients.

## Usage in Your Project

### For Claude Desktop

Add this configuration to your Claude Desktop config file:

**MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "weather": {
      "command": "python3",
      "args": ["/absolute/path/to/mcp-weather/command/server.py"],
      "description": "Karachi weather data from Open-Meteo API"
    }
  }
}
```

**Note**: Replace `/absolute/path/to/mcp-weather/command/server.py` with the actual absolute path to the server.py file on your system.

### For Claude Code CLI

Claude Code supports stdio MCP servers with three configuration scopes. This server runs as a subprocess using stdio transport.

**Prerequisites**:
- Claude Code CLI installed
- Python dependencies installed: `pip3 install -r requirements.txt`

**Method 1: Using CLI Command (Recommended)**

Add the MCP server using the Claude CLI with stdio transport:

```bash
# Local scope (default - personal development)
claude mcp add --transport stdio weather -- python3 /absolute/path/to/mcp-weather/command/server.py

# Project scope (shared via .mcp.json in project root)
claude mcp add --transport stdio weather --scope project -- python3 /absolute/path/to/mcp-weather/command/server.py

# User scope (available across all projects)
claude mcp add --transport stdio weather --scope user -- python3 /absolute/path/to/mcp-weather/command/server.py
```

**Important**: The double dash (`--`) separates Claude's flags from the server command.

**Using Virtual Environment**:

If using a virtual environment, specify the full Python path:

```bash
claude mcp add --transport stdio weather -- /absolute/path/to/mcp-weather/command/venv/bin/python3 /absolute/path/to/mcp-weather/command/server.py
```

**Method 2: Manual Configuration (Project Scope)**

Create `.mcp.json` in your project root:

```json
{
  "mcpServers": {
    "weather": {
      "command": "python3",
      "args": ["/absolute/path/to/mcp-weather/command/server.py"]
    }
  }
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
1. The `get_karachi_weather` tool will be available automatically
2. Ask Claude: "What's the weather in Karachi?"
3. Or use slash command in Claude Code: `/mcp` to view available tools

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

Augment Code supports MCP servers and provides multiple methods to configure them. This command-based server uses stdio transport.

**Prerequisites**:
- Augment Code extension installed in VS Code
- Python dependencies installed: `pip3 install -r requirements.txt`

**Method 1: Settings Panel (Recommended)**

1. Open the Augment panel in VS Code
2. Click the **options menu** (hamburger icon) in the upper right
3. Select **Settings**
4. Scroll to the **MCP servers** section
5. Click **"+ Add MCP"** (for local servers)
6. Fill in the configuration:
   - **Name**: `weather`
   - **Command**: `python3`
   - **Args**: Add argument `/absolute/path/to/mcp-weather/command/server.py`
7. Click **Save**

**Method 2: JSON Import**

1. Open Augment Settings (gear icon)
2. Click **"Import from JSON"** in the MCP section
3. Paste this configuration:

```json
{
  "mcpServers": {
    "weather": {
      "command": "python3",
      "args": ["/absolute/path/to/mcp-weather/command/server.py"]
    }
  }
}
```

4. Click **Save**

**Note**: Replace `/absolute/path/to/mcp-weather/command/server.py` with the actual absolute path to the server.py file on your system.

**Method 3: Using Virtual Environment Path**

If using a virtual environment, specify the full Python path:

```json
{
  "mcpServers": {
    "weather": {
      "command": "/absolute/path/to/mcp-weather/command/venv/bin/python3",
      "args": ["/absolute/path/to/mcp-weather/command/server.py"]
    }
  }
}
```

**Usage with Augment Code**:

1. The `get_karachi_weather` tool will be available in Augment Agent
2. Ask questions like:
   - "What's the current weather in Karachi?"
   - "Check the weather conditions in Karachi"
   - "Tell me the temperature in Karachi"

**Verification**:

- Check the MCP servers list in Settings to confirm "weather" appears
- Look for the weather tool in Augment Agent's available tools
- Use the "..." menu next to the server name to view status or logs

**Troubleshooting**:

- Ensure all dependencies are installed: `pip3 install -r requirements.txt`
- Verify the absolute path to server.py is correct
- Check the Augment logs if the server fails to start
- Use the virtual environment Python path if you have dependency issues

### For VSCode GitHub Copilot

GitHub Copilot in VSCode supports MCP servers starting from **VS Code 1.102**. You can add this weather server to enhance Copilot with real-time weather data capabilities.

**Prerequisites**:
- VS Code 1.102 or later
- GitHub Copilot subscription
- MCP support enabled in your organization (if applicable)

**Method 1: Via Command Palette (Recommended)**

1. Open Command Palette (Ctrl/Cmd + Shift + P)
2. Run command: **"MCP: Add Server"**
3. Choose **"Workspace"** or **"Global"** scope
4. Fill in the configuration:
   - **Name**: `weather`
   - **Type**: `stdio`
   - **Command**: `python3`
   - **Args**: `/absolute/path/to/mcp-weather/command/server.py`

**Method 2: Manual Configuration**

Create or edit `.vscode/mcp.json` in your workspace:

```json
{
  "servers": {
    "weather": {
      "type": "stdio",
      "command": "python3",
      "args": ["/absolute/path/to/mcp-weather/command/server.py"]
    }
  }
}
```

**For global configuration**, use Command Palette: **"MCP: Open User Configuration"**

**Method 3: Using Virtual Environment Path**

If using a virtual environment, specify the full Python path:

```json
{
  "servers": {
    "weather": {
      "type": "stdio",
      "command": "/absolute/path/to/mcp-weather/command/venv/bin/python3",
      "args": ["/absolute/path/to/mcp-weather/command/server.py"]
    }
  }
}
```

**Usage with GitHub Copilot**:

1. Open GitHub Copilot Chat (Ctrl/Cmd + Alt + I)
2. Enable **Agent Mode** if available
3. The `get_karachi_weather` tool will be available in the tool picker
4. Ask questions like:
   - "What's the current weather in Karachi?"
   - "Check the weather conditions"
   - "Tell me the temperature in Karachi"

**Verification**:

1. Run Command Palette: **"MCP: List Servers"**
2. Verify "weather" appears in the list
3. Check status is "Running"
4. Open Copilot Chat and check the tool picker for `get_karachi_weather`

**Troubleshooting**:

- Run **"MCP: List Servers"** → Select "weather" → Click "Show Output" to view logs
- Use **"MCP: Reset Cached Tools"** to refresh tool discovery
- Restart VS Code after configuration changes
- If trust dialog appears, confirm you trust the server before proceeding

**Security Note**: VS Code will display a trust confirmation when adding the server. Only add MCP servers from trusted sources as they can execute code on your machine.

### For Other MCP Clients

Any MCP client that supports stdio transport can use this server. Configure it with:
- **Command**: `python3`
- **Args**: `["/absolute/path/to/mcp-weather/command/server.py"]`

The server provides one tool:

- `get_karachi_weather`: Fetches current weather for Karachi

## Example Response

When you ask "What's the weather in Karachi?", you'll get a formatted response like:

```
🌍 **Karachi, Pakistan**
📅 2025-01-20T10:30

🌡️ Temperature: 22.5°C (feels like 21.8°C)
☁️ Conditions: Partly cloudy
💧 Humidity: 65%
💨 Wind Speed: 15.2 km/h
🌧️ Precipitation: 0 mm
```

## API Used

This server uses the free [Open-Meteo API](https://open-meteo.com/) which requires no API key.

## Technical Details

- Built with FastMCP (Python MCP SDK)
- Uses stdio transport for communication (standard input/output)
- Async/await for efficient HTTP requests
- Single tool: `get_karachi_weather`

## Differences from HTTP Server

This command-based server uses **stdio transport** which means:
- The server runs as a subprocess of the MCP client
- Communication happens via standard input/output
- No HTTP endpoint or port needed
- Best for local development and single-client usage
- Automatically starts/stops with the client

For a server that runs as a standalone HTTP service, see the [HTTP implementation](../http/).

## Troubleshooting

### Virtual Environment Path Issues

If you're using a virtual environment, you may need to use the full path to the Python interpreter:

```json
{
  "mcpServers": {
    "weather": {
      "command": "/absolute/path/to/mcp-weather/command/venv/bin/python3",
      "args": ["/absolute/path/to/mcp-weather/command/server.py"]
    }
  }
}
```

### Permission Denied

If you get a permission denied error, make sure the server.py file is executable:

```bash
chmod +x server.py
```

Or specify the python3 command explicitly in your configuration.
