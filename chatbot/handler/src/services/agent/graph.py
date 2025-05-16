import logging
from typing import AsyncGenerator

from langchain_aws import ChatBedrockConverse
from langchain_core.messages import ToolMessage, HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_postgres import PostgresChatMessageHistory
from langgraph.graph import StateGraph, END

from config.config import config
from database import database

from .tools import TOOLS
from .state import InputState, State

logger = logging.getLogger(__name__)


class Graph:
    def __init__(self, session_id=None):
        llm = ChatBedrockConverse(
            model=config.AWS_BEDROCK_MODEL_ID,
            temperature=0,
            max_tokens=None,
            region_name=config.AWS_REGION_NAME,
        )

        self.conversation_history = PostgresChatMessageHistory(
            "chat_history",
            session_id,
            sync_connection=database.sync_connection,
        )
        self.model = llm.bind_tools(TOOLS)
        workflow = StateGraph(State, input=InputState)
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

    def __call_model(self, state: State, config: RunnableConfig):
        response = self.model.invoke(state["messages"], config)
        return {"messages": [response]}

    @staticmethod
    def __call_tools(state: State):
        outputs = []

        tools_by_name = {tool.name: tool for tool in TOOLS}
        for tool_call in state["messages"][-1].tool_calls:
            tool_result = tools_by_name[tool_call["name"]].invoke(tool_call["args"])
            if tool_call["name"] == "tavily_search":
                query = tool_result.get("query", "Unknown query")
                results = tool_result.get("results", [])

                formatted_result = f"Search query: {query}\n\nSearch Results:\n"
                for i, result in enumerate(results, 1):
                    formatted_result += (
                        f"{i}. Title: {result.get('title', 'N/A')}\n"
                        f"   URL: {result.get('url', 'N/A')}\n"
                        f"   Content: {result.get('content', 'N/A')}\n"
                        f"   Score: {result.get('score', 'N/A')}\n\n"
                    )
            else:
                formatted_result = str(tool_result)

            outputs.append(
                ToolMessage(
                    content=formatted_result,
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        return {"messages": outputs}

    @staticmethod
    def __should_continue(state: State):
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

        history_messages = self.conversation_history.get_messages()
        last_10_messages = (
            history_messages[-10:] if len(history_messages) > 10 else history_messages
        )

        logger.info(f"Last 10 messages: {last_10_messages}")

        system_message_content_1 = """
        You are a helpful assistant designed to provide accurate and relevant answers. Follow these guidelines:
        1. Answer the user's question to the best of your ability in a clear, concise, and conversational tone.
        2. If you don't know the answer, respond with "I don't know" and suggest how the user can find the information.
        3. If the question is unclear, ask the user to clarify or provide more details.
        4. Use the provided conversation history (the last 10 messages) to give contextually relevant answers. The history is included as separate messages before the user's question.
        5. You have access to tools to retrieve external information. Use them when the question requires up-to-date data, specific facts, or information beyond your knowledge. If unsure whether to use a tool, prioritize direct answers unless the question explicitly requires external data.
        6. If more context is needed to provide a better answer, ask the user for additional details.
        The user's question follows the history.
        """

        old_context_messages = [
            SystemMessage(content=system_message_content_1),
            *last_10_messages,
        ]

        try:
            # Invoke the graph with the question
            result = await self.graph.ainvoke(
                {
                    "messages": [*old_context_messages, HumanMessage(content=question)],
                }
            )

            # Filter out the messages that are in old_context_messages
            filtered_messages = [
                message
                for message in result["messages"]
                if message not in old_context_messages
            ]

            logger.info(f"Filtered messages: {filtered_messages}")

            self.conversation_history.add_messages(filtered_messages)
            for message in result["messages"]:
                logger.info(message)

            # Extract the last message from the state
            last_message = result["messages"][-1]

            # Handle different content types
            return last_message.content

        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return f"Error: Failed to process message: {str(e)}"
