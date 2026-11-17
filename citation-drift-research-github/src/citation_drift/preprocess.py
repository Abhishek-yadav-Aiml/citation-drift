import re

def normalize_whitespace(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("text must be str")
    if not text.strip():
        raise ValueError("text cannot be empty")
    # Deliberately conservative: do not remove punctuation, negation, digits,
    # units, equations, citation markers, or scientific qualifiers.
    return re.sub(r"\s+", " ", text).strip()

def prepare_records(records):
    output = []
    for row in records:
        item = dict(row)
        item["claim_processed"] = normalize_whitespace(row["claim"])
        item["evidence_processed"] = normalize_whitespace(row["evidence"])
        output.append(item)
    return output
