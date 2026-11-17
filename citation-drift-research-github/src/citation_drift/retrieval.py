from rank_bm25 import BM25Okapi
import re

def tokenize(text):
    return re.findall(r"\w+", text.lower())

def bm25_top_k(claim, passages, top_k=5):
    if not passages:
        return []
    corpus = [tokenize(p) for p in passages]
    if not any(corpus):
        return []
    bm25 = BM25Okapi(corpus)
    scores = bm25.get_scores(tokenize(claim))
    order = sorted(range(len(passages)), key=lambda i: scores[i], reverse=True)
    return [
        {"passage_id": f"p{i}", "rank": rank + 1,
         "bm25_score": float(scores[i]), "text": passages[i]}
        for rank, i in enumerate(order[:top_k])
    ]
