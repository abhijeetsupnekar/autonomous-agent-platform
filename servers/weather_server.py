import os
from urllib import response
import httpx

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv(dotenv_path=".env")

mcp = FastMCP("WeatherServer")

API_KEY = os.getenv("WEATHER_API_KEY")

print("API KEY:", API_KEY)


@mcp.tool()
async def get_weather(city: str):
    """
    Get current weather information for a city.
    """

    url = "http://api.weatherapi.com/v1/current.json"

    params = {
        "key": API_KEY,
        "q": city,
    }

    async with httpx.AsyncClient() as client:

        response = await client.get(url, params=params)

        print(response.text)
        data = response.json()

    if "error" in data:
        return {"error": data["error"]["message"]}

    current = data["current"]
    location = data["location"]

    return {
        "city": location["name"],
        "country": location["country"],
        "temperature_c": current["temp_c"],
        "condition": current["condition"]["text"],
        "humidity": current["humidity"],
        "wind_kph": current["wind_kph"],
    }


if __name__ == "__main__":
    mcp.run()
