import logging
from typing import AsyncGenerator

from langchain_aws import ChatBedrockConverse
from langchain_core.messages import ToolMessage, HumanMessage, SystemMessage, AIMessage
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
        Invoke the graph to process a question and return all new messages in a structured format.

        Args:
            question (str): The user's question or message.

        Returns:
            str: A structured string containing all new messages generated during processing.
        """
        history_messages = self.conversation_history.get_messages()
        last_10_messages = (
            history_messages[-10:] if len(history_messages) > 10 else history_messages
        )

        system_message_content = """
        You are a helpful assistant designed to provide accurate and relevant answers. Follow these guidelines:
        1. Answer the user's question to the best of your ability in a clear, concise, and conversational tone.
        2. If you don't know the answer, respond with "I don't know" and suggest how the user can find the information.
        3. If the question is unclear, ask the user to clarify or provide more details.
        4. Use the provided conversation history (the last 10 messages) to give contextually relevant answers.
        5. You have access to tools to retrieve external information. Use them when the question requires up-to-date data, specific facts, or information beyond your knowledge.
        6. If more context is needed, ask the user for additional details.
        The user's question follows the history.
        """

        old_context_messages = [
            SystemMessage(content=system_message_content),
            *last_10_messages,
        ]

        last_message = last_10_messages[-1] if last_10_messages else None
        human_assistance_tool_call_id = None
        human_assistance_tool_args = None
        if (
            last_message
            and isinstance(last_message, AIMessage)
            and hasattr(last_message, "tool_calls")
            and last_message.tool_calls
        ):
            for tool_call in last_message.tool_calls:
                if tool_call["name"] == "human_assistance":
                    human_assistance_tool_call_id = tool_call["id"]
                    human_assistance_tool_args = tool_call["args"]
                    break

        # If there's a pending human_assistance tool call, process it
        if human_assistance_tool_call_id:
            # Validate query
            query = human_assistance_tool_args.get("query")
            if not query or not isinstance(query, str):
                raise ValueError("Invalid or missing query for human_assistance")

            # Append the tool result as a ToolMessage
            human_message = ToolMessage(
                content=question,
                name="human_assistance",
                tool_call_id=human_assistance_tool_call_id,
            )
        else:
            human_message = HumanMessage(content=question)

        try:
            # Invoke the graph with the question
            result = await self.graph.ainvoke(
                {
                    "messages": [*old_context_messages, human_message],
                }
            )

            # Filter out the messages that are in old_context_messages
            filtered_messages = [
                message
                for message in result["messages"]
                if message not in old_context_messages
            ]

            logger.info(f"Filtered messages: {filtered_messages}")

            # Store all new messages in the conversation history
            self.conversation_history.add_messages(filtered_messages)

            # Build the response by processing all filtered messages
            response_parts = []
            for message in filtered_messages:
                if isinstance(message, AIMessage):
                    if len(message.tool_calls) > 0:
                        for ai_message in message.content:
                            if isinstance(ai_message, dict):
                                ai_message_type = ai_message.get("type")
                                ai_message_name = ai_message.get("name")
                                if ai_message_type == "text":
                                    response_parts.append(ai_message.get("text"))
                                elif (
                                    ai_message_type == "tool_use"
                                    and ai_message_name == "human_assistance"
                                ):
                                    ai_message_input = ai_message.get("input")
                                    response_parts.append(ai_message_input.get("query"))
                    else:
                        response_parts.append(message.content)

            # Combine all parts into a single response, separated by newlines
            final_response = "\n".join(response_parts)

            logger.info(f"Final response: {final_response}")
            return final_response

        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return f"Error: Failed to process message: {str(e)}"
