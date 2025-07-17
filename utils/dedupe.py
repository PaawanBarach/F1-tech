from sentence_transformers import SentenceTransformer, util
_model = SentenceTransformer("all-MiniLM-L6-v2")

def is_duplicate(new_text: str, existing: list[str], threshold: float) -> bool:
    if not existing: return False
    emb1 = _model.encode(new_text, convert_to_tensor=True)
    embs = _model.encode(existing, convert_to_tensor=True)
    sims = util.cos_sim(emb1, embs)
    return bool(sims.max() >= threshold)
