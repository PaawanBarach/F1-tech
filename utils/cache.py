import diskcache as dc
CACHE = dc.Cache("./.cache")

def get_cached_response(query: str):
    return CACHE.get(query)

def set_cached_response(query: str, resp):
    CACHE.set(query, resp, expire=None)
