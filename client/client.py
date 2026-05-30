import os
import json
import asyncio
from dotenv import load_dotenv
from google import genai
from mcp import ClientSession
from mcp.client.stdio import stdio_client
from mcp.client.stdio import StdioServerParameters

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


async def main():

    user_query = "Find Delllaptops"

    prompt = f"""
You are an AI shopping agent.

Available tools:

1. search_products(category)
   → searches products by category

2. get_product_by_name(name)
   → searches products by product name

3. list_categories()
   → lists all categories

4. add_to_cart(product_name)
   → adds product to shopping cart

5. view_cart()
   → displays cart items

Based on the user query,
decide:

- tool_name
- arguments

Return ONLY valid JSON.

Example:

{{
  "tool_name": "search_products",
  "arguments": {{
    "category": "mobile"
  }}
}}

User Query:
{user_query}
"""

    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)

    raw_output = response.text.strip()

    raw_output = raw_output.replace("```json", "")
    raw_output = raw_output.replace("```", "")
    raw_output = raw_output.strip()

    print("\nLLM Decision:\n")
    print(raw_output)

    tool_decision = json.loads(raw_output)

    tool_name = tool_decision["tool_name"]

    arguments = tool_decision["arguments"]
    from shared.utils import normalize_category, normalize_product_name

    if "category" in arguments:
        arguments["category"] = normalize_category(arguments["category"])

    if "name" in arguments:
        arguments["name"] = normalize_product_name(arguments["name"])

    server_params = StdioServerParameters(
        command="python", args=["-m", "servers.product_server"]
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            result = await session.call_tool(tool_name, arguments)

            print("\nTool Execution Result:\n")

            for item in result.content:
                print(item.text)


asyncio.run(main())
