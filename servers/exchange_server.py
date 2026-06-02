import os
import httpx

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv(dotenv_path=".env")

mcp = FastMCP("ExchangeServer")

API_KEY = os.getenv("EXCHANGE_API_KEY")


@mcp.tool()
async def convert_currency(
    from_currency: str,
    to_currency: str,
    amount: float,
):
    """
    Convert an amount from one currency to another.
    """
    print("API KEY:", API_KEY)
    url = (
        f"https://v6.exchangerate-api.com/v6/"
        f"{API_KEY}/pair/"
        f"{from_currency.upper()}/"
        f"{to_currency.upper()}/"
        f"{amount}"
    )

    async with httpx.AsyncClient() as client:

        response = await client.get(url)

        data = response.json()

    if data.get("result") != "success":

        return {"error": "Currency conversion failed"}

    return {
        "from_currency": from_currency.upper(),
        "to_currency": to_currency.upper(),
        "amount": amount,
        "converted_amount": data["conversion_result"],
        "rate": data["conversion_rate"],
    }


if __name__ == "__main__":
    mcp.run()
