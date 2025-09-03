import os
import pytest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from fastapi.testclient import TestClient
from api_server import app

client = TestClient(app)

def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_knowledge_base_status():
    response = client.get("/knowledge-base/status")
    assert response.status_code == 200
    assert "vector_store" in response.json()

def test_ask_endpoint():
    test_question = {"question": "Explain F1 tire compounds"}
    response = client.post("/ask", 
        json=test_question,
        headers={"Authorization": f"Bearer {os.environ['HF_TOKEN']}"}
    )
    assert response.status_code == 200
    assert "answer" in response.json()
