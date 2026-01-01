#!/usr/bin/env python3
"""MCP Weather Server using FastMCP (Command/stdio transport)."""
import httpx
from fastmcp import FastMCP

# Capital city coordinates
ISLAMABAD_COORDS = {
    "lat": 33.6844,
    "lon": 73.0479
}

# Create FastMCP server
mcp = FastMCP("mcp-weather")


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


if __name__ == "__main__":
    # Run the server using stdio transport (for command-based execution)
    mcp.run(transport="stdio")
