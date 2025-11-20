#!/usr/bin/env python3
import asyncio
import httpx
import json
from typing import Any
from mcp.server import Server
from mcp.types import Tool, TextContent
import uvicorn
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse, StreamingResponse
from starlette.requests import Request

# Karachi coordinates
KARACHI_COORDS = {
    "lat": 24.8607,
    "lon": 67.0011
}

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail"
}


def interpret_weather_code(code: int) -> str:
    """Convert weather code to human-readable description."""
    return WEATHER_CODES.get(code, f"Unknown weather code: {code}")


async def fetch_weather() -> dict[str, Any]:
    """Fetch current weather data for Karachi from Open-Meteo API."""
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={KARACHI_COORDS['lat']}"
        f"&longitude={KARACHI_COORDS['lon']}"
        f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,"
        f"precipitation,weather_code,wind_speed_10m"
        f"&timezone=Asia/Karachi"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()


# Create MCP server
mcp_server = Server("mcp-weather")


@mcp_server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="get_karachi_weather",
            description="Get the current weather conditions for Karachi, Pakistan. "
                       "Returns temperature, humidity, wind speed, and weather conditions.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]


@mcp_server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    if name == "get_karachi_weather":
        try:
            weather_data = await fetch_weather()
            current = weather_data["current"]

            weather_info = {
                "location": "Karachi, Pakistan",
                "timestamp": current["time"],
                "temperature": f"{current['temperature_2m']}°C",
                "feels_like": f"{current['apparent_temperature']}°C",
                "humidity": f"{current['relative_humidity_2m']}%",
                "wind_speed": f"{current['wind_speed_10m']} km/h",
                "precipitation": f"{current['precipitation']} mm",
                "conditions": interpret_weather_code(current["weather_code"]),
                "weather_code": current["weather_code"]
            }

            return [TextContent(
                type="text",
                text=json.dumps(weather_info, indent=2)
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error fetching weather: {str(e)}"
            )]

    raise ValueError(f"Unknown tool: {name}")


async def handle_root(request: Request):
    """Handle root endpoint for health check."""
    return JSONResponse({
        "status": "running",
        "server": "mcp-weather",
        "version": "1.0.0",
        "endpoints": {
            "sse": "/sse",
            "health": "/"
        },
        "tools": ["get_karachi_weather"]
    })


# Import and create SSE transport after server is defined
from mcp.server.sse import SseServerTransport
from starlette.routing import Mount

sse_transport = SseServerTransport("/sse/messages")


async def handle_sse_connection(request: Request):
    """Handle SSE GET connection."""
    scope = request.scope
    receive = request.receive
    send = request._send

    # SSE connection
    async with sse_transport.connect_sse(scope, receive, send) as (read_stream, write_stream):
        await mcp_server.run(
            read_stream,
            write_stream,
            mcp_server.create_initialization_options()
        )


async def handle_sse_messages(request: Request):
    """Handle POST messages to SSE endpoint."""
    scope = request.scope
    receive = request.receive
    send = request._send

    await sse_transport.handle_post_message(scope, receive, send)


# Create Starlette app
app = Starlette(
    routes=[
        Route("/", endpoint=handle_root),
        Route("/sse", endpoint=handle_sse_connection, methods=["GET"]),
        Route("/sse/messages", endpoint=handle_sse_messages, methods=["POST"]),
    ]
)


if __name__ == "__main__":
    print("Starting Karachi Weather MCP HTTP Server on http://localhost:8003")
    print("SSE endpoint: http://localhost:8003/sse")
    uvicorn.run(app, host="0.0.0.0", port=8003)
