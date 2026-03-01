from re import findall
from math import log

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

def idf (N : int, df : int) -> float :
    return log (((N - df + 0.5) / (df + 0.5)) + 1.0)

def bm25_term_score (tf : int, doc_len : int, avg_doc_len : float, N : int, 
                     df : int, k1 : float = 1.5, b : float = 0.75) -> float :
    if tf <= 0 or df <= 0 or N <= 0 or avg_doc_len <= 0 :
        return 0.0

    term_idf = idf (N, df)
    denom = tf + k1 * (1.0 - b + b * (doc_len / avg_doc_len))
    return term_idf * ((tf * (k1 + 1.0)) / denom)

def bm25_doc_score (query_terms : list [str], file : str, index : dict [str, dict], doc_lens : dict,
                    N : int, avg_doc_len : float, k1 : float = 1.5, b : float = 0.75) -> float :
    score = 0.0
    doc_len = doc_lens.get (file, 0)

    for term in query_terms :
        postings = index.get (term, {})
        tf = len (postings.get (file, []))
        df = len (postings)
        score += bm25_term_score (tf, doc_len, avg_doc_len, N, df, k1, b)
    return score