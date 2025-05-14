import os
import logging
from typing import Annotated, Sequence, TypedDict, AsyncGenerator

from langchain_aws import ChatBedrockConverse
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.messages import ToolMessage, BaseMessage, HumanMessage
from langchain_core.tools import Tool
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

from config.config import config

logger = logging.getLogger(__name__)

os.environ["SERPER_API_KEY"] = config.SERPER_API_KEY


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
        search = GoogleSerperAPIWrapper()

        self.tools = [
            Tool(
                name="Search",
                func=search.run,
                description="Useful for when you need to ask with a search engine.",
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
