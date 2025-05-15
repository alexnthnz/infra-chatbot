import os
import logging
from typing import Annotated, Sequence, TypedDict, AsyncGenerator

from langchain_aws import ChatBedrockConverse
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.messages import ToolMessage, BaseMessage, HumanMessage
from langchain_core.tools import Tool
from langchain_core.runnables import RunnableConfig
from langchain_tavily import TavilySearch
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

from config.config import config

logger = logging.getLogger(__name__)

os.environ["SERPER_API_KEY"] = config.SERPER_API_KEY
os.environ["TAVILY_API_KEY"] = config.TAVILY_API_KEY


class AgentState(TypedDict):
    """The state of the agent."""

    messages: Annotated[Sequence[BaseMessage], add_messages]
    number_of_steps: int


class Agent:
    def __init__(self):
        """Initialize the Agent with a Bedrock LLM."""
        llm = ChatBedrockConverse(
            model=config.AWS_BEDROCK_MODEL_ID,
            temperature=0,
            max_tokens=None,
            region_name=config.AWS_REGION_NAME,
        )
        search_1 = GoogleSerperAPIWrapper()
        search_2 = TavilySearch(max_results=5, topic="general")

        self.tools = [
            Tool(
                name="google_search",
                func=search_1.run,
                description="Fetches raw, detailed Google search results (URLs, titles, snippets) for broad web data analysis or research.",
            ),
            Tool(
                name="tavily_search",
                func=search_2.run,
                description="Provides curated, concise web results optimized for AI, ideal for quick, relevant answers or content generation.",
            ),
        ]

        self.model = llm.bind_tools(self.tools)
        workflow = StateGraph(AgentState)
        workflow.add_node("llm", self.__call_model)
        workflow.add_node("tools", self.__call_tools)
        workflow.set_entry_point("llm")
        workflow.add_conditional_edges(
            "llm",
            self.__should_continue,
            {
                "continue": "tools",
                "end": END,
            },
        )
        workflow.add_edge("tools", "llm")
        self.graph = workflow.compile()

    def __call_tools(self, state: AgentState):
        outputs = []

        tools_by_name = {tool.name: tool for tool in self.tools}
        for tool_call in state["messages"][-1].tool_calls:
            tool_result = tools_by_name[tool_call["name"]].invoke(tool_call["args"])
            outputs.append(
                ToolMessage(
                    content=tool_result,
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        return {"messages": outputs}

    def __call_model(self, state: AgentState, config: RunnableConfig):
        response = self.model.invoke(state["messages"], config)
        return {"messages": [response]}

    def __should_continue(self, state: AgentState):
        messages = state["messages"]
        if not messages[-1].tool_calls:
            return "end"
        return "continue"

    async def stream_message(self, question: str) -> AsyncGenerator[str, None]:
        """
        Stream the agent's response for a given question using astream_events.

        Args:
            question (str): The user's question or message.

        Yields:
            str: Chunks of the response in Server-Sent Events (SSE) format.
        """
        try:
            async for message_chunk in self.graph.astream(
                {
                    "messages": [HumanMessage(content=question)],
                },
                stream_mode="messages",
            ):
                aimessage = message_chunk[0]
                content_list = aimessage.content
                if isinstance(content_list, str):
                    yield f"data: {content_list}\n\n"
                elif isinstance(content_list, list):
                    for content_item in content_list:
                        if isinstance(content_item, str):
                            yield f"data: {content_item}\n\n"
                        elif isinstance(content_item, dict):
                            text = content_item.get("text")
                            if text:
                                yield f"data: {text}\n\n"

        except Exception as e:
            logger.error(f"Error streaming message: {e}")
            yield f"data: Error: Failed to process message: {str(e)}\n\n"

    async def get_message(self, question: str) -> str:
        """
        Invoke the graph to process a question and return the final message content.

        Args:
            question (str): The user's question or message.

        Returns:
            str: The final message content from the graph's response.
        """
        try:
            # Invoke the graph with the question
            result = await self.graph.ainvoke(
                {
                    "messages": [HumanMessage(content=question)],
                }
            )
        
            for message in result["messages"]:
                log_details = f"Message (type={message.type}): {message.content}"
            
                # Add tool call information if present
                if hasattr(message, "tool_calls") and message.tool_calls:
                    log_details += f" | Tool Calls: {message.tool_calls}"
            
                # Add token usage if available (for AIMessage)
                if hasattr(message, "usage_metadata") and message.usage_metadata:
                    token_info = message.usage_metadata
                    log_details += f" | Tokens: input={token_info.get('input_tokens', 0)}, output={token_info.get('output_tokens', 0)}, total={token_info.get('total_tokens', 0)}"
            
                logger.info(log_details)

            # Extract the last message from the state
            last_message = result["messages"][-1]
        
            # Handle different content types
            if isinstance(last_message.content, str):
                return last_message.content
            elif isinstance(last_message.content, list):
                # Combine text content from list items
                content_parts = []
                for item in last_message.content:
                    if isinstance(item, str):
                        content_parts.append(item)
                    elif isinstance(item, dict):
                        text = item.get("text")
                        if text:
                            content_parts.append(text)
                return "".join(content_parts)
        
            return "No valid content found in response."
    
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return f"Error: Failed to process message: {str(e)}"
