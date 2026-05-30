from langgraph.graph import StateGraph, END

from graph.state import ShoppingState
import asyncio

from graph.nodes import (
    planner_node,
    execute_tool_calls,
    response_node,
)

builder = StateGraph(ShoppingState)

builder.add_node("planner", planner_node)

builder.add_node(
    "tool_executor",
    lambda state: asyncio.run(execute_tool_calls(state)),
)

builder.add_node(
    "response_generator",
    response_node,
)

builder.set_entry_point("planner")

builder.add_edge(
    "planner",
    "tool_executor",
)

builder.add_edge(
    "tool_executor",
    "response_generator",
)

builder.add_edge(
    "response_generator",
    END,
)

graph = builder.compile()
