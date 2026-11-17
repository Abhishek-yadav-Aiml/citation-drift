import argparse
import csv
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from citation_drift.seed import set_seed
from citation_drift.data import load_jsonl
from citation_drift.preprocess import prepare_records
from citation_drift.alignscore_model import AlignScoreScorer
from citation_drift.evaluate import evaluate_binary
from citation_drift.plots import save_score_histogram

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="results/alignscore_predictions.csv")
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--threshold", type=float, default=None,
                        help="Optional threshold selected on DEV data only.")
    parser.add_argument("--positive-label", default="SUPPORTED")
    parser.add_argument("--negative-labels", nargs="*", default=[
        "NOT_SUPPORTED_IN_INSPECTED_SOURCE"
    ])
    args = parser.parse_args()

    set_seed(args.seed)
    records, errors = load_jsonl(args.input)
    records = prepare_records(records)

    scorer = AlignScoreScorer(
        checkpoint=args.checkpoint, device=args.device,
        batch_size=args.batch_size
    )

    contexts = [r["evidence_processed"] for r in records]
    claims = [r["claim_processed"] for r in records]
    scores = scorer.score(contexts, claims)

    for row, score in zip(records, scores):
        row["alignscore"] = score

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    columns = [
        "example_id", "source_paper_id", "claim_id", "partition",
        "claim", "evidence", "alignscore", "gold_label"
    ]
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)

    ckpt = Path(args.checkpoint)
    metadata = {
        "python": sys.version,
        "platform": platform.platform(),
        "seed": args.seed,
        "device": args.device,
        "batch_size": args.batch_size,
        "checkpoint_path": str(ckpt),
        "checkpoint_sha256": sha256(ckpt),
        "input_path": str(Path(args.input)),
        "n_records": len(records),
        "validation_errors": errors,
        "score_semantics": "continuous factual-consistency score; not a 4-class label",
    }
    Path("results").mkdir(exist_ok=True)
    Path("results/run_metadata.json").write_text(json.dumps(metadata, indent=2))

    save_score_histogram(
        scores, "results/score_distribution.png"
    )

    if args.threshold is not None:
        metrics = evaluate_binary(
            records, threshold=args.threshold,
            positive_label=args.positive_label,
            negative_labels=tuple(args.negative_labels)
        )
        Path("results/metrics.json").write_text(json.dumps(metrics, indent=2))
        print("Binary metrics saved. Confirm threshold was selected on DEV only.")

    print(f"Scored {len(records)} records.")
    print(f"Predictions: {out}")
    print("Metadata: results/run_metadata.json")
    print("Histogram: results/score_distribution.png")

if __name__ == "__main__":
    main()
