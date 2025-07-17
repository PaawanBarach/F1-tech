import os
from vectorstore import STORE
from ingestion import run_full_ingest

def check_vectorstore_status():
    """Check if vectorstore has any data and show some basic info"""
    print("=== F1 Technical Analyst Knowledge Base Status ===")
    
    # Check if FAISS index exists
    index_path = "faiss_index"
    if os.path.exists(index_path):
        print(f"✓ FAISS index found at: {index_path}")
    else:
        print("✗ No FAISS index found")
    
    # Try to get some documents
    try:
        # Search for general F1 content
        docs = STORE.similarity_search("Formula 1 racing", k=5)
        print(f"✓ Found {len(docs)} documents in vectorstore")
        
        if docs:
            print("\n=== Sample Documents ===")
            for i, doc in enumerate(docs[:3]):
                content = doc.page_content[:200] if hasattr(doc, 'page_content') else str(doc)[:200]
                print(f"{i+1}. {content}...")
        else:
            print("No documents found - knowledge base is empty")
            
    except Exception as e:
        print(f"✗ Error accessing vectorstore: {e}")
    
    print("\n" + "="*50)

def run_manual_ingestion():
    """Run data ingestion manually"""
    print("=== Running Manual Data Ingestion ===")
    try:
        run_full_ingest()
        print("✓ Data ingestion completed successfully")
    except Exception as e:
        print(f"✗ Error during ingestion: {e}")
    print("="*50)

if __name__ == "__main__":
    check_vectorstore_status()
    
    # Ask if user wants to run ingestion
    response = input("\nWould you like to run manual data ingestion now? (y/n): ")
    if response.lower().startswith('y'):
        run_manual_ingestion()
        print("\nChecking knowledge base after ingestion...")
        check_vectorstore_status()
