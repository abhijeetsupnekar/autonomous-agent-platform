from ast import arguments

from mcp import ClientSession
from mcp.client.stdio import stdio_client
from mcp.client.stdio import StdioServerParameters

SERVER_PARAMS = StdioServerParameters(
    command="python",
    args=["-m", "servers.product_server"],
)

import os

COMMON_ENV = {
    **os.environ,
    "WEATHER_API_KEY": os.getenv("WEATHER_API_KEY", ""),
    "EXCHANGE_API_KEY": os.getenv("EXCHANGE_API_KEY", ""),
    "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY", ""),
}

print("MCP_CLIENT WEATHER:", os.getenv("WEATHER_API_KEY"))
print("COMMON_ENV WEATHER:", COMMON_ENV.get("WEATHER_API_KEY"))

SERVER_REGISTRY = {
    "product": StdioServerParameters(
        command="python",
        args=["-m", "servers.product_server"],
        env=COMMON_ENV,
    ),
    "weather": StdioServerParameters(
        command="python",
        args=["-m", "servers.weather_server"],
        env=COMMON_ENV,
    ),
    "exchange": StdioServerParameters(
        command="python",
        args=["-m", "servers.exchange_server"],
        env=COMMON_ENV,
    ),
}

print("COMMON_ENV WEATHER:", bool(COMMON_ENV.get("WEATHER_API_KEY")))


async def get_available_tools():

    all_tools = []

    for server_name, server_params in SERVER_REGISTRY.items():

        async with stdio_client(server_params) as (read, write):

            async with ClientSession(read, write) as session:

                await session.initialize()

                tools = await session.list_tools()

                for tool in tools.tools:

                    tool.server_name = server_name

                    all_tools.append(tool)

    return all_tools


async def execute_tool(tool_name: str, arguments: dict):

    tools = await get_available_tools()

    matching_tool = next((tool for tool in tools if tool.name == tool_name), None)

    if not matching_tool:
        return f"Tool {tool_name} not found"

    server_name = matching_tool.server_name

    server_params = SERVER_REGISTRY[server_name]

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()
            print("TOOL:", tool_name)
            print("ARGS:", arguments)
            result = await session.call_tool(tool_name, arguments)

            formatted_result = []

            for item in result.content:
                formatted_result.append(item.text)

            return "\n".join(formatted_result)
