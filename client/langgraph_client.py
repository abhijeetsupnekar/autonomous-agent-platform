from graph.workflow import graph

initial_state = {
    "user_query": "Show me mobile phones, add iPhone to cart and checkout",
    "tool_calls": [],
    "tool_results": [],
    "final_response": None,
}

result = graph.invoke(initial_state)

print("\nFINAL STATE:\n")

print("\nFINAL RESPONSE:\n")

print(result["final_response"])
