from fastapi.testclient import TestClient

from src.app.app import app

client = TestClient(app)

def test_invocations_success():
    """
    Test that a valid prompt returns a successful response with the expected structure.
    """
    # Sample prompt that should trigger a valid response
    payload = {"prompt": "What's the weather like today?"}
    
    response = client.post("/invocations", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    # Check that all expected keys are present in the response
    assert "processed_prompt" in data  # Updated from "analysis"
    assert "sentiment" in data
    assert "requires_internet" in data
    assert "category" in data

    # Check the nested structure of sentiment
    assert "label" in data["sentiment"]
    assert "score" in data["sentiment"]
    assert data["sentiment"]["label"] == "NEUTRAL"  # Since it's a question
    assert data["sentiment"]["score"] == 0.5

    # Check the nested structure of category
    assert "category" in data["category"]
    assert "score" in data["category"]
    assert data["category"]["category"] in ["declarative", "interrogative", "imperative", "exclamatory", "conversational"]
    assert 0 <= data["category"]["score"] <= 1

    # Check requires_internet is a boolean
    assert isinstance(data["requires_internet"], bool)

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
    assert data["category"]["category"] == "exclamatory"
    assert 0 <= data["category"]["score"] <= 1

    # Test an imperative prompt
    payload = {"prompt": "Tell me a story."}
    response = client.post("/invocations", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["category"]["category"] == "imperative"
    assert 0 <= data["category"]["score"] <= 1
