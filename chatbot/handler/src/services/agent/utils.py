import logging
from typing import List, Tuple

from langchain_core.messages import BaseMessage, ToolMessage, AIMessage

logger = logging.getLogger(__name__)


def format_tool_message(tool_call: dict, tool_result: dict) -> str:
    if tool_call["name"] == "tavily_search":
        query = tool_result.get("query", "Unknown query")
        results = tool_result.get("results", [])
        images = tool_result.get("images", [])
        formatted_result = f"Search query: {query}\n\nSearch Results:\n"
        for i, result in enumerate(results, 1):
            formatted_result += (
                f"{i}. Title: {result.get('title', 'N/A')}\n"
                f"   URL: {result.get('url', 'N/A')}\n"
                f"   Content: {result.get('content', 'N/A')}\n"
                f"   Score: {result.get('score', 'N/A')}\n\n"
            )
        if images:
            formatted_result += "Images:\n"
            for i, image in enumerate(images, 1):
                formatted_result += f"{i}. Image URL: {image}\n"
    elif tool_call["name"] == "google_search":
        search_params = tool_result.get("searchParameters", {})
        query = search_params.get("q", "Unknown query")
        knowledge_graph = tool_result.get("knowledgeGraph", {})
        organic_results = tool_result.get("organic", [])
        people_also_ask = tool_result.get("peopleAlsoAsk", [])

        formatted_result = f"Search query: {query}\n\n"

        if knowledge_graph:
            formatted_result += "Knowledge Graph:\n"
            formatted_result += (
                f"  Title: {knowledge_graph.get('title', 'N/A')}\n"
                f"  Type: {knowledge_graph.get('type', 'N/A')}\n"
                f"  Description: {knowledge_graph.get('description', 'N/A')}\n"
                f"  Website: {knowledge_graph.get('website', 'N/A')}\n\n"
            )

        if organic_results:
            formatted_result += "Organic Results:\n"
            for i, result in enumerate(organic_results, 1):
                formatted_result += (
                    f"{i}. Title: {result.get('title', 'N/A')}\n"
                    f"   URL: {result.get('link', 'N/A')}\n"
                    f"   Snippet: {result.get('snippet', 'N/A')}\n\n"
                )

        if people_also_ask:
            formatted_result += "People Also Ask:\n"
            for i, item in enumerate(people_also_ask, 1):
                formatted_result += (
                    f"{i}. Question: {item.get('question', 'N/A')}\n"
                    f"   Answer: {item.get('snippet', 'N/A')}\n\n"
                )
    else:
        formatted_result = str(tool_result)

    return formatted_result


def format_response_message(
    filtered_messages: List[BaseMessage], include_tool_message: bool = False
) -> Tuple[str, List[str], List[str]]:
    """
    Formats a list of messages into a single string for display or logging.

    Args:
        filtered_messages (List[BaseMessage]): The list of messages to format.
        include_tool_message (bool): Whether to include tool messages in the response string.
                                    If False, tool messages are processed for resources but not included
                                    in the response. Defaults to True.

    Returns:
        tuple: A tuple containing:
            - str: The formatted string representation of the messages.
            - List[str]: A list of URLs extracted from search results.
    """
    response_parts = []
    search_resources = []
    images = []
    for message in filtered_messages:
        if isinstance(message, AIMessage):
            if len(message.tool_calls) > 0:
                for ai_message in message.content:
                    if isinstance(ai_message, dict):
                        ai_message_type = ai_message.get("type")
                        ai_message_name = ai_message.get("name")
                        if ai_message_type == "text":
                            text = ai_message.get("text")
                            response_parts.append(f"{text}\n")
                        elif (
                            ai_message_type == "tool_use"
                            and ai_message_name == "human_assistance"
                        ):
                            ai_message_input = ai_message.get("input")
                            query = ai_message_input.get("query")
                            response_parts.append(
                                f"### Human Assistance Query\n**Query:** {query}\n"
                            )
            else:
                response_parts.append(f"{message.content}\n")
        elif isinstance(message, ToolMessage):
            if message.name == "tavily_search":
                lines = message.content.split("\n")
                formatted_results = ""
                # Process each result block
                result_blocks = message.content.split("\n\n")
                logger.info(f"Result blocks: {result_blocks}")
                for block in result_blocks:
                    if block.strip():
                        result_lines = block.split("\n")
                        logger.info(f"Result lines: {result_lines}")
                        # Ensure the block has enough lines and contains a URL
                        if (
                            len(result_lines) >= 4
                            and "URL:" in result_lines[1]
                            and "Score:" in result_lines[3]
                            and "Content:" in result_lines[2]
                        ):
                            title = result_lines[0].split("Title: ", 1)[1].strip()
                            url = result_lines[1].split("URL: ", 1)[1].strip()
                            content = result_lines[2].split("Content: ", 1)[1].strip()
                            score = result_lines[3].split("Score: ", 1)[1].strip()
                            formatted_results += (
                                f"- **Title:** {title}\n"
                                f"  - **URL:** {url}\n"
                                f"  - **Content:** {content}\n"
                                f"  - **Score:** {score}\n"
                            )
                            if url and url.startswith("http"):
                                search_resources.append(url)
                        else:
                            for line in result_lines:
                                if "Image URL:" in line:
                                    image_url = line.split("Image URL: ", 1)[1].strip()
                                    if image_url and image_url.startswith("http"):
                                        images.append(image_url)

                if formatted_results and include_tool_message:
                    query = lines[0].replace("Search query: ", "").strip()
                    response_parts.append(
                        f"### Search Results\n**Query:** {query}\n\n{formatted_results}\n"
                    )
            elif message.name == "google_search":
                lines = message.content.split("\n")
                formatted_results = ""
                current_section = ""
                for line in lines[2:]:
                    if line in [
                        "Knowledge Graph:",
                        "Organic Results:",
                        "People Also Ask:",
                    ]:
                        current_section = line
                        formatted_results += f"**{line.strip(':')}**\n"
                    elif current_section == "Knowledge Graph:":
                        formatted_results += f"{line.strip()}\n"
                    elif current_section == "Organic Results:":
                        if line.startswith(tuple(f"{i}. " for i in range(1, 10))):
                            formatted_results += f"{line}\n"
                        elif line.startswith("   URL: "):
                            url = line.replace("   URL: ", "").strip()
                            if url and url.startswith("http"):
                                search_resources.append(url)
                            formatted_results += f"  {line}\n"
                        else:
                            formatted_results += f"  {line}\n"
                    elif current_section == "People Also Ask:":
                        formatted_results += f"{line}\n"
                if formatted_results and include_tool_message:
                    query = lines[0].replace("Search query: ", "").strip()
                    response_parts.append(
                        f"### Search Results\n**Query:** {query}\n\n{formatted_results}\n"
                    )
            elif include_tool_message:
                response_parts.append(
                    f"### Tool Result ({message.name})\n{message.content}\n"
                )

    # Combine all parts into a single response, separated by newlines
    final_response = "\n".join(response_parts)
    return final_response, search_resources, images
