from typing import TypedDict, Optional


class ShoppingState(TypedDict):

    user_query: str

    tool_calls: list

    tool_results: list

    final_response: Optional[str]
