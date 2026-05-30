import asyncio

from shared.mcp_client import get_available_tools

tools = asyncio.run(get_available_tools())

print(tools)
