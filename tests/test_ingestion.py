import pytest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from ingestion_fixed import run_full_ingest
from unittest.mock import patch

@patch('ingestion_fixed.ingest_rss')
@patch('ingestion_fixed.ingest_json')
@patch('ingestion_fixed.ingest_pdfs')
@patch('ingestion_fixed.ingest_images')
@patch('ingestion_fixed.ingest_openf1')
def test_full_ingestion(mock_pdfs, mock_json, mock_rss):
    mock_rss.return_value = 5
    mock_json.return_value = 3
    mock_pdfs.return_value = 2
    
    result = run_full_ingest()
    assert result == 10
    mock_rss.assert_called_once()
    mock_json.assert_called_once()
    mock_pdfs.assert_called_once()
