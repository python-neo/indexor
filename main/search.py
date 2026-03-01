from .utils import parse_query, bm25_doc_score

def _matches_phrase (phrase_words : list [str], file : str, index : dict [str, dict]) -> bool :
    if not phrase_words :
        return True
    if any (w not in index or file not in index [w] for w in phrase_words) :
        return False

    starts = index [phrase_words [0]] [file]
    for p in starts :
        ok = True
        for i, w in enumerate (phrase_words [1:], start = 1) :
            if (p + i) not in index [w] [file] :
                ok = False
                break
        if ok :
            return True
    return False

def search (query : str, index : dict [str, dict], doc_lens : dict [str, int], 
            N : int, avg_doc_len : float) -> list [tuple [str, float]] :
    terms, phrases = parse_query (query)

    phrase_terms : list [str] = []
    phrase_word_lists : list [list [str]] = []
    for phrase in phrases :
        words = phrase.split ()
        if words :
            phrase_word_lists.append (words)
            phrase_terms.extend (words)

    query_terms = terms + phrase_terms
    if not query_terms :
        return []

    seen : set [str] = set ()
    query_terms = [t for t in query_terms if not (t in seen or seen.add (t))]

    candidates : set [str] = set ()
    for term in query_terms :
        postings = index.get (term, {})
        candidates |= set (postings.keys ())

    ranked : list [tuple [str, float]] = []

    for file in candidates :
        if phrase_word_lists and not any (_matches_phrase (words, file, index) for words in phrase_word_lists) :
            continue

        score = bm25_doc_score (query_terms, file, index, doc_lens, N, avg_doc_len)
        if score > 0 :
            ranked.append ((file, score))

    ranked.sort (key = lambda x : x [1], reverse = True)
    return ranked