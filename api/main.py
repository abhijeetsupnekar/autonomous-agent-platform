import os

from fastapi import FastAPI
from pydantic import BaseModel

from graph.workflow import graph
from fastapi.middleware.cors import CORSMiddleware

print("FASTAPI WEATHER KEY EXISTS:", bool(os.getenv("WEATHER_API_KEY")))
app = FastAPI(
    title="Shopping MCP Agent API",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://shopping-agent-frontend.web.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    query: str


@app.get("/")
def root():

    return {"message": "Shopping MCP Agent API Running"}


@app.get("/health")
def health():

    return {"status": "healthy"}


@app.post("/chat")
def chat(request: ChatRequest):

    initial_state = {
        "user_query": request.query,
        "tool_calls": [],
        "tool_results": [],
        "final_response": None,
    }

    result = graph.invoke(initial_state)

    return {
        "query": request.query,
        "plan": result["tool_calls"],
        "tool_results": result["tool_results"],
        "response": result["final_response"],
    }
