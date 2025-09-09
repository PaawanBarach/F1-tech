# F1 Technical Analysis System

A comprehensive Formula 1 analytics platform combining real-time data, knowledge base, and AI analysis.

## Features

- Real-time OpenF1 API integration
- AI-powered question answering with HuggingFace models
- Knowledge base with automated ingestion (PDFs, articles, JSON data)
- Web UI and API endpoints
- Vector search with FAISS
- Conversation memory and caching

## Quick Start

### Prerequisites
- Python 3.10+
- [HuggingFace Token](https://huggingface.co/settings/tokens)
- Git

```bash
# Clone repository
git clone https://github.com/PaawanBarach/F1-tech.git
cd F1-tech

# Install dependencies
pip install -r requirements.txt

# Set environment variables
set HF_TOKEN=your_huggingface_token
```

### Running the System
```bash
# Start API server
uvicorn api_server:app --reload

# In another terminal, start UI
python main.py
```

Access the web interface at `http://localhost:7860` or API docs at `http://localhost:8000/docs`

## Data Ingestion
```bash
# Run full ingestion pipeline
python ingestion.py
```

## Configuration
Update `config.yml` for:
- RSS feed sources
- PDF directories
- API endpoints
- Model parameters
