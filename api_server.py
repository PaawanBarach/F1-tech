from fastapi import FastAPI
from vectorstore import STORE
from agents import answer_question
import os

app = FastAPI()

@app.get("/")
def root():
    return {"message": "F1 Technical Analyst API", "status": "running"}

@app.get("/ping")
def ping():
    return {"status": "alive"}

@app.get("/knowledge-base/status")
def get_knowledge_base_status():
    """Check the status of the knowledge base"""
    try:
        # Check if FAISS index exists
        index_exists = os.path.exists("faiss_index")
        
        # Get sample documents
        docs = STORE.similarity_search("Formula 1", k=5)
        doc_count = len(docs)
        
        sample_docs = []
        for doc in docs[:3]:
            content = doc.page_content[:100] if hasattr(doc, 'page_content') else str(doc)[:100]
            sample_docs.append(content)
        
        return {
            "index_exists": index_exists,
            "document_count": doc_count,
            "sample_documents": sample_docs
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/knowledge-base/search")
def search_knowledge_base(query: str, k: int = 5):
    """Search the knowledge base"""
    try:
        docs = STORE.similarity_search(query, k=k)
        results = []
        for doc in docs:
            content = doc.page_content if hasattr(doc, 'page_content') else str(doc)
            results.append({
                "content": content[:500],  # Limit to 500 chars
                "metadata": getattr(doc, 'metadata', {})
            })
        return {"query": query, "results": results}
    except Exception as e:
        return {"error": str(e)}

@app.post("/ask")
def ask_question(question: dict):
    """Ask a question to the F1 analyst"""
    try:
        query = question.get("query", "")
        if not query:
            return {"error": "No query provided"}
        
        answer, sources = answer_question(query)
        return {
            "query": query,
            "answer": answer,
            "sources": sources
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    print("Starting F1 Technical Analyst API on http://127.0.0.1:8000")
    print("Available endpoints:")
    print("  - GET  /                           : API info")
    print("  - GET  /knowledge-base/status      : Check knowledge base")
    print("  - GET  /knowledge-base/search?query=<query> : Search knowledge base")
    print("  - POST /ask                        : Ask a question")
    uvicorn.run(app, host="127.0.0.1", port=8000)
