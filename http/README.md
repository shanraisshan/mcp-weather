# MCP Weather Server for 195 Countries (Streamable HTTP)

A Python-based Model Context Protocol (MCP) server that fetches current weather data for all 195 UN member countries using the Open-Meteo API. Built with FastMCP 2.3+ using the modern Streamable HTTP transport.

## Installation

### Local Development

```bash
cd http
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 server.py
```
The server will start on `http://localhost:8003`

### Deploy to Render.com (Free Tier - needs nayapay card)

1. **Fork or push this repository to GitHub**

2. **Create a new Web Service on Render:**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" and select "Web Service"
   - Connect your GitHub repository
   - Configure the service:
     - **Name**: `weather-mcp-shayan` (or your preferred name)
     - **Region**: Choose your preferred region
     - **Branch**: `main`
     - **Root Directory**: `http`
     - **Runtime**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python server.py`
   - Click "Create Web Service"

3. **Use your deployed server:**
   - Once deployed, Render will provide you with a URL like: `https://mcp-weather-j5kl.onrender.com`
   - Your MCP endpoint will be: `https://mcp-weather-j5kl.onrender.com/mcp`
   - Update your MCP client configuration with this URL instead of `http://localhost:8003/mcp`

**Note:** The free tier on Render may spin down after inactivity. The first request after inactivity may take 30-60 seconds to wake up the service.

### Keeping Your Server Alive with Cron-Job.org (shayanrais.gt)

To prevent your Render free tier server from spinning down after 15 minutes of inactivity, you can use a free cron service to ping it every 14 minutes:

1. **Go to [cron-job.org](https://cron-job.org/)** and create a free account

2. **Create a new cron job:**
   - Click "Create cronjob" in your dashboard
   - **Title**: `Keep MCP Weather Server Alive`
   - **URL**: `https://mcp-weather-j5kl.onrender.com/` (replace with your actual Render URL)
   - **Schedule**: Select "Every 14 minutes"
     - Or use custom expression: `*/14 * * * *`
   - **Request method**: GET
   - **Enabled**: Yes (check the box)

3. **Save the cron job** and it will start pinging your server automatically

Your server's home endpoint (`/`) is perfect for this purpose - it returns a simple HTML page confirming the server is running, which will keep the server active without consuming significant resources.

## Usage in Your Project

### 🤖 Claude Code CLI

![](/!/mcp-http-claude-code.png)

**Method 1: Using CLI Command (Recommended)**

```bash
# Local scope (default - personal development)
claude mcp add weather-mcp-shayan http://localhost:8003/mcp

# Project scope (shared via .mcp.json in project root)
claude mcp add weather-mcp-shayan --scope project http://localhost:8003/mcp

# User scope (available across all projects)
claude mcp add weather-mcp-shayan --scope user http://localhost:8003/mcp
```

**Method 2: Manual Configuration (Project Scope)**

Create `.mcp.json` in your project root:

```json
{
  "mcpServers": {
    "weather-mcp-shayan": {
      "type": "http",
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
claude mcp get weather-mcp-shayan

# Remove a server
claude mcp remove weather-mcp-shayan

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
    "weather-mcp-shayan": {
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
   - **Name**: `weather-mcp-shayan`
   - **Type**: `http` (Streamable HTTP)
   - **URL**: `http://localhost:8003/mcp`

**Method 2: Manual Configuration**

Create or edit `.vscode/mcp.json` in your workspace:

```json
{
  "servers": {
    "weather-mcp-shayan": {
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
       "weather-mcp-shayan": {
         "serverUrl": "http://localhost:8003/mcp",
         "description": "Weather data for 195 countries from Open-Meteo API"
       }
     }
   }
   ```
