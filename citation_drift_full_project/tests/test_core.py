import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from citation_drift.data import load_jsonl
from citation_drift.preprocess import normalize_whitespace, prepare_records
from citation_drift.retrieval import bm25_top_k
from citation_drift.evaluate import evaluate_binary

def test_loader_and_preprocess(tmp_path):
    p = tmp_path / "data.jsonl"
    row = {
        "example_id": "e1", "source_paper_id": "p1",
        "claim": "  No   improvement was observed. ",
        "evidence": "No improvement was observed.",
        "gold_label": "SUPPORTED"
    }
    p.write_text(json.dumps(row) + "\n", encoding="utf-8")
    records, errors = load_jsonl(p)
    assert not errors
    processed = prepare_records(records)
    assert processed[0]["claim_processed"] == "No improvement was observed."
    assert "No" in processed[0]["claim_processed"]

def test_bm25():
    passages = [
        "The proposed system uses a transformer encoder.",
        "The paper reports a supervised classification experiment."
    ]
    result = bm25_top_k("transformer encoder", passages, top_k=1)
    assert len(result) == 1
    assert result[0]["text"] == passages[0]

def test_binary_evaluation():
    rows = [
        {"gold_label": "SUPPORTED", "alignscore": 0.9},
        {"gold_label": "NOT_SUPPORTED_IN_INSPECTED_SOURCE", "alignscore": 0.1},
        {"gold_label": "PARTIALLY_SUPPORTED", "alignscore": 0.5}
    ]
    metrics = evaluate_binary(rows, threshold=0.5)
    assert metrics["n_evaluated"] == 2
    assert metrics["accuracy"] == 1.0

def test_empty_preprocess_rejected():
    try:
        normalize_whitespace("   ")
    except ValueError:
        return
    raise AssertionError("Expected empty text to be rejected")
