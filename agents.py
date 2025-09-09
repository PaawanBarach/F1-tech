import os, re
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from vectorstore import STORE, upsert_texts
from utils.cache import get_cached_response, set_cached_response
from utils.plotting import dynamic_plots
import requests

load_dotenv()
HF_TOKEN = os.environ["HF_TOKEN"]

# direct HuggingFace inference client
client = InferenceClient(provider="hf-inference", api_key=HF_TOKEN)

SYSTEM = (
    "You are an expert Formula 1 technical analyst.\n"
    "First, check the question against OpenF1 API for a direct factual answer. "
    "If found, return that succinctly with source link. "
    "Otherwise, retrieve from knowledge base and web as fallback, "
    "wrap internal reasoning in <think>…</think>, then give a 3–4 paragraph analysis, "
    "citing sources as [1], [2], … and embedding any chart as markdown image."
)

def _query_openf1(question: str):
    base = "https://api.openf1.org/v1"
    if "race" in question.lower():
        r = requests.get(f"{base}/races", timeout=5).json()
        return f"OpenF1 Races (latest):\n" + "\n".join(f"- {x['name']} on {x['date']}" for x in r[:3]), ["OpenF1 API"]
    if "lap" in question.lower():
        l = requests.get(f"{base}/laps?lap_duration>=60", timeout=5).json()
        return f"OpenF1 Laps (>60s):\n" + "\n".join(f"- session {x['session_key']}, dur {x['lap_duration']}s" for x in l[:3]), ["OpenF1 API"]
    return None, None

def answer_question(query: str):
    cached = get_cached_response(query)
    if cached:
        thinking, answer, sources = cached
        imgs = dynamic_plots("\n".join(sources))
        return thinking, answer, sources, imgs

    of1_ans, of1_src = _query_openf1(query)
    if of1_ans:
        upsert_texts([f"OpenF1: {query} -> {of1_ans}"])
        thinking = "<think>Used OpenF1 API for direct data.</think>"
        set_cached_response(query, (thinking, of1_ans, of1_src))
        return thinking, of1_ans, of1_src, []

    docs = STORE.similarity_search(query, k=5)
    sources = [d.page_content for d in docs if d.page_content != "placeholder"]
    context = "\n\n".join(sources) or "No relevant KB context."

    resp = client.chat.completions.create(
        model="HuggingFaceTB/SmolLM3-3B",
        messages=[
            {"role":"system","content":SYSTEM},
            {"role":"user","content":f"Context:\n{context}\n\nQuestion: {query}"}
        ],
    )
    content = resp.choices[0].message.content


    m = re.search(r"<think>(.*?)</think>", content, re.DOTALL)
    thinking = m.group(1).strip() if m else ""
    answer   = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()

    if all(len(s) < 20 for s in sources):
        upsert_texts([f"Learning note: {query}"])
    imgs = dynamic_plots(context)


    set_cached_response(query, (thinking, answer, sources))
    return thinking, answer, sources, imgs
