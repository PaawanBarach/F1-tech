import os, glob, yaml, requests, feedparser, importlib
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
from utils.dedupe import is_duplicate
from vectorstore import upsert_texts

cfg = yaml.safe_load(open("config.yml", encoding="utf-8"))
_seen = []

def _clean_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "footer", "nav", "aside", "header", "form"]):
        tag.decompose()
    return soup.get_text(separator="\n").strip()

def ingest_rss() -> int:
    added = 0
    for url in cfg["rss_feeds"]:
        feed = feedparser.parse(url, agent="Mozilla/5.0")
        for entry in feed.entries[:5]:
            title = entry.title.strip()
            summary = _clean_html(getattr(entry, "summary", ""))
            try:
                body_html = requests.get(entry.link, timeout=5).text
                body = _clean_html(body_html)
            except:
                body = summary
            content = f"RSS Article: {title}\n\n{body}"
            if not is_duplicate(content, _seen, cfg["dedupe_threshold"]):
                _seen.append(content)
                upsert_texts([content])
                added += 1
    return added

def ingest_json() -> int:
    added = 0
    for url in cfg["json_feeds"]:
        data = requests.get(url, timeout=10).json()
        for post in data[:5]:
            title = post.get("title", "")
            raw = post.get("content", {}) if isinstance(post.get("content"), dict) else {"rendered": post.get("content", "")}
            content = _clean_html(raw.get("rendered", ""))
            full = f"JSON Article: {title}\n\n{content}"
            if title and content and not is_duplicate(full, _seen, cfg["dedupe_threshold"]):
                _seen.append(full)
                upsert_texts([full])
                added += 1
    return added

def ingest_openf1() -> int:
    base = cfg["apis"]["openf1_base"].rstrip("/")
    added = 0
    # Races
    races = requests.get(f"{base}/v1/races", timeout=10).json()
    for r in races[:5]:
        info = f"Race: {r['name']} on {r['date']} @ {r['circuitName']}"
        if not is_duplicate(info, _seen, cfg["dedupe_threshold"]):
            _seen.append(info)
            upsert_texts([info])
            added += 1
    # Laps longer than 60s
    laps = requests.get(f"{base}/v1/laps?lap_duration>=60", timeout=10).json()
    for lp in laps[:5]:
        info = f"Lap: session {lp['session_key']}, driver #{lp['driver_number']}, duration {lp['lap_duration']}s"
        if not is_duplicate(info, _seen, cfg["dedupe_threshold"]):
            _seen.append(info)
            upsert_texts([info])
            added += 1
    return added

def ingest_pdfs() -> int:
    added = 0
    for d in cfg["pdf_dirs"]:
        for fp in glob.glob(os.path.join(d, "*.pdf")):
            text = "\n".join(page.extract_text() or "" for page in PdfReader(fp).pages)
            if len(text) > 100 and not is_duplicate(text, _seen, cfg["dedupe_threshold"]):
                entry = f"PDF Document: {os.path.basename(fp)}\n\n{text}"
                _seen.append(text)
                upsert_texts([entry])
                added += 1
    return added

def ingest_images() -> int:
    added = 0
    try:
        import pytesseract, cv2
    except ImportError:
        return 0
    for d in cfg["image_dirs"]:
        for ext in ("*.jpg","*.png"):
            for p in glob.glob(os.path.join(d, ext)):
                txt = pytesseract.image_to_string(cv2.imread(p))
                txt = txt.strip()
                if len(txt) > 40 and not is_duplicate(txt, _seen, cfg["dedupe_threshold"]):
                    entry = f"Image OCR: {os.path.basename(p)}\n\n{txt}"
                    _seen.append(txt)
                    upsert_texts([entry])
                    added += 1
    return added

def ingest_plugins() -> int:
    added = 0
    for fn in glob.glob("plugins/*.py"):
        name = os.path.basename(fn)[:-3]
        mod = importlib.import_module(f"plugins.{name}")
        if hasattr(mod, "ingest"):
            for txt in mod.ingest():
                if not is_duplicate(txt, _seen, cfg["dedupe_threshold"]):
                    _seen.append(txt)
                    upsert_texts([txt])
                    added += 1
    return added

def run_full_ingest() -> int:
    return (
        ingest_rss()
      + ingest_json()
      + ingest_openf1()
      + ingest_pdfs()
      + ingest_images()
      + ingest_plugins()
    )
