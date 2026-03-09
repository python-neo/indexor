from re import findall
from math import log

def tokenize (text : str) -> list [str] :
    """
    Normalize text into lowercase alphabetic tokens.

    Parameters :
        text (str) : Raw text input.

    Returns :
        list [str] : Tokenized word list.
    """
    text = text.lower ()
    return findall (r"\b[a-z]+\b", text)

def parse_query (query : str) -> tuple [list [str], list [str]] :
    """
    Parse query into plain terms and quoted phrases.

    Parameters :
        query (str) : Raw query string.

    Returns :
        tuple [list [str], list [str]] :
            - Unquoted terms
            - Quoted phrases
    """
    phrase_parts = findall (r'"([^"]+)"', query)
    phrases = [" ".join (tokenize (p)) for p in phrase_parts if tokenize (p)]
    rest = findall (r'"[^"]+"|[^"]+', query)
    unquoted = " ".join (part for part in rest if not part.strip ().startswith ('"'))
    terms = tokenize (unquoted)
    return terms, phrases

def _uko (items : list) -> list [str] :
    """
    Return unique items while preserving input order.

    Parameters :
        items (list) : Input item list.

    Returns :
        list [str] : De-duplicated ordered list.
    """
    seen : set = set ()
    return [x for x in items if not (x in seen or seen.add (x))]

def parse_query_with_requirements (query : str) -> tuple [list [str], list [str], list [str], list [str]] :
    """
    Parse query into optional and required terms/phrases.

    Requirement rule :
        `left + right` marks both adjacent clauses as required.

    Parameters :
        query (str) : Raw query string.

    Returns :
        tuple [list [str], list [str], list [str], list [str]] :
            - Optional terms
            - Optional phrases
            - Required terms
            - Required phrases
    """
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
    """
    Compute BM25 inverse document frequency.

    Parameters :
        N (int) : Total number of documents.
        df (int) : Number of documents containing the term.

    Returns :
        float : IDF score.
    """
    return log (((N - df + 0.5) / (df + 0.5)) + 1.0)

def bm25_term_score (tf : int, doc_len : int, avg_doc_len : float, N : int, 
                     df : int, k1 : float = 1.5, b : float = 0.75) -> float :
    """
    Compute BM25 contribution for one term in one document.

    Parameters :
        tf (int) : Term frequency in the document.
        doc_len (int) : Document token count.
        avg_doc_len (float) : Average token count across all documents.
        N (int) : Total number of documents.
        df (int) : Number of documents containing the term.
        k1 (float) : BM25 term-frequency saturation parameter.
        b (float) : BM25 length-normalization parameter.

    Returns :
        float : BM25 term score.
    """
    if tf <= 0 or df <= 0 or N <= 0 or avg_doc_len <= 0 :
        return 0.0

    term_idf = idf (N, df)
    denom = tf + k1 * (1.0 - b + b * (doc_len / avg_doc_len))
    return term_idf * ((tf * (k1 + 1.0)) / denom)

def bm25_doc_score (query_terms : list [str], file : str, index : dict [str, dict], doc_lens : dict,
                    N : int, avg_doc_len : float, k1 : float = 1.5, b : float = 0.75) -> float :
    """
    Compute total BM25 score for a document against query terms.

    Parameters :
        query_terms (list [str]) : Query terms used for scoring.
        file (str) : File path to score.
        index (dict [str, dict]) : Inverted index postings.
        doc_lens (dict) : Token counts per document.
        N (int) : Total number of documents.
        avg_doc_len (float) : Average token count across all documents.
        k1 (float) : BM25 term-frequency saturation parameter.
        b (float) : BM25 length-normalization parameter.

    Returns :
        float : Total BM25 score for the given document.
    """
    score = 0.0
    doc_len = doc_lens.get (file, 0)

    for term in query_terms :
        postings = index.get (term, {})
        tf = len (postings.get (file, []))
        df = len (postings)
        score += bm25_term_score (tf, doc_len, avg_doc_len, N, df, k1, b)
    return score
