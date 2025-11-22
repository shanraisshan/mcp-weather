# MCP Weather Server for Karachi (Streamable HTTP)

A Python-based Model Context Protocol (MCP) server that fetches current weather data for Karachi, Pakistan using the Open-Meteo API. Built with FastMCP 2.3+ using the modern Streamable HTTP transport.

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 server.py
```
The server will start on `http://localhost:8003`

## Usage in Your Project

### 🤖 Claude Code CLI

![](/!/mcp-http-claude-code.png)

**Method 1: Using CLI Command (Recommended)**

```bash
# Local scope (default - personal development)
claude mcp add weather http://localhost:8003/mcp

# Project scope (shared via .mcp.json in project root)
claude mcp add weather --scope project http://localhost:8003/mcp

# User scope (available across all projects)
claude mcp add weather --scope user http://localhost:8003/mcp
```

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

### 🤖 Augment Code

![](/!/mcp-http-augment.png)

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

### 🤖 VSCode GitHub Copilot

![](/!/mcp-http-copilot.png)

**Method 1: Via Command Palette (Recommended)**

1. Open Command Palette (Ctrl/Cmd + Shift + P)
2. Run command: **"MCP: Add Server"**
3. Choose **"Workspace"** or **"Global"** scope
4. Fill in the configuration:
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

### 🤖 Google Antigravity IDE

![](/!/mcp-http-antigravity.png)

   - Click on the **Agent** session in your workspace
   - Select the **"..."** (more options) dropdown at the top of the editor's side panel
   - Choose **"MCP Servers"** to open the MCP Store
   - Click **"Manage MCP Servers"** at the top of the MCP Store
   - Select **"View raw config"** in the main tab
   - This opens the `mcp_config.json` file for editing

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
