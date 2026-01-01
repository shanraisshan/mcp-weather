#!/usr/bin/env python3
"""MCP Weather Server using FastMCP."""
import httpx
import os
from fastmcp import FastMCP
from starlette.responses import HTMLResponse

# Capital city coordinates
ISLAMABAD_COORDS = {
    "lat": 33.6844,
    "lon": 73.0479
}

ABU_DHABI_COORDS = {
    "lat": 24.4539,
    "lon": 54.3773
}

# Create FastMCP server
mcp = FastMCP("mcp-weather-shayan")


# Add a custom route for the home page
@mcp.custom_route("/", ["GET"])
async def home(request):
    """Display MCP info, available tools, and setup instructions."""
    server_name = mcp.name

    # Define available tools
    tools = [
        ("get_pakistan_weather_shayan", "Get the current temperature for Pakistan (Islamabad) in degrees Celsius."),
        ("get_uae_weather_shayan", "Get the current temperature for UAE (Abu Dhabi) in degrees Celsius."),
    ]

    tools_html = ""
    for name, desc in tools:
        tools_html += f"""
            <div class="tool">
                <div class="tool-name">{name}()</div>
            </div>
            """

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{server_name}</title>
        <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🌤️</text></svg>">
        <style>
            * {{
                box-sizing: border-box;
            }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background-color: #f5f5f5;
                margin: 0;
                padding: 40px 20px;
                color: #333;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
            }}
            h1 {{
                font-size: 2rem;
                margin-bottom: 0.5rem;
            }}
            .status {{
                color: #22c55e;
                font-size: 0.9rem;
                margin-bottom: 2rem;
            }}
            h2 {{
                font-size: 1.25rem;
                margin-top: 2rem;
                margin-bottom: 1rem;
                color: #555;
            }}
            .tool {{
                background: white;
                border-radius: 8px;
                padding: 16px;
                margin-bottom: 12px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }}
            .tool-name {{
                font-family: monospace;
                font-weight: 600;
                color: #2563eb;
            }}
            .tool-desc {{
                color: #666;
                margin-top: 4px;
                font-size: 0.9rem;
            }}
            pre {{
                background: #1e1e1e;
                color: #d4d4d4;
                padding: 16px;
                border-radius: 8px;
                overflow-x: auto;
                font-size: 0.85rem;
                line-height: 1.5;
            }}
            .key {{ color: #9cdcfe; }}
            .string {{ color: #ce9178; }}
            code {{
                font-family: 'SF Mono', Monaco, 'Courier New', monospace;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{server_name}</h1>
            <div class="status">Running</div>

            <h2>Available Tools</h2>
            {tools_html}

            <h2>Add to Your MCP Client</h2>
            <p>For Claude Code, Create .mcp.json at project root and add the following:</p>
            <pre><code>{{
  <span class="key">"mcpServers"</span>: {{
    <span class="key">"weather-mcp-karachi"</span>: {{
      <span class="key">"type"</span>: <span class="string">"http"</span>,
      <span class="key">"url"</span>: <span class="string">"https://mcp-weather-j5kl.onrender.com/mcp"</span>
    }}
  }}
}}</code></pre>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


async def fetch_temperature(lat: float, lon: float) -> float:
    """Fetch current temperature from Open-Meteo API."""
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}"
        f"&longitude={lon}"
        f"&current=temperature_2m"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()
        return data["current"]["temperature_2m"]


@mcp.tool()
async def get_pakistan_weather_shayan() -> str:
    """
    Get the current temperature for Pakistan (Islamabad).

    Returns temperature in degrees Celsius.
    """
    try:
        temperature = await fetch_temperature(
            ISLAMABAD_COORDS["lat"],
            ISLAMABAD_COORDS["lon"]
        )
        return f"{temperature}°C"

    except Exception as e:
        return f"Error fetching weather: {str(e)}"


@mcp.tool()
async def get_uae_weather_shayan() -> str:
    """
    Get the current temperature for UAE (Abu Dhabi).

    Returns temperature in degrees Celsius.
    """
    try:
        temperature = await fetch_temperature(
            ABU_DHABI_COORDS["lat"],
            ABU_DHABI_COORDS["lon"]
        )
        return f"{temperature}°C"

    except Exception as e:
        return f"Error fetching weather: {str(e)}"


if __name__ == "__main__":
    # Run the server with Streamable HTTP transport
    # This is the recommended transport for MCP servers (FastMCP 2.3+)
    # Compatible with Google Antigravity, Claude Code, and other modern MCP clients
    # Use PORT from environment (Render) or default to 8003 for local development
    port = int(os.getenv("PORT", "8003"))
    mcp.run(transport="http", port=port, host="0.0.0.0")
