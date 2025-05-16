import os
from typing import List

from langchain_tavily import TavilySearch
from langchain_core.tools import tool, Tool, BaseTool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langgraph.types import interrupt

from config.config import config


os.environ["SERPER_API_KEY"] = config.SERPER_API_KEY
os.environ["TAVILY_API_KEY"] = config.TAVILY_API_KEY

search_1 = GoogleSerperAPIWrapper()
search_2 = TavilySearch(max_results=5, topic="general")


@tool
def human_assistance(query: str) -> str:
    """Request assistance from a human."""
    human_response = interrupt({"query": query})
    return human_response["data"]


TOOLS: List[Tool | BaseTool] = [
    Tool(
        name="google_search",
        func=search_1.run,
        description="Fetches raw, detailed Google search results (URLs, titles, snippets) for broad web data analysis "
        "or research.",
    ),
    Tool(
        name="tavily_search",
        func=search_2.run,
        description="Provides curated, concise web results optimized for AI, ideal for quick, relevant answers or "
        "content generation.",
    ),
    human_assistance,
]
