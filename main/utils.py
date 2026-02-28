from re import findall

def tokenize (text : str) -> list [str] :
    text = text.lower ()
    return findall (r"\b[a-z]+\b", text)

def parse_query (query : str) -> tuple [list [str], list [str]] :
    phrase_parts = findall (r'"([^"]+)"', query)
    phrases = [" ".join (tokenize (p)) for p in phrase_parts if tokenize (p)]
    rest = findall (r'"[^"]+"|[^"]+', query)
    unquoted = " ".join (part for part in rest if not part.strip ().startswith ('"'))
    terms = tokenize (unquoted)
    return terms, phrases