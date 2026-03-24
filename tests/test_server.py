from fastapi.testclient import TestClient
from server import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_vector_routing():
    response = client.post("/mcp/route", json={"query": "fetch database server logs"})
    assert response.status_code == 200
    data = response.json()
    assert data["target_node"] == "vector_mcp_node"
    assert data["confidence"] > 0.90
