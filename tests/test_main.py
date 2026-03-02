"""Tests for the main FastAPI application."""

from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient) -> None:
    """Test the root health check endpoint.

    Args:
        client: Test client fixture.
    """
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "running" in data["message"]


def test_hello_endpoint(client: TestClient) -> None:
    """Test the hello endpoint.

    Args:
        client: Test client fixture.
    """
    response = client.get("/api/v1/hello")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Agente de Atendimento" in data["message"]


def test_cors_headers(client: TestClient) -> None:
    """Test CORS middleware is configured.

    Args:
        client: Test client fixture.
    """
    response = client.get("/", headers={"Origin": "http://localhost:3000"})
    assert response.status_code == 200
    # CORS headers should be present
    assert "access-control-allow-origin" in response.headers


def test_404_on_nonexistent_route(client: TestClient) -> None:
    """Test 404 response for non-existent routes.

    Args:
        client: Test client fixture.
    """
    response = client.get("/nonexistent-route")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
