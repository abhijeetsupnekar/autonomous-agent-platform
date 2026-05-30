import asyncio

from shared.mcp_client import execute_tool

result = asyncio.run(execute_tool("get_weather", {"city": "Pune"}))

print(result)
