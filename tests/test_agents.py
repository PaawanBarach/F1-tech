import pytest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from agents_enhanced import answer_question
from unittest.mock import patch

def test_direct_openf1_answer():
    with patch('agents_enhanced._query_openf1') as mock_openf1:
        mock_openf1.return_value = {"answer": "Pirelli provides 5 compounds", "source": "openf1.io"}
        response = answer_question("What tire compounds are used in F1?")
        assert isinstance(response, str), "Response should be a string"
        assert "Pirelli" in response, "Expected tire manufacturer mention"
        assert "openf1.io" in response, "Missing OpenF1 source citation"

def test_fallback_to_knowledge_base():
    with patch('agents_enhanced._query_openf1') as mock_openf1:
        mock_openf1.return_value = None
        response = answer_question("Explain aerodynamic balance in F1 cars")
        assert "" not in response
        assert "aerodynamic" in response.lower()
