import asyncio

from shared.mcp_client import execute_tool

result = asyncio.run(
    execute_tool(
        "convert_currency",
        {
            "from_currency": "USD",
            "to_currency": "INR",
            "amount": 100,
        },
    )
)

print(result)
