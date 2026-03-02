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

def _uko (items : list) -> list [str] :
    seen : set = set ()
    return [x for x in items if not (x in seen or seen.add (x))]

def parse_query_with_requirements (query : str) -> tuple [list [str], list [str], list [str], list [str]] :
    tokens = findall (r'"[^"]+"|\+|[^\s"]+', query)
    clauses : list [str] = []
    plus_between : list [bool] = []

    for token in tokens :
        if token == "+" :
            pending_plus = True
            continue

        clauses.append (token)
        if len (clauses) > 1 :
            plus_between.append (pending_plus)
        pending_plus = False

    required_clause = [False] * len (clauses)
    for i, is_plus in enumerate (plus_between) :
        if is_plus :
            required_clause [i] = True
            required_clause [i + 1] = True

    terms, phrases, required_terms, required_phrases = [], [], [], []
    for i, clause in enumerate (clauses) :
        is_required = required_clause [i]
        is_quoted = clause.startswith ('"') and clause.endswith ('"') and len (clause) >= 2
        raw = clause [1:-1] if is_quoted else clause
        words = tokenize (raw)
        if not words :
            continue

        if is_quoted :
            phrase = " ".join (words)
            phrases.append (phrase)
            if is_required :
                required_phrases.append (phrase)
        else :
            terms.extend (words)
            if is_required :
                required_terms.extend (words)

    if clauses and not required_terms and not required_phrases :
        required_terms, required_phrases = terms.copy (), phrases.copy ()

    return (_uko (terms), _uko (phrases), _uko (required_terms), _uko (required_phrases),)

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