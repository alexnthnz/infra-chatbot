from langchain.prompts.prompt import PromptTemplate
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.pydantic_v1 import BaseModel, Field, validator
from typing import Dict, Any
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_aws import ChatBedrockConverse

from src.config.settings import settings
from src.utils.logger import logger
from src.utils.utilities import is_question

# Create the search tool with API key
search_tool = GoogleSerperAPIWrapper(serper_api_key=settings.SERPER_API_KEY)


# Initialize the bedrock model
def get_bedrock_model():
    """
    Initialize and return an AWS Bedrock LLM for RAG.
    """
    try:
        # Initialize Bedrock client
        bedrock_llm = ChatBedrockConverse(
            model_id=settings.AWS_BEDROCK_MODEL_ID,
            region_name=settings.AWS_REGION_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID or None,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY or None,
            temperature=0.0,
        )
        return bedrock_llm
    except Exception as e:
        logger.error(f"Failed to initialize Bedrock model: {e}")
        # Fall back to OpenAI if Bedrock fails
        return get_llm()


# Initialize the RAG function
def rag_query(query: str) -> str:
    """
    Process a query through the RAG system.

    In a real implementation, this would retrieve relevant documents
    from a vector store and use them to generate a response.

    Args:
        query: The user's query

    Returns:
        The response from the RAG system
    """
    try:
        model = get_bedrock_model()
        # This is where you would normally add document retrieval and context injection
        # For now, we're demonstrating a simple version that just uses the LLM
        response = model.invoke(
            f"You are a helpful assistant answering based on your knowledge. "
            f"Respond concisely to this query: {query}"
        )

        # Parse the content from the response
        if hasattr(response, "content"):
            return response.content
        return str(response)
    except Exception as e:
        logger.error(f"Error in RAG query: {e}")
        return f"Error processing your query through RAG system: {str(e)}"


# Define the tools
tools = [
    Tool(
        name="search",
        description="Search the web for current or factual information. Use this for questions about current events, facts that might change over time, or recent information.",
        func=search_tool.run,
    ),
    Tool(
        name="rag",
        description="Query the knowledge base for domain-specific information. Use this for questions about internal data, company-specific knowledge, or specialized domain expertise.",
        func=rag_query,
    ),
]

# Get the react agent prompt
react_prompt = hub.pull("hwchase17/react")


# Define Pydantic models for parsers
class SentimentOutput(BaseModel):
    label: str = Field(description="The sentiment label (POSITIVE, NEGATIVE, or NEUTRAL)")
    score: float = Field(description="Confidence score between 0 and 1")

    @validator("score")
    def score_must_be_between_0_and_1(cls, v):
        if not 0 <= v <= 1:
            return 0.5
        return v


class CategoryOutput(BaseModel):
    category: str = Field(description="The category of the prompt")
    score: float = Field(description="Confidence score between 0 and 1")

    @validator("score")
    def score_must_be_between_0_and_1(cls, v):
        if not 0 <= v <= 1:
            return 0.5
        return v


class PromptDecisionOutput(BaseModel):
    enhanced_prompt: str = Field(description="The enhanced version of the user prompt")
    use_search: bool = Field(description="Whether to use search to answer this prompt")
    use_rag: bool = Field(description="Whether to use RAG to answer this prompt")
    reasoning: str = Field(description="Reasoning behind the decision")


def get_llm():
    """
    Initialize and return a LangChain LLM.
    """
    try:
        return ChatOpenAI(
            model_name=settings.openai_model,
            temperature=settings.openai_temperature,
            openai_api_key=settings.OPENAI_API_KEY,
        )
    except Exception as e:
        logger.error(f"Failed to initialize LLM: {e}")
        raise


# Create a single LLM instance to be used for tasks
llm = get_llm()


def categorize_prompt(prompt: str) -> dict:
    """
    Classify the prompt into a category using LangChain LLM.

    Args:
        prompt: The user's prompt.

    Returns:
        Dict with the category and confidence score.
    """
    try:
        parser = PydanticOutputParser(pydantic_object=CategoryOutput)

        template = """
        Classify the following prompt into one of these categories: {categories}
        
        Prompt: {prompt}
        
        Respond with a valid JSON in this format:
        {format_instructions}
        """

        prompt_template = PromptTemplate(
            template=template,
            input_variables=["prompt", "categories"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        input_text = prompt_template.format(
            prompt=prompt, categories=", ".join(settings.prompt_categories)
        )

        response = llm.invoke(input_text)
        result = parser.parse(response.content)

        return {"category": result.category, "score": result.score}
    except Exception as e:
        logger.error(f"Error categorizing prompt: {e}")
        return {"category": "Unknown", "score": 0.0}


def analyze_sentiment(prompt: str) -> dict:
    """
    Analyze the sentiment of the prompt using LangChain LLM.

    Args:
        prompt: The user's prompt.

    Returns:
        Dict with the sentiment label and score.
    """
    # For questions, we'll still use our rule-based approach
    if is_question(prompt):
        return {"label": "NEUTRAL", "score": 0.5}

    try:
        parser = PydanticOutputParser(pydantic_object=SentimentOutput)

        template = """
        Analyze the sentiment of the following prompt and classify it as POSITIVE, NEGATIVE, or NEUTRAL.
        
        Prompt: {prompt}
        
        Respond with a valid JSON in this format:
        {format_instructions}
        """

        prompt_template = PromptTemplate(
            template=template,
            input_variables=["prompt"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        input_text = prompt_template.format(prompt=prompt)
        response = llm.invoke(input_text)
        result = parser.parse(response.content)

        return {"label": result.label, "score": result.score}
    except Exception as e:
        logger.error(f"Error analyzing sentiment: {e}")
        return {"label": "NEUTRAL", "score": 0.5}


def check_internet_requirement(prompt: str) -> bool:
    """
    Determine if the prompt requires internet access using a LangChain agent.

    This implementation uses the ReAct pattern to determine if a search tool
    is needed to answer the prompt by attempting to use it.

    Args:
        prompt: The user's prompt.

    Returns:
        Boolean indicating if internet access is required.
    """
    try:
        # Create a specific prompt for the agent
        internet_check_prompt = f"Does answering '{prompt}' require looking up current information from the internet? Try to determine this using only your knowledge. If you can answer with your built-in knowledge, no internet is needed. If you need current events, search results, or real-time data, then internet is needed."

        # Get the LLM
        agent_llm = get_llm()

        # Create the agent with the react prompt and tools
        agent = create_react_agent(
            llm=agent_llm,
            tools=[tools[0]],  # Only use the search tool for this check
            prompt=react_prompt,
        )

        # Create an agent executor
        agent_executor = AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=[tools[0]],  # Only use the search tool for this check
            verbose=False,
            handle_parsing_errors=True,
            max_iterations=3,  # Limit the number of iterations to avoid excessive API calls
        )

        # Run the agent
        result = agent_executor.invoke({"input": internet_check_prompt})

        # Check if a search tool was used in the process
        tool_used = any(
            "Action: search" in str(step) for step in result.get("intermediate_steps", [])
        )

        # Check the final answer for internet requirement indications
        output = result.get("output", "").lower()

        # Determine internet requirement based on agent's behavior and answer
        requires_internet = (
            tool_used
            or "internet" in output
            and ("required" in output or "needed" in output or "yes" in output)
            or "search" in output
            and ("required" in output or "needed" in output or "yes" in output)
            or "current" in output
            and ("information" in output or "data" in output)
        )

        return requires_internet

    except Exception as e:
        logger.error(f"Error checking internet requirement with agent: {e}")

        # Fall back to the simpler method if agent fails
        try:
            template = """
            Determine if answering the following prompt would require internet access or recent information.
            
            Prompt: {prompt}
            
            Respond with only 'YES' if internet access is needed, or 'NO' if it is not needed.
            """

            prompt_template = PromptTemplate(template=template, input_variables=["prompt"])

            input_text = prompt_template.format(prompt=prompt)
            response = llm.invoke(input_text)

            # Get the content of the response
            result_text = response.content.strip().upper()

            # Return true if YES is found in the response
            return "YES" in result_text
        except Exception as inner_e:
            logger.error(f"Error in fallback internet requirement check: {inner_e}")
            return False


def analyze_and_enhance_prompt(prompt: str) -> Dict[str, Any]:
    """
    Analyze a user prompt, enhance it, and decide whether to use search or RAG.

    This function:
    1. Categorizes the prompt
    2. Analyzes sentiment
    3. Determines if internet is required
    4. Enhances the prompt for better results
    5. Decides whether to use search or RAG

    Args:
        prompt: The user's prompt.

    Returns:
        Dictionary containing the analysis results, enhanced prompt, and tool decision.
    """
    try:
        # Normalize the prompt
        normalized_prompt = prompt.strip()

        # Step 1: Categorize the prompt
        category_result = categorize_prompt(normalized_prompt)

        # Step 2: Analyze sentiment
        sentiment_result = analyze_sentiment(normalized_prompt)

        # Step 3: Check if internet is required
        requires_internet = check_internet_requirement(normalized_prompt)

        # Step 4: Enhance the prompt and decide on tools
        parser = PydanticOutputParser(pydantic_object=PromptDecisionOutput)

        template = """
        You are an AI assistant that analyzes user prompts and decides how to handle them.
        
        Here is a user prompt: "{prompt}"
        
        Your task is to:
        1. Enhance this prompt to make it clearer, more specific, and easier to answer correctly.
        2. Decide whether to use a search tool or a RAG (Retrieval Augmented Generation) system:
           - Use search when: The prompt requires current events, real-time data, specific internet facts, or external information not likely in internal documents.
           - Use RAG when: The prompt requires access to domain-specific knowledge, company information, or specialized context that might be in internal documents.
        
        Consider:
        - Prompt category: {category}
        - Requires internet access: {requires_internet}
        - Sentiment: {sentiment}
        
        For the enhanced prompt:
        - Make it clearer and more specific
        - Preserve the original intent
        - Format it as a well-structured question or request
        
        For the tool decision:
        - Both tools can't be true at the same time
        - If the information sought is likely to be in public internet sources and is time-sensitive, use search
        - If the information is likely to be in internal documents or specialized knowledge, use RAG
        
        Respond with a valid JSON in this format:
        {format_instructions}
        """

        prompt_template = PromptTemplate(
            template=template,
            input_variables=["prompt", "category", "requires_internet", "sentiment"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        input_text = prompt_template.format(
            prompt=normalized_prompt,
            category=category_result["category"],
            requires_internet=requires_internet,
            sentiment=sentiment_result["label"],
        )

        response = llm.invoke(input_text)
        decision_result = parser.parse(response.content)

        # Return the comprehensive analysis
        return {
            "original_prompt": normalized_prompt,
            "enhanced_prompt": decision_result.enhanced_prompt,
            "category": category_result,
            "sentiment": sentiment_result,
            "requires_internet": requires_internet,
            "use_search": decision_result.use_search,
            "use_rag": decision_result.use_rag,
            "reasoning": decision_result.reasoning,
        }

    except Exception as e:
        logger.error(f"Error analyzing and enhancing prompt: {e}")
        # Return a fallback response
        return {
            "original_prompt": prompt,
            "enhanced_prompt": prompt,  # No enhancement in case of error
            "category": (
                category_result
                if "category_result" in locals()
                else {"category": "Unknown", "score": 0.0}
            ),
            "sentiment": (
                sentiment_result
                if "sentiment_result" in locals()
                else {"label": "NEUTRAL", "score": 0.5}
            ),
            "requires_internet": requires_internet if "requires_internet" in locals() else False,
            "use_search": False,
            "use_rag": True,  # Default to RAG in case of error
            "reasoning": "Error occurred during analysis, defaulting to RAG",
            "error": str(e),
        }
