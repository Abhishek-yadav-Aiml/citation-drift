# Citation Drift Research — Runnable Colab Project

This repository is a **research pipeline scaffold** for evaluating AlignScore-base on claim–evidence pairs in computer-science literature summaries.

## What this project does

1. Loads a JSONL claim/evidence dataset.
2. Validates required fields and optional gold labels.
3. Preserves raw text and creates whitespace-normalized copies.
4. Optionally retrieves evidence passages with BM25 from a paper's supplied passages.
5. Scores each `(context, claim)` pair using the official AlignScore API.
6. Saves continuous scores and metadata.
7. If a development-set threshold is explicitly supplied, evaluates binary supported/not-supported predictions.
8. Saves metrics and plots.

**Important methodological limits**
- AlignScore returns a continuous factual-consistency score. It is not automatically a validated four-class classifier for `SUPPORTED`, `PARTIALLY_SUPPORTED`, `NOT_SUPPORTED_IN_INSPECTED_SOURCE`, and `CONTRADICTED`.
- This code therefore saves continuous scores by default. Binary classification is optional and must use a threshold chosen on development data only.
- Do not merge retrieval failure with `NOT_SUPPORTED_IN_INSPECTED_SOURCE`.
- CS-PaperSum is treated only as a candidate paper pool, not as a ready-made claim-citation benchmark.
- The project does not train AlignScore. It uses the released frozen checkpoint.
- The included sample JSONL is synthetic and is only for testing the loader, not research results.

## Official baseline reference

AlignScore: Yuheng Zha, Yichi Yang, Ruichen Li, and Zhiting Hu (ACL 2023), *AlignScore: Evaluating Factual Consistency with a Unified Alignment Function*.

Official code: https://github.com/yuh-zha/AlignScore  
Official README/API: https://github.com/yuh-zha/AlignScore#evaluating-factual-consistency  
Checkpoint: https://huggingface.co/yzha/AlignScore/resolve/main/AlignScore-base.ckpt

The official API is:

```python
from alignscore import AlignScore
scorer = AlignScore(
    model="roberta-base",
    batch_size=1,
    device="cpu",
    ckpt_path="/content/models/AlignScore-base.ckpt",
    evaluation_mode="nli_sp",
)
scores = scorer.score(contexts=[...], claims=[...])
```

The original README recommends installing the compatible PyTorch version before AlignScore, then installing the repository and spaCy English model. Dependency compatibility must be tested in the actual Colab runtime. Do not assume current Colab package versions satisfy the legacy requirements.

## Colab use

1. Upload this ZIP to Google Drive and extract it, or upload the extracted project folder.
2. Open `notebooks/00_run_pipeline_colab.ipynb` with Colab.
3. Set `PROJECT_DIR` in the first configuration cell to the extracted folder location.
4. Put your own annotated JSONL at `data/processed/claim_evidence.jsonl`.
5. Put the AlignScore-base checkpoint at `models/AlignScore-base.ckpt`.
6. Install and validate AlignScore in the dedicated environment before running the pipeline.
7. Run the notebook cells in order.

If using the previously created environment:
`/content/alignscore-env/bin/python`, execute the pipeline with that interpreter:

```bash
/content/alignscore-env/bin/python scripts/run_pipeline.py \
  --input data/processed/claim_evidence.jsonl \
  --output results/alignscore_predictions.csv \
  --checkpoint models/AlignScore-base.ckpt \
  --device cpu \
  --batch-size 1
```

Adjust paths to absolute Colab paths if needed.

## Dataset schema

One JSON object per line:

```json
{
  "example_id": "ex001",
  "source_paper_id": "paper001",
  "claim_id": "claim001",
  "claim": "The proposed model improves document classification.",
  "evidence": "The paper reports improved classification performance.",
  "gold_label": "SUPPORTED",
  "partition": "test"
}
```

Required: `example_id`, `source_paper_id`, `claim`, `evidence`.  
Optional: `claim_id`, `gold_label`, `partition`.

Allowed gold labels:
- `SUPPORTED`
- `PARTIALLY_SUPPORTED`
- `NOT_SUPPORTED_IN_INSPECTED_SOURCE`
- `CONTRADICTED`

Also allowed for *evidence availability* in a separate field (do not conflate with support):
- `AVAILABLE`
- `INSUFFICIENT_ACCESS`
- `INSUFFICIENT_RETRIEVAL`
- `INSUFFICIENT_CONTEXT`

The pipeline keeps gold labels unchanged. It does not convert them into AlignScore predictions unless a binary threshold is explicitly supplied.

## BM25 input schema (optional)

A record may include `candidate_passages`, a list of strings, and `claim` as query. The pipeline selects top-k passages and stores them in `retrieved_evidence`. If `evidence` is already provided, that supplied evidence is used by default. To use BM25 output as the AlignScore context, run with `--use-bm25`.

BM25 is lexical retrieval; save retrieval rank and scores for a full research run. The compact scaffold stores the selected passage strings, not a full IR benchmark.

## Outputs

- `results/alignscore_predictions.csv`: example IDs, paper IDs, claim, context, score, gold label, partition.
- `results/run_metadata.json`: environment, config, checkpoint hash, seed.
- `results/metrics.json`: only created when gold labels and a binary threshold are supplied.
- `results/score_distribution.png`: score histogram.
- `results/confusion_matrix.png`: only for the optional binary evaluation.

## Threshold protocol

Do not choose a threshold based on the test partition. Determine it using development data only, save the selected threshold and selection procedure, then evaluate the held-out test partition once. Since the four human labels contain partial support and contradiction, a binary mapping is a separate operational simplification and must be declared. The default mapping in this scaffold is not set automatically.

## Reproducibility

- Default seed: 42.
- The baseline is frozen inference; there is no model training loop.
- Record the exact Git commit of AlignScore and SHA-256 of the checkpoint.
- Keep paper-level partitions grouped by `source_paper_id`.
- Do not place private API keys or restricted PDFs in the repository.
- Colab `/content` is ephemeral; copy results to Google Drive for persistence.

## Debugging

Run:
```bash
python -m pytest -q
```

For AlignScore import/checkpoint errors, first verify:
- correct interpreter is `/content/alignscore-env/bin/python`;
- `import alignscore, torch, spacy` succeeds in that interpreter;
- `en_core_web_sm` is installed for that interpreter;
- checkpoint exists and checksum is recorded;
- the same environment has all runtime dependencies.

Do not report the baseline as reproduced until actual checkpoint inference and the evaluation protocol have been validated.
