# Formula 1 Technical Analysis System Context

## Project Overview
AI-powered system for Formula 1 technical analysis using RAG (Retrieval Augmented Generation). Integrates real-time data, knowledge base, and LLM analysis.

## Key Components

### Core Modules:
- `agents_enhanced.py`: Main question answering with OpenF1 API integration
- `api_server.py`: FastAPI endpoints for KB/search and Q&A
- `articles.py`: Technical article generation using HF models
- `enhanced_main.py`: Gradio UI + API integration

### Data Processing:
- `ingestion_fixed.py`: Data ingestion pipeline (RSS/JSON/PDF/Images)
- `vectorstore.py`: FAISS vector store management
- `utils/dedupe.py`: Text deduplication with sentence transformers
- `utils/plotting.py`: Dynamic visualization generation

### Infrastructure:
- Dockerized deployment (Dockerfile, docker-compose.yml)
- HuggingFace Inference integration (HF_TOKEN)
- Caching system (`utils/cache.py`)
- Plugin system (`plugins/` directory)

### Key Workflows:
1. User question → OpenF1 API check → KB search → LLM analysis
2. Automated content ingestion → Vector store updating
3. Technical article generation from trending topics
4. Real-time data visualization generation

## Critical Dependencies
- HuggingFace Inference Client
- FastAPI/Gradio for interfaces
- FAISS vector storage
- SentenceTransformers for embeddings
- OpenF1 API integration
