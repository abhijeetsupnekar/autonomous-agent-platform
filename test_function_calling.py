import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

tools = [
    types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="search_products",
                description="Search products by category",
                parameters={
                    "type": "OBJECT",
                    "properties": {
                        "category": {
                            "type": "STRING",
                            "description": "Product category",
                        }
                    },
                    "required": ["category"],
                },
            )
        ]
    )
]

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Show me mobile products",
    config=types.GenerateContentConfig(tools=tools),
)

print(response)
