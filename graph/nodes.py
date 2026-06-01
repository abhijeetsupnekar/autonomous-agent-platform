import os
import asyncio
import json
from dotenv import load_dotenv
from google import genai
from graph.state import ShoppingState
from shared.utils import normalize_category, normalize_product_name
from shared.mcp_client import execute_tool, get_available_tools

from shared.mcp_client import (
    execute_tool,
    get_available_tools,
)

load_dotenv()

import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY environment variable not set")

client = genai.Client(api_key=GEMINI_API_KEY)


def planner_node(state: ShoppingState):

    user_query = state["user_query"]

    tools = asyncio.run(get_available_tools())

    tool_descriptions = []

    for tool in tools:

        tool_descriptions.append(
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema,
            }
        )

    prompt = f"""
You are an AI planning agent.

Available tools:

{json.dumps(tool_descriptions, indent=2)}

Generate a JSON list of tool calls needed to answer the user's request.

Return ONLY valid JSON.

Example:

[
  {{
    "tool_name": "get_weather",
    "arguments": {{
      "city": "London"
    }}
  }},
  {{
    "tool_name": "convert_currency",
    "arguments": {{
      "from_currency": "USD",
      "to_currency": "GBP",
      "amount": 1000
    }}
  }}
]

User Query:
{user_query}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    raw_output = response.text.strip()

    raw_output = raw_output.replace("```json", "")
    raw_output = raw_output.replace("```", "")
    raw_output = raw_output.strip()

    tool_calls = json.loads(raw_output)

    state["tool_calls"] = tool_calls

    print("\nPLAN:")

    for tool_call in tool_calls:

        print(tool_call)

    return state


async def execute_tool_calls(state: ShoppingState):

    tool_results = []

    for tool_call in state["tool_calls"]:

        tool_name = tool_call["tool_name"]

        arguments = tool_call["arguments"]

        print(f"\nExecuting: {tool_name}")
        print(f"Arguments: {arguments}")

        result = await execute_tool(
            tool_name,
            arguments,
        )

        tool_results.append(
            {
                "tool_name": tool_name,
                "arguments": arguments,
                "result": result,
            }
        )

    state["tool_results"] = tool_results

    return state


def response_node(state: ShoppingState):

    prompt = f"""
You are a helpful AI assistant.

User Query:
{state['user_query']}

Tool Results:
{json.dumps(state['tool_results'], indent=2)}

Generate a clean and helpful response using all tool results.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    state["final_response"] = response.text

    return state
