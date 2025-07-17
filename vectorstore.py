import os
from sentence_transformers import SentenceTransformer
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

MODEL_NAME = "all-MiniLM-L6-v2"
_MODEL     = SentenceTransformer(MODEL_NAME)
EMBED      = HuggingFaceEmbeddings(model_name=MODEL_NAME)
INDEX_DIR  = os.path.join(os.getcwd(), "faiss_index")

def init_vectorstore():
    if os.path.exists(INDEX_DIR) and os.path.exists(f"{INDEX_DIR}.pkl"):
        return FAISS.load_local(INDEX_DIR, EMBED, allow_dangerous_deserialization=True)
    # start with a dummy placeholder so we never hit empty
    return FAISS.from_texts(["placeholder"], EMBED, metadatas=[{"placeholder": True}])

STORE = init_vectorstore()

def upsert_texts(texts: list[str], store=None):
    store = store or STORE
    embeddings = _MODEL.encode(texts).tolist()
    store.add_texts(texts=texts, embeddings=embeddings)
    store.save_local(INDEX_DIR)
