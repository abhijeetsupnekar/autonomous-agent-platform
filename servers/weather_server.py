import os
from urllib import response
import httpx

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv(dotenv_path=".env")

mcp = FastMCP("WeatherServer")


@mcp.tool()
async def get_weather(city: str):

    api_key = os.getenv("WEATHER_API_KEY")

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()

    if response.status_code != 200:
        return {"error": data.get("message", "Unknown error")}

    return {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temperature_c": data["main"]["temp"],
        "condition": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind_kph": round(data["wind"]["speed"] * 3.6, 2),
    }


if __name__ == "__main__":
    mcp.run()
