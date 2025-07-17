import os, datetime
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from vectorstore import STORE
from utils.cache import set_cached_response

load_dotenv()
HF_TOKEN = os.environ["HF_TOKEN"]

client = InferenceClient(provider="hf-inference", api_key=HF_TOKEN)

SYSTEM_ART = (
    "You are an expert F1 technical analyst. Write a detailed, data‑rich article "
    "covering these topics, embed any diagrams as markdown images, and cite sources."
)

def find_trending_topics(k=5):
    docs = STORE.similarity_search("F1 technical analysis", k=min(k,50))
    return [d.page_content for d in docs if d.page_content != "placeholder"]

def generate_technical_article():
    topics = find_trending_topics()
    bullet = "\n".join(f"- {t[:80]}…" for t in topics[:5])
    prompt = f"Write a technical analysis article covering:\n{bullet}\nFormat in Markdown."
    resp = client.chat.completions.create(
        model="HuggingFaceTB/SmolLM3-3B",
        messages=[{"role":"system","content":SYSTEM_ART},
                  {"role":"user","content":prompt}],
    )
    article = resp.choices[0].message.content
    key = f"article_{datetime.datetime.utcnow():%Y%m%d_%H%M%S}"
    os.makedirs("articles", exist_ok=True)
    path = f"articles/{key}.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(article)
    set_cached_response(key, (article, ["auto-generated"]))
    return key, article
