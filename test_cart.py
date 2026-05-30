import asyncio

from shared.mcp_client import execute_tool

print(
    asyncio.run(
        execute_tool(
            "add_to_cart",
            {"product_name": "iPhone"},
        )
    )
)

print(
    asyncio.run(
        execute_tool(
            "view_cart",
            {},
        )
    )
)

print(
    asyncio.run(
        execute_tool(
            "checkout",
            {},
        )
    )
)
