#!/usr/bin/env python3
"""MCP Weather Server for Karachi using FastMCP."""
import httpx
from typing import Any
from fastmcp import FastMCP

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

# Create FastMCP server
mcp = FastMCP("mcp-weather")


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


@mcp.tool()
async def get_karachi_weather() -> str:
    """
    Get the current weather conditions for Karachi, Pakistan.

    Returns temperature, humidity, wind speed, precipitation, and weather conditions.
    """
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

        # Format as readable text
        result = f"""
🌍 **{weather_info['location']}**
📅 {weather_info['timestamp']}

🌡️ Temperature: {weather_info['temperature']} (feels like {weather_info['feels_like']})
☁️ Conditions: {weather_info['conditions']}
💧 Humidity: {weather_info['humidity']}
💨 Wind Speed: {weather_info['wind_speed']}
🌧️ Precipitation: {weather_info['precipitation']}
"""
        return result.strip()

    except Exception as e:
        return f"Error fetching weather: {str(e)}"


if __name__ == "__main__":
    # Run the server on port 8003
    mcp.run(transport="sse", port=8003, host="0.0.0.0")
