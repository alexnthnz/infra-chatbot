from fastapi.testclient import TestClient

from src.app.app import app

client = TestClient(app)

def test_invocations_success():
    # Sample prompt that should trigger a valid response
    payload = {"prompt": "What's the weather like today?"}
    
    response = client.post("/invocations", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    # Check that all expected keys are present in the response
    assert "analysis" in data
    assert "score" in data
    assert "label" in data
    assert "requires_internet" in data

def test_invocations_empty_prompt():
    # Test that an empty prompt returns a 400 error
    payload = {"prompt": ""}
    response = client.post("/invocations", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Prompt is empty"
