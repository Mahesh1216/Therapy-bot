import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.parametrize("persona", ["professional", "companion", "yap"])
def test_chat_endpoint_success(persona):
    """
    Tests if the /chat endpoint returns a successful response for each persona.
    """
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "Hello, I need some support.",
            "history": [],
            "persona": persona
        }
    )
    assert response.status_code == 200
    assert "response" in response.json()
    assert isinstance(response.json()["response"], str)


def test_chat_endpoint_long_history():
    """
    Tests the /chat endpoint with a long history (edge case).
    """
    history = [f"Message {i}" for i in range(50)]
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "Does the bot handle long history?",
            "history": history,
            "persona": "professional"
        }
    )
    assert response.status_code == 200
    assert "response" in response.json()


def test_chat_endpoint_invalid_persona():
    """
    Tests the /chat endpoint with an invalid persona (failure case).
    """
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "Test invalid persona",
            "history": [],
            "persona": "invalid_persona"
        }
    )
    assert response.status_code == 422 or response.status_code == 400


def test_chat_endpoint_empty_message():
    """
    Tests how the /chat endpoint handles an empty message.
    """
    response = client.post(
        "/api/v1/chat",
        json={"message": "", "history": [], "persona": "professional"}
    )
    assert response.status_code == 422  # Validation error


def test_chat_endpoint_no_message():
    """
    Tests how the /chat endpoint handles a request with no message field.
    """
    response = client.post(
        "/api/v1/chat",
        json={"history": [], "persona": "professional"}
    )
    assert response.status_code == 422  # Validation error