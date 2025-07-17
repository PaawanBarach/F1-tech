# Drop-in new logic: e.g. ingest team press releases
import requests
from vectorstore import STORE, upsert_texts

def ingest_team_press(team: str):
    url = f"https://cms.example.com/{team}/news.json"
    data = requests.get(url, timeout=10).json()
    texts = [item["title"] + "\n" + item.get("body", "") for item in data]
    upsert_texts(texts, STORE)
