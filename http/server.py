#!/usr/bin/env python3
"""MCP Weather Server using FastMCP - 195 Countries."""
import httpx
import os
from fastmcp import FastMCP
from starlette.responses import HTMLResponse

# All 193 UN member countries with capital coordinates
COUNTRIES = {
    "afghanistan": {"capital": "Kabul", "lat": 34.5553, "lon": 69.2075},
    "albania": {"capital": "Tirana", "lat": 41.3275, "lon": 19.8187},
    "algeria": {"capital": "Algiers", "lat": 36.7538, "lon": 3.0588},
    "andorra": {"capital": "Andorra la Vella", "lat": 42.5063, "lon": 1.5218},
    "angola": {"capital": "Luanda", "lat": -8.8390, "lon": 13.2894},
    "antigua_and_barbuda": {"capital": "Saint John's", "lat": 17.1274, "lon": -61.8468},
    "argentina": {"capital": "Buenos Aires", "lat": -34.6037, "lon": -58.3816},
    "armenia": {"capital": "Yerevan", "lat": 40.1792, "lon": 44.4991},
    "australia": {"capital": "Canberra", "lat": -35.2809, "lon": 149.1300},
    "austria": {"capital": "Vienna", "lat": 48.2082, "lon": 16.3738},
    "azerbaijan": {"capital": "Baku", "lat": 40.4093, "lon": 49.8671},
    "bahamas": {"capital": "Nassau", "lat": 25.0480, "lon": -77.3554},
    "bahrain": {"capital": "Manama", "lat": 26.2285, "lon": 50.5860},
    "bangladesh": {"capital": "Dhaka", "lat": 23.8103, "lon": 90.4125},
    "barbados": {"capital": "Bridgetown", "lat": 13.1132, "lon": -59.5988},
    "belarus": {"capital": "Minsk", "lat": 53.9006, "lon": 27.5590},
    "belgium": {"capital": "Brussels", "lat": 50.8503, "lon": 4.3517},
    "belize": {"capital": "Belmopan", "lat": 17.2510, "lon": -88.7590},
    "benin": {"capital": "Porto-Novo", "lat": 6.4969, "lon": 2.6289},
    "bhutan": {"capital": "Thimphu", "lat": 27.4728, "lon": 89.6390},
    "bolivia": {"capital": "La Paz", "lat": -16.4897, "lon": -68.1193},
    "bosnia_and_herzegovina": {"capital": "Sarajevo", "lat": 43.8563, "lon": 18.4131},
    "botswana": {"capital": "Gaborone", "lat": -24.6282, "lon": 25.9231},
    "brazil": {"capital": "Brasilia", "lat": -15.8267, "lon": -47.9218},
    "brunei": {"capital": "Bandar Seri Begawan", "lat": 4.9031, "lon": 114.9398},
    "bulgaria": {"capital": "Sofia", "lat": 42.6977, "lon": 23.3219},
    "burkina_faso": {"capital": "Ouagadougou", "lat": 12.3714, "lon": -1.5197},
    "burundi": {"capital": "Gitega", "lat": -3.4264, "lon": 29.9246},
    "cabo_verde": {"capital": "Praia", "lat": 14.9331, "lon": -23.5133},
    "cambodia": {"capital": "Phnom Penh", "lat": 11.5564, "lon": 104.9282},
    "cameroon": {"capital": "Yaounde", "lat": 3.8480, "lon": 11.5021},
    "canada": {"capital": "Ottawa", "lat": 45.4215, "lon": -75.6972},
    "central_african_republic": {"capital": "Bangui", "lat": 4.3947, "lon": 18.5582},
    "chad": {"capital": "N'Djamena", "lat": 12.1348, "lon": 15.0557},
    "chile": {"capital": "Santiago", "lat": -33.4489, "lon": -70.6693},
    "china": {"capital": "Beijing", "lat": 39.9042, "lon": 116.4074},
    "colombia": {"capital": "Bogota", "lat": 4.7110, "lon": -74.0721},
    "comoros": {"capital": "Moroni", "lat": -11.7172, "lon": 43.2473},
    "congo_democratic_republic": {"capital": "Kinshasa", "lat": -4.4419, "lon": 15.2663},
    "congo_republic": {"capital": "Brazzaville", "lat": -4.2634, "lon": 15.2429},
    "costa_rica": {"capital": "San Jose", "lat": 9.9281, "lon": -84.0907},
    "cote_divoire": {"capital": "Yamoussoukro", "lat": 6.8276, "lon": -5.2893},
    "croatia": {"capital": "Zagreb", "lat": 45.8150, "lon": 15.9819},
    "cuba": {"capital": "Havana", "lat": 23.1136, "lon": -82.3666},
    "cyprus": {"capital": "Nicosia", "lat": 35.1856, "lon": 33.3823},
    "czechia": {"capital": "Prague", "lat": 50.0755, "lon": 14.4378},
    "denmark": {"capital": "Copenhagen", "lat": 55.6761, "lon": 12.5683},
    "djibouti": {"capital": "Djibouti", "lat": 11.5721, "lon": 43.1456},
    "dominica": {"capital": "Roseau", "lat": 15.3092, "lon": -61.3794},
    "dominican_republic": {"capital": "Santo Domingo", "lat": 18.4861, "lon": -69.9312},
    "ecuador": {"capital": "Quito", "lat": -0.1807, "lon": -78.4678},
    "egypt": {"capital": "Cairo", "lat": 30.0444, "lon": 31.2357},
    "el_salvador": {"capital": "San Salvador", "lat": 13.6929, "lon": -89.2182},
    "equatorial_guinea": {"capital": "Malabo", "lat": 3.7504, "lon": 8.7371},
    "eritrea": {"capital": "Asmara", "lat": 15.3229, "lon": 38.9251},
    "estonia": {"capital": "Tallinn", "lat": 59.4370, "lon": 24.7536},
    "eswatini": {"capital": "Mbabane", "lat": -26.3054, "lon": 31.1367},
    "ethiopia": {"capital": "Addis Ababa", "lat": 9.0320, "lon": 38.7469},
    "fiji": {"capital": "Suva", "lat": -18.1416, "lon": 178.4415},
    "finland": {"capital": "Helsinki", "lat": 60.1699, "lon": 24.9384},
    "france": {"capital": "Paris", "lat": 48.8566, "lon": 2.3522},
    "gabon": {"capital": "Libreville", "lat": 0.4162, "lon": 9.4673},
    "gambia": {"capital": "Banjul", "lat": 13.4549, "lon": -16.5790},
    "georgia": {"capital": "Tbilisi", "lat": 41.7151, "lon": 44.8271},
    "germany": {"capital": "Berlin", "lat": 52.5200, "lon": 13.4050},
    "ghana": {"capital": "Accra", "lat": 5.6037, "lon": -0.1870},
    "greece": {"capital": "Athens", "lat": 37.9838, "lon": 23.7275},
    "grenada": {"capital": "Saint George's", "lat": 12.0561, "lon": -61.7488},
    "guatemala": {"capital": "Guatemala City", "lat": 14.6349, "lon": -90.5069},
    "guinea": {"capital": "Conakry", "lat": 9.6412, "lon": -13.5784},
    "guinea_bissau": {"capital": "Bissau", "lat": 11.8816, "lon": -15.6178},
    "guyana": {"capital": "Georgetown", "lat": 6.8013, "lon": -58.1551},
    "haiti": {"capital": "Port-au-Prince", "lat": 18.5944, "lon": -72.3074},
    "honduras": {"capital": "Tegucigalpa", "lat": 14.0723, "lon": -87.1921},
    "hungary": {"capital": "Budapest", "lat": 47.4979, "lon": 19.0402},
    "iceland": {"capital": "Reykjavik", "lat": 64.1466, "lon": -21.9426},
    "india": {"capital": "New Delhi", "lat": 28.6139, "lon": 77.2090},
    "indonesia": {"capital": "Jakarta", "lat": -6.2088, "lon": 106.8456},
    "iran": {"capital": "Tehran", "lat": 35.6892, "lon": 51.3890},
    "iraq": {"capital": "Baghdad", "lat": 33.3152, "lon": 44.3661},
    "ireland": {"capital": "Dublin", "lat": 53.3498, "lon": -6.2603},
    "israel": {"capital": "Jerusalem", "lat": 31.7683, "lon": 35.2137},
    "italy": {"capital": "Rome", "lat": 41.9028, "lon": 12.4964},
    "jamaica": {"capital": "Kingston", "lat": 18.0179, "lon": -76.8099},
    "japan": {"capital": "Tokyo", "lat": 35.6762, "lon": 139.6503},
    "jordan": {"capital": "Amman", "lat": 31.9454, "lon": 35.9284},
    "kazakhstan": {"capital": "Astana", "lat": 51.1694, "lon": 71.4491},
    "kenya": {"capital": "Nairobi", "lat": -1.2921, "lon": 36.8219},
    "kiribati": {"capital": "Tarawa", "lat": 1.3382, "lon": 173.0176},
    "north_korea": {"capital": "Pyongyang", "lat": 39.0392, "lon": 125.7625},
    "south_korea": {"capital": "Seoul", "lat": 37.5665, "lon": 126.9780},
    "kuwait": {"capital": "Kuwait City", "lat": 29.3759, "lon": 47.9774},
    "kyrgyzstan": {"capital": "Bishkek", "lat": 42.8746, "lon": 74.5698},
    "laos": {"capital": "Vientiane", "lat": 17.9757, "lon": 102.6331},
    "latvia": {"capital": "Riga", "lat": 56.9496, "lon": 24.1052},
    "lebanon": {"capital": "Beirut", "lat": 33.8938, "lon": 35.5018},
    "lesotho": {"capital": "Maseru", "lat": -29.3167, "lon": 27.4833},
    "liberia": {"capital": "Monrovia", "lat": 6.2907, "lon": -10.7605},
    "libya": {"capital": "Tripoli", "lat": 32.8872, "lon": 13.1913},
    "liechtenstein": {"capital": "Vaduz", "lat": 47.1410, "lon": 9.5209},
    "lithuania": {"capital": "Vilnius", "lat": 54.6872, "lon": 25.2797},
    "luxembourg": {"capital": "Luxembourg", "lat": 49.6116, "lon": 6.1319},
    "madagascar": {"capital": "Antananarivo", "lat": -18.8792, "lon": 47.5079},
    "malawi": {"capital": "Lilongwe", "lat": -13.9626, "lon": 33.7741},
    "malaysia": {"capital": "Kuala Lumpur", "lat": 3.1390, "lon": 101.6869},
    "maldives": {"capital": "Male", "lat": 4.1755, "lon": 73.5093},
    "mali": {"capital": "Bamako", "lat": 12.6392, "lon": -8.0029},
    "malta": {"capital": "Valletta", "lat": 35.8989, "lon": 14.5146},
    "marshall_islands": {"capital": "Majuro", "lat": 7.1164, "lon": 171.1858},
    "mauritania": {"capital": "Nouakchott", "lat": 18.0735, "lon": -15.9582},
    "mauritius": {"capital": "Port Louis", "lat": -20.1609, "lon": 57.5012},
    "mexico": {"capital": "Mexico City", "lat": 19.4326, "lon": -99.1332},
    "micronesia": {"capital": "Palikir", "lat": 6.9248, "lon": 158.1610},
    "moldova": {"capital": "Chisinau", "lat": 47.0105, "lon": 28.8638},
    "monaco": {"capital": "Monaco", "lat": 43.7384, "lon": 7.4246},
    "mongolia": {"capital": "Ulaanbaatar", "lat": 47.8864, "lon": 106.9057},
    "montenegro": {"capital": "Podgorica", "lat": 42.4304, "lon": 19.2594},
    "morocco": {"capital": "Rabat", "lat": 34.0209, "lon": -6.8416},
    "mozambique": {"capital": "Maputo", "lat": -25.9692, "lon": 32.5732},
    "myanmar": {"capital": "Naypyidaw", "lat": 19.7633, "lon": 96.0785},
    "namibia": {"capital": "Windhoek", "lat": -22.5609, "lon": 17.0658},
    "nauru": {"capital": "Yaren", "lat": -0.5477, "lon": 166.9209},
    "nepal": {"capital": "Kathmandu", "lat": 27.7172, "lon": 85.3240},
    "netherlands": {"capital": "Amsterdam", "lat": 52.3676, "lon": 4.9041},
    "new_zealand": {"capital": "Wellington", "lat": -41.2865, "lon": 174.7762},
    "nicaragua": {"capital": "Managua", "lat": 12.1150, "lon": -86.2362},
    "niger": {"capital": "Niamey", "lat": 13.5137, "lon": 2.1098},
    "nigeria": {"capital": "Abuja", "lat": 9.0765, "lon": 7.3986},
    "north_macedonia": {"capital": "Skopje", "lat": 41.9981, "lon": 21.4254},
    "norway": {"capital": "Oslo", "lat": 59.9139, "lon": 10.7522},
    "oman": {"capital": "Muscat", "lat": 23.5880, "lon": 58.3829},
    "pakistan": {"capital": "Islamabad", "lat": 33.6844, "lon": 73.0479},
    "palau": {"capital": "Ngerulmud", "lat": 7.5006, "lon": 134.6242},
    "palestine": {"capital": "Ramallah", "lat": 31.9038, "lon": 35.2034},
    "panama": {"capital": "Panama City", "lat": 8.9824, "lon": -79.5199},
    "papua_new_guinea": {"capital": "Port Moresby", "lat": -9.4438, "lon": 147.1803},
    "paraguay": {"capital": "Asuncion", "lat": -25.2637, "lon": -57.5759},
    "peru": {"capital": "Lima", "lat": -12.0464, "lon": -77.0428},
    "philippines": {"capital": "Manila", "lat": 14.5995, "lon": 120.9842},
    "poland": {"capital": "Warsaw", "lat": 52.2297, "lon": 21.0122},
    "portugal": {"capital": "Lisbon", "lat": 38.7223, "lon": -9.1393},
    "qatar": {"capital": "Doha", "lat": 25.2854, "lon": 51.5310},
    "romania": {"capital": "Bucharest", "lat": 44.4268, "lon": 26.1025},
    "russia": {"capital": "Moscow", "lat": 55.7558, "lon": 37.6173},
    "rwanda": {"capital": "Kigali", "lat": -1.9403, "lon": 29.8739},
    "saint_kitts_and_nevis": {"capital": "Basseterre", "lat": 17.3026, "lon": -62.7177},
    "saint_lucia": {"capital": "Castries", "lat": 14.0101, "lon": -60.9875},
    "saint_vincent_and_grenadines": {"capital": "Kingstown", "lat": 13.1587, "lon": -61.2248},
    "samoa": {"capital": "Apia", "lat": -13.8506, "lon": -171.7513},
    "san_marino": {"capital": "San Marino", "lat": 43.9424, "lon": 12.4578},
    "sao_tome_and_principe": {"capital": "Sao Tome", "lat": 0.3302, "lon": 6.7333},
    "saudi_arabia": {"capital": "Riyadh", "lat": 24.7136, "lon": 46.6753},
    "senegal": {"capital": "Dakar", "lat": 14.7167, "lon": -17.4677},
    "serbia": {"capital": "Belgrade", "lat": 44.7866, "lon": 20.4489},
    "seychelles": {"capital": "Victoria", "lat": -4.6191, "lon": 55.4513},
    "sierra_leone": {"capital": "Freetown", "lat": 8.4657, "lon": -13.2317},
    "singapore": {"capital": "Singapore", "lat": 1.3521, "lon": 103.8198},
    "slovakia": {"capital": "Bratislava", "lat": 48.1486, "lon": 17.1077},
    "slovenia": {"capital": "Ljubljana", "lat": 46.0569, "lon": 14.5058},
    "solomon_islands": {"capital": "Honiara", "lat": -9.4456, "lon": 159.9729},
    "somalia": {"capital": "Mogadishu", "lat": 2.0469, "lon": 45.3182},
    "south_africa": {"capital": "Pretoria", "lat": -25.7479, "lon": 28.2293},
    "south_sudan": {"capital": "Juba", "lat": 4.8594, "lon": 31.5713},
    "spain": {"capital": "Madrid", "lat": 40.4168, "lon": -3.7038},
    "sri_lanka": {"capital": "Colombo", "lat": 6.9271, "lon": 79.8612},
    "sudan": {"capital": "Khartoum", "lat": 15.5007, "lon": 32.5599},
    "suriname": {"capital": "Paramaribo", "lat": 5.8520, "lon": -55.2038},
    "sweden": {"capital": "Stockholm", "lat": 59.3293, "lon": 18.0686},
    "switzerland": {"capital": "Bern", "lat": 46.9480, "lon": 7.4474},
    "syria": {"capital": "Damascus", "lat": 33.5138, "lon": 36.2765},
    "tajikistan": {"capital": "Dushanbe", "lat": 38.5598, "lon": 68.7740},
    "tanzania": {"capital": "Dodoma", "lat": -6.1630, "lon": 35.7516},
    "thailand": {"capital": "Bangkok", "lat": 13.7563, "lon": 100.5018},
    "timor_leste": {"capital": "Dili", "lat": -8.5569, "lon": 125.5603},
    "togo": {"capital": "Lome", "lat": 6.1256, "lon": 1.2254},
    "tonga": {"capital": "Nuku'alofa", "lat": -21.2114, "lon": -175.1998},
    "trinidad_and_tobago": {"capital": "Port of Spain", "lat": 10.6596, "lon": -61.5086},
    "tunisia": {"capital": "Tunis", "lat": 36.8065, "lon": 10.1815},
    "turkey": {"capital": "Ankara", "lat": 39.9334, "lon": 32.8597},
    "turkmenistan": {"capital": "Ashgabat", "lat": 37.9601, "lon": 58.3261},
    "tuvalu": {"capital": "Funafuti", "lat": -8.5211, "lon": 179.1962},
    "uganda": {"capital": "Kampala", "lat": 0.3476, "lon": 32.5825},
    "ukraine": {"capital": "Kyiv", "lat": 50.4501, "lon": 30.5234},
    "uae": {"capital": "Abu Dhabi", "lat": 24.4539, "lon": 54.3773},
    "united_kingdom": {"capital": "London", "lat": 51.5074, "lon": -0.1278},
    "united_states": {"capital": "Washington D.C.", "lat": 38.9072, "lon": -77.0369},
    "uruguay": {"capital": "Montevideo", "lat": -34.9011, "lon": -56.1645},
    "uzbekistan": {"capital": "Tashkent", "lat": 41.2995, "lon": 69.2401},
    "vanuatu": {"capital": "Port Vila", "lat": -17.7333, "lon": 168.3273},
    "vatican_city": {"capital": "Vatican City", "lat": 41.9029, "lon": 12.4534},
    "venezuela": {"capital": "Caracas", "lat": 10.4806, "lon": -66.9036},
    "vietnam": {"capital": "Hanoi", "lat": 21.0278, "lon": 105.8342},
    "yemen": {"capital": "Sanaa", "lat": 15.3694, "lon": 44.1910},
    "zambia": {"capital": "Lusaka", "lat": -15.3875, "lon": 28.3228},
    "zimbabwe": {"capital": "Harare", "lat": -17.8292, "lon": 31.0522},
}

# Create FastMCP server
mcp = FastMCP("weather-mcp-shayan-http")


# Add a custom route for the home page
@mcp.custom_route("/", ["GET"])
async def home(request):
    """Display MCP info, available tools, and setup instructions."""
    server_name = mcp.name + " (http)"

    # Generate tools list from COUNTRIES
    tools = [f"get_{country}_weather_shayan" for country in sorted(COUNTRIES.keys())]

    tools_html = ""
    for name in tools:
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
            .tools-container {{
                max-height: 400px;
                overflow-y: auto;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 8px;
                background: #fafafa;
            }}
            .tool {{
                background: white;
                border-radius: 4px;
                padding: 6px 10px;
                margin-bottom: 2px;
                box-shadow: 0 1px 2px rgba(0,0,0,0.05);
            }}
            .tool-name {{
                font-family: monospace;
                font-weight: 600;
                font-size: 0.75rem;
                color: #2563eb;
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
            .tool-count {{
                font-size: 0.85rem;
                color: #666;
                margin-bottom: 0.5rem;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{server_name}</h1>
            <div class="status">Running</div>

            <h2>Add to Your MCP Client</h2>
            <p>For Claude Code, Create .mcp.json at project root and add the following:</p>
            <pre><code>{{
  <span class="key">"mcpServers"</span>: {{
    <span class="key">"weather-mcp-shayan-http"</span>: {{
      <span class="key">"type"</span>: <span class="string">"http"</span>,
      <span class="key">"url"</span>: <span class="string">"https://mcp-weather-j5kl.onrender.com/mcp"</span>
    }}
  }}
}}</code></pre>

            <h2>Available Tools</h2>
            <div class="tool-count">{len(tools)} tools available</div>
            <div class="tools-container">
                {tools_html}
            </div>
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


def create_weather_tool(country_key: str, country_data: dict):
    """Factory function to create weather tools for each country."""
    capital = country_data["capital"]
    lat = country_data["lat"]
    lon = country_data["lon"]

    # Create display name from country key
    country_display = country_key.replace("_", " ").title()

    async def get_weather() -> str:
        try:
            temperature = await fetch_temperature(lat, lon)
            return f"{temperature}°C"
        except Exception as e:
            return f"Error fetching weather: {str(e)}"

    # Set function metadata
    get_weather.__name__ = f"get_{country_key}_weather_shayan"
    get_weather.__doc__ = f"""Get the current temperature for {country_display} ({capital}).

Returns temperature in degrees Celsius."""

    return get_weather


# Register all country weather tools
for country_key, country_data in COUNTRIES.items():
    tool_func = create_weather_tool(country_key, country_data)
    mcp.tool()(tool_func)


if __name__ == "__main__":
    # Run the server with Streamable HTTP transport
    # This is the recommended transport for MCP servers (FastMCP 2.3+)
    # Compatible with Google Antigravity, Claude Code, and other modern MCP clients
    # Use PORT from environment (Render) or default to 8003 for local development
    port = int(os.getenv("PORT", "8003"))
    mcp.run(transport="http", port=port, host="0.0.0.0")
