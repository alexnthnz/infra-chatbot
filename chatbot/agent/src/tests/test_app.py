from fastapi.testclient import TestClient
import pytest
from unittest.mock import patch, MagicMock

from src.app.app import app

client = TestClient(app)


# Mock the LangChain LLM and agent responses
@pytest.fixture(autouse=True)
def mock_langchain_responses():
    # Set up all the necessary mocks
    with (
        patch("src.app.inference.llm") as mock_llm,
        patch("src.app.inference.get_bedrock_model") as mock_bedrock,
        patch("src.app.inference.AgentExecutor.from_agent_and_tools") as mock_agent_executor,
    ):

        # Create a mock for the Bedrock LLM
        bedrock_mock = MagicMock()
        bedrock_mock.invoke.return_value = MagicMock(
            content="This is a response from the RAG system"
        )
        mock_bedrock.return_value = bedrock_mock

        # Create a mock for the prompt decision
        decision_mock = MagicMock()
        decision_mock.content = """
        {
            "enhanced_prompt": "What is the current weather forecast for New York City?",
            "use_search": true,
            "use_rag": false,
            "reasoning": "This question requires real-time information about weather that changes frequently."
        }
        """

        # Create mock for RAG decision
        rag_decision_mock = MagicMock()
        rag_decision_mock.content = """
        {
            "enhanced_prompt": "What are the company policies regarding remote work?",
            "use_search": false,
            "use_rag": true,
            "reasoning": "This question is about internal company policies which would be found in internal documents."
        }
        """

        # Create a mock response for sentiment analysis
        sentiment_mock = MagicMock()
        sentiment_mock.content = '{"label": "NEUTRAL", "score": 0.5}'

        # Create a mock response for category classification
        category_mock = MagicMock()
        category_mock.content = '{"category": "interrogative", "score": 0.9}'

        # Configure the LLM mock to return different responses based on input
        def llm_side_effect(input_text):
            if "sentiment" in input_text.lower():
                return sentiment_mock
            elif "categorize" in input_text.lower() or "classify" in input_text.lower():
                return category_mock
            elif "remote work" in input_text.lower() or "company policies" in input_text.lower():
                return rag_decision_mock
            elif "analyze" in input_text.lower() and "prompt" in input_text.lower():
                return decision_mock
            else:
                return MagicMock(content="YES")

        mock_llm.invoke.side_effect = llm_side_effect

        # Create a mock for the agent executor
        agent_mock = MagicMock()
        # Mock a successful agent run that indicates internet is required
        agent_mock.invoke.return_value = {
            "output": "Yes, this requires internet access to answer correctly.",
            "intermediate_steps": [("Action: search", "Some search results")],
        }

        # Return the mock agent executor instance
        mock_agent_executor.return_value = agent_mock

        yield mock_llm


def test_invocations_enhanced_analysis_search():
    """
    Test that the invocations endpoint returns enhanced prompt analysis with search decision.
    """
    # Sample prompt that should use search
    payload = {"prompt": "What's the weather in New York?"}

    response = client.post("/invocations", json=payload)
    assert response.status_code == 200

    data = response.json()

    # Check that all expected keys are present in the response
    assert "original_prompt" in data
    assert "enhanced_prompt" in data
    assert "sentiment" in data
    assert "requires_internet" in data
    assert "category" in data
    assert "use_search" in data
    assert "use_rag" in data
    assert "reasoning" in data

    # Check the enhanced prompt
    assert data["enhanced_prompt"] == "What is the current weather forecast for New York City?"

    # Check the tool decisions
    assert data["use_search"] is True
    assert data["use_rag"] is False

    # Verify other data
    assert "label" in data["sentiment"]
    assert "score" in data["sentiment"]
    assert "category" in data["category"]
    assert "score" in data["category"]


def test_invocations_enhanced_analysis_rag():
    """
    Test that the invocations endpoint returns enhanced prompt analysis with RAG decision.
    """
    # Sample prompt that should use RAG
    payload = {"prompt": "What are the company policies for remote work?"}

    response = client.post("/invocations", json=payload)
    assert response.status_code == 200

    data = response.json()

    # Check the enhanced prompt and tool decisions
    assert "enhanced_prompt" in data
    assert data["use_search"] is False
    assert data["use_rag"] is True


def test_invocations_empty_prompt():
    """
    Test that an empty prompt returns a 400 error with the correct error message.
    """
    payload = {"prompt": ""}
    response = client.post("/invocations", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Prompt is empty"


def test_invocations_category_classification():
    """
    Test that the prompt is correctly categorized for different types of prompts.
    """
    # Test an interrogative prompt
    payload = {"prompt": "What is the capital of France?"}
    response = client.post("/invocations", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["category"]["category"] == "interrogative"
    assert 0 <= data["category"]["score"] <= 1

    # Test an exclamatory prompt
    payload = {"prompt": "I love this app!"}
    response = client.post("/invocations", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["category"]["category"] == "interrogative"  # Using mock response
    assert 0 <= data["category"]["score"] <= 1

    # Test an imperative prompt
    payload = {"prompt": "Tell me a story."}
    response = client.post("/invocations", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["category"]["category"] == "interrogative"  # Using mock response
    assert 0 <= data["category"]["score"] <= 1
