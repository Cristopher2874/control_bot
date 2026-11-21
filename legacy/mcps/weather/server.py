import json
import logging
from typing import Any
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("weather-mcp-server")

# Initialize FastMCP server configured for HTTP transport on port 8000
mcp = FastMCP(
    name="weather",
    host="127.0.0.1",
    port=8000,
    streamable_http_path="/mcp",
)

# Mock weather database with realistic sample data
WEATHER_DATA: dict[str, dict[str, Any]] = {
    "new york": {
        "temperature": 18,
        "unit": "Celsius",
        "condition": "Partly Cloudy",
        "humidity": 65,
        "wind_speed_kmh": 14,
    },
    "london": {
        "temperature": 14,
        "unit": "Celsius",
        "condition": "Light Rain",
        "humidity": 82,
        "wind_speed_kmh": 20,
    },
    "tokyo": {
        "temperature": 22,
        "unit": "Celsius",
        "condition": "Clear",
        "humidity": 55,
        "wind_speed_kmh": 9,
    },
    "paris": {
        "temperature": 16,
        "unit": "Celsius",
        "condition": "Overcast",
        "humidity": 70,
        "wind_speed_kmh": 12,
    },
    "san francisco": {
        "temperature": 17,
        "unit": "Celsius",
        "condition": "Foggy",
        "humidity": 78,
        "wind_speed_kmh": 18,
    },
}


@mcp.tool()
def get_current_weather(city: str) -> str:
    """Get the current weather conditions for a specified city.

    Args:
        city: Name of the city (e.g. 'Tokyo', 'London', 'New York').
    """
    logger.info(f"Received request for current weather in: {city}")
    normalized_city = city.strip().lower()

    if normalized_city in WEATHER_DATA:
        data = WEATHER_DATA[normalized_city]
    else:
        # Fallback dynamic mock data for any unlisted city
        data = {
            "temperature": 20,
            "unit": "Celsius",
            "condition": "Sunny",
            "humidity": 60,
            "wind_speed_kmh": 10,
        }

    result = {
        "city": city.title(),
        **data,
    }
    return json.dumps(result, indent=2)


@mcp.tool()
def get_weather_forecast(city: str, days: int = 3) -> str:
    """Get the weather forecast for a specified city over the next few days.

    Args:
        city: Name of the city.
        days: Number of forecast days (1 to 5). Defaults to 3.
    """
    days = max(1, min(days, 5))
    logger.info(f"Received request for {days}-day forecast in: {city}")

    sample_conditions = ["Sunny", "Partly Cloudy", "Rain Showers", "Clear", "Overcast"]
    forecast = []
    base_temp = WEATHER_DATA.get(city.strip().lower(), {}).get("temperature", 20)

    for i in range(1, days + 1):
        forecast.append({
            "day": f"Day +{i}",
            "condition": sample_conditions[(i - 1) % len(sample_conditions)],
            "high_c": base_temp + (i % 3) - 1,
            "low_c": base_temp - 4 - (i % 2),
        })

    result = {
        "city": city.title(),
        "forecast_days": days,
        "forecast": forecast,
    }
    return json.dumps(result, indent=2)


if __name__ == "__main__":
    logger.info("Starting Weather MCP HTTP server on http://127.0.0.1:8000/mcp ...")
    mcp.run(transport="streamable-http")
