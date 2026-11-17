# Detecting Citation Drift in AI-Generated Literature Summaries

This repository contains the project code scaffold and supporting research materials. Start with this README, then see [`GITHUB_UPLOAD_GUIDE.md`](GITHUB_UPLOAD_GUIDE.md) for publishing instructions and [`REPOSITORY_STATUS.md`](REPOSITORY_STATUS.md) for a concise inventory and reproducibility caveats.

## Supporting materials

- `docs/research_decisions.md` — research design decisions and rationale.
- `docs/annotation_guideline_pilot_spec.md` — claim/evidence annotation labels and pilot specification.
- `docs/baseline_reproduction_validation_report.md` — validation status and reproduction audit.
- `reports/Preliminary_Citation_Drift_Experiment_Report.docx` — report of the separately run preliminary SciFact/DeBERTa-v3 experiment.
- `paper/overleaf/` — IEEE conference-style LaTeX source and BibTeX references.

## 1. Project status and scope

This repository contains a **research pipeline scaffold** for evaluating the frozen AlignScore-base model on claim–evidence pairs. It includes JSONL loading and validation, conservative text normalization, an optional BM25 retrieval helper, an AlignScore adapter, optional binary evaluation, metadata logging, a score-distribution plot, configuration files, and unit tests.

**Important: the AlignScore pipeline in this repository has not been successfully executed end to end.** The AlignScore import previously failed in the Colab environment, and no successful checkpoint inference from `scripts/run_pipeline.py` has been reported.

A separate preliminary experiment was run in Google Colab using SciFact and the pretrained `cross-encoder/nli-deberta-v3-base` NLI model. That experiment is described below so that its results are not confused with the AlignScore scaffold. The code for that separate NLI experiment is not currently included as a runnable script in this repository.

### What has actually been demonstrated

| Component | Status |
|---|---|
| Repository scaffold and configuration files | Present |
| JSONL loader, preprocessing, BM25 helper, evaluation and plotting modules | Present |
| Synthetic JSONL fixture | Present; demonstration data only |
| SciFact + DeBERTa-v3 NLI experiment | Run separately in Colab; results reported by the project author |
| AlignScore import | Attempted; failed in the reported environment |
| AlignScore checkpoint download | Not confirmed |
| AlignScore inference through this repository | **Not run / not reproduced** |
| Repository test suite (`pytest`) | **[TEST REQUIRED]** |
| End-to-end pipeline command | **[TEST REQUIRED]** |

Do not cite the SciFact/DeBERTa results as results produced by the AlignScore pipeline.

## 2. Problem statement

The broader research problem is to identify cases where factual claims in AI-generated scientific literature summaries are not accurately supported by the cited source papers. A claim may be fully supported, partially supported, absent from the inspected source, or contradicted by it. Evidence access and retrieval status must be recorded separately: an inaccessible paper or failed retrieval is not proof that a claim is unsupported.

The intended annotation labels in `configs/label_policy.md` are:

- `SUPPORTED`
- `PARTIALLY_SUPPORTED`
- `NOT_SUPPORTED_IN_INSPECTED_SOURCE`
- `CONTRADICTED`

Evidence availability is a separate field:

- `AVAILABLE`
- `INSUFFICIENT_ACCESS`
- `INSUFFICIENT_RETRIEVAL`
- `INSUFFICIENT_CONTEXT`

The current AlignScore scaffold produces continuous factual-consistency scores. It does **not** implement a validated four-class citation-drift classifier.

## 3. Repository layout

```text
citation_drift_full_project/
├── README.md
├── requirements-core.txt
├── configs/
│   ├── experiment.yaml
│   └── label_policy.md
├── data/
│   ├── processed/
│   │   └── sample_synthetic.jsonl
│   ├── raw/
│   ├── interim/
│   └── annotations/
├── models/
├── notebooks/
│   └── 00_run_pipeline_colab.ipynb
├── prompts/
│   └── research_prompts.md
├── results/
├── scripts/
│   └── run_pipeline.py
├── src/citation_drift/
│   ├── alignscore_model.py
│   ├── data.py
│   ├── evaluate.py
│   ├── plots.py
│   ├── preprocess.py
│   ├── retrieval.py
│   └── seed.py
└── tests/
    └── test_core.py
```

`sample_synthetic.jsonl` contains two invented demonstration records. It is included only to illustrate the input schema and must not be included in research metrics or described as real experimental data.

## 4. Environment and setup

### Target environment

The project notebook targets Google Colab. The configured AlignScore run uses CPU and batch size 1. GPU use is optional in principle, but it has not been benchmarked for this project.

The recorded Colab diagnostics from earlier sessions included Python 3.13.x and PyTorch 2.x in the default runtime. A separate Python 3.10 environment was then created at `/content/alignscore-env`. The exact final runtime state and package versions are not preserved in a complete successful environment log.

The following commands were reported as run while recreating the dedicated environment:

```bash
pip install -q uv
uv python install 3.10
uv venv /content/alignscore-env --python 3.10
```

The user also reported completing the core dependency installation command below after recreating the environment. A successful package-resolution log was not retained in the repository, so verify it in a fresh runtime:

```bash
uv pip install \
  --python /content/alignscore-env/bin/python \
  -r requirements-core.txt
```

**[TEST REQUIRED]** Confirm the interpreter and installed packages:

```bash
/content/alignscore-env/bin/python --version
/content/alignscore-env/bin/python -c "import numpy, pandas, sklearn, rank_bm25, matplotlib, yaml; print('Core imports OK')"
```

### Dependencies

`requirements-core.txt` currently lists unpinned dependencies:

```text
numpy
pandas
scikit-learn
rank-bm25
matplotlib
seaborn
PyYAML
pytest
```

There is no complete lockfile in this project. Exact installed versions must be recorded from the runtime before a reproducibility claim is made.

The AlignScore project has additional legacy dependencies and version constraints. The core requirements file is **not sufficient by itself** to install AlignScore. The previous attempt to import AlignScore encountered missing dependencies (including `spacy` and `click`); the final import did not succeed in the reported session.

**[TEST REQUIRED]** After installing the compatible AlignScore dependency stack in the same interpreter, run:

```bash
/content/alignscore-env/bin/python -c "from alignscore import AlignScore; print('AlignScore import OK')"
```

Do not assume that this command works until it completes successfully in the active runtime.

## 5. Dataset access, preparation, and license

### 5.1 SciFact data used in the separate NLI baseline

The separate DeBERTa-v3 NLI experiment downloaded SciFact from the following public data archive URL:

```text
https://scifact.s3-us-west-2.amazonaws.com/release/latest/data.tar.gz
```

The archive was extracted in the temporary Colab filesystem under `/content/scifact`. The development claims and abstract corpus were used to construct 338 claim–evidence pairs.

The reported gold-label distribution was:

- SUPPORT: 216
- CONTRADICT: 122

The data archive's precise release/version identifier and a license file or license statement were not saved in this repository. **Check the dataset's official repository/card and license before redistributing the dataset or derived files.** This README does not grant rights to redistribute SciFact content.

### 5.2 Candidate source pool for the broader project

CS-PaperSum was considered as a candidate source-paper pool in the research plan. It is not included in this repository, was not downloaded as part of the recorded run, and has not been verified as a ready-made claim–citation benchmark. Before use, inspect the official dataset card, version, fields, license, citation information, and full-text access terms. Do not assume that it contains human-annotated claim–citation support labels.

### 5.3 Preparing project JSONL data

The AlignScore pipeline expects one JSON object per line in:

```text
data/processed/claim_evidence.jsonl
```

Required fields:

- `example_id`: unique example identifier
- `source_paper_id`: canonical source paper identifier
- `claim`: claim text
- `evidence`: inspected evidence text

Optional fields:

- `claim_id`
- `gold_label`
- `partition`
- `candidate_passages` (list of candidate evidence passages for the BM25 helper)
- `evidence_availability` (separate from the support label)

Example schema only (replace with properly sourced and annotated data):

```json
{
  "example_id": "ex001",
  "source_paper_id": "paper001",
  "claim_id": "claim001",
  "claim": "A scientific claim goes here.",
  "evidence": "The inspected source passage goes here.",
  "gold_label": "SUPPORTED",
  "partition": "dev",
  "evidence_availability": "AVAILABLE"
}
```

Do not use this illustrative record as a real observation. Keep raw source files, annotations, and processed JSONL separate. Store source identifiers, URLs, versions, access dates, and checksums in a data manifest. Split by `source_paper_id` so claims from the same source paper do not leak across partitions.

### 5.4 Data privacy and repository hygiene

The `.gitignore` excludes raw/interim/annotation data, model checkpoint files (`*.ckpt`), results, local environments, and `.env` files. Keep private data, API keys, access tokens, restricted PDFs, and non-redistributable model weights out of Git. Do not commit downloaded full text unless its license explicitly permits redistribution.

## 6. Baselines and experimental commands

### 6.1 Separate SciFact + DeBERTa-v3 NLI experiment (reported as executed)

A separate Colab session used:

- Dataset: SciFact development split
- Number of claim–evidence pairs: 338
- Model: `cross-encoder/nli-deberta-v3-base`
- Model output mapping: index 0 = contradiction, 1 = entailment, 2 = neutral
- Mapping for comparison: entailment → SUPPORT; contradiction → CONTRADICT
- No fine-tuning was performed.

The reported measurements were:

| Measure | Reported value |
|---|---:|
| Overall accuracy across 338 examples, counting NEUTRAL as incorrect | 45.56% |
| Non-neutral predictions | 170 |
| Coverage | 50.30% |
| Correct non-neutral predictions | 154 |
| Conditional accuracy on 170 non-neutral predictions | 90.59% |
| Conditional macro F1 | 0.91 |
| NEUTRAL predictions | 168 |

The full confusion matrix (gold rows; predicted columns) was:

| Gold / predicted | SUPPORT | CONTRADICT | NEUTRAL |
|---|---:|---:|---:|
| SUPPORT | 73 | 13 | 130 |
| CONTRADICT | 3 | 81 | 38 |

These values were reported from the separate Colab run. The notebook/script that generated this DeBERTa experiment is not currently present in this repository, so the experiment is not independently reproducible from this repository alone. Preserve the original Colab notebook and prediction CSV with the research artifacts.

The following commands describe the separate Colab workflow that was reported as executed. They are included for provenance; they are **not** a script shipped in this repository:

```python
# Install the libraries used by the separate NLI experiment.
!pip install -q sentence-transformers scikit-learn pandas matplotlib

# Download the SciFact archive into Colab temporary storage.
import urllib.request
import tarfile

url = "https://scifact.s3-us-west-2.amazonaws.com/release/latest/data.tar.gz"
archive = "/content/scifact.tar.gz"
urllib.request.urlretrieve(url, archive)

with tarfile.open(archive, "r:gz") as tar:
    tar.extractall("/content/scifact", filter="data")
```

The model inference step used the Hugging Face Sentence-Transformers cross-encoder interface:

```python
import torch
from sentence_transformers import CrossEncoder

model = CrossEncoder(
    "cross-encoder/nli-deberta-v3-base",
    device="cuda" if torch.cuda.is_available() else "cpu"
)

pairs = list(zip(df["evidence"], df["claim"]))
scores = model.predict(pairs, batch_size=8, show_progress_bar=True)

labels = ["CONTRADICT", "SUPPORT", "NEUTRAL"]
df["predicted_label"] = [
    labels[int(index)] for index in scores.argmax(axis=1)
]
```

The reported model configuration was `{0: 'contradiction', 1: 'entailment', 2: 'neutral'}`. The output CSV was saved as `/content/scifact_predictions.csv`. These code fragments reflect the reported workflow, but a clean end-to-end rerun and preservation of the exact notebook are still recommended.

### 6.2 AlignScore-base baseline implemented in this repository

The AlignScore pipeline is a separate planned baseline. It uses the official AlignScore API and a frozen checkpoint; it does not train AlignScore.

The expected checkpoint path is:

```text
models/AlignScore-base.ckpt
```

The upstream checkpoint URL recorded in the project scaffold is:

```text
https://huggingface.co/yzha/AlignScore/resolve/main/AlignScore-base.ckpt
```

The checkpoint was not confirmed downloaded in the recorded environment. Review the upstream repository and model terms before downloading or redistributing weights. The `.gitignore` excludes checkpoint files.

**[TEST REQUIRED]** After confirming the checkpoint is available and the AlignScore import succeeds, run from the repository root:

```bash
/content/alignscore-env/bin/python -m pytest -q

/content/alignscore-env/bin/python scripts/run_pipeline.py \
  --input data/processed/claim_evidence.jsonl \
  --output results/alignscore_predictions.csv \
  --checkpoint models/AlignScore-base.ckpt \
  --device cpu \
  --batch-size 1 \
  --seed 42
```

The second command requires a real, appropriately annotated JSONL file at the input path. The included synthetic fixture is for software smoke tests only and must not be used for research claims.

### 6.3 Optional binary evaluation

The script accepts a threshold only when it has been selected using development data and frozen before test evaluation.

**[TEST REQUIRED]** Example command shape:

```bash
/content/alignscore-env/bin/python scripts/run_pipeline.py \
  --input data/processed/claim_evidence.jsonl \
  --output results/alignscore_predictions.csv \
  --checkpoint models/AlignScore-base.ckpt \
  --device cpu \
  --batch-size 1 \
  --seed 42 \
  --threshold <DEV_SELECTED_THRESHOLD>
```

Replace the placeholder with a threshold selected on development data. Do not tune the threshold on the test set. By default, the binary evaluator compares `SUPPORTED` with `NOT_SUPPORTED_IN_INSPECTED_SOURCE`; partial and contradicted labels are excluded. This is a binary simplification, not a four-class evaluation.

## 7. Evaluation protocol

The AlignScore model returns a continuous factual-consistency score. It is not intrinsically a validated four-class classifier for the four human labels above.

The repository's default behavior is to save continuous scores. Optional binary evaluation requires:

1. A declared positive and negative label mapping.
2. A threshold selected using development data only.
3. A frozen threshold before held-out test evaluation.
4. Explicit reporting of excluded labels and the number of evaluated examples.

Do not merge failed retrieval or inaccessible full text into `NOT_SUPPORTED_IN_INSPECTED_SOURCE`. Evidence availability must remain a separate annotation dimension.

For the separate DeBERTa NLI run, overall accuracy included all 338 examples and treated NEUTRAL as incorrect because the gold labels were binary. Conditional accuracy and F1 were calculated only on the 170 non-neutral predictions. Always report the 50.30% coverage with the 90.59% conditional accuracy.

## 8. Reproducing key figures and outputs

For a successful AlignScore run, `scripts/run_pipeline.py` is designed to write:

- `results/alignscore_predictions.csv`
- `results/run_metadata.json`
- `results/score_distribution.png`
- `results/metrics.json` when optional threshold evaluation is requested

The score histogram is generated by `src/citation_drift/plots.py`.

The current plotting module creates a score-distribution histogram only. It does not currently create a confusion-matrix figure. Confusion-matrix values are returned by the evaluation helper as JSON data; a confusion-matrix plotting script is **[TEST REQUIRED / NOT IMPLEMENTED]**.

The DeBERTa SciFact confusion matrix and metrics above were printed in a separate Colab experiment. This repository does not currently contain a script to regenerate those exact DeBERTa outputs.

## 9. Compute requirements

### Configured settings

`configs/experiment.yaml` currently specifies:

- Baseline: `AlignScore-base`
- Backbone: `roberta-base`
- Evaluation mode: `nli_sp`
- Device: `cpu`
- Batch size: `1`
- Seed: `42`
- Checkpoint: `models/AlignScore-base.ckpt`
- Retrieval: disabled by default; top-k configured as 5

CPU is the configured default. GPU execution may be possible depending on the compatible PyTorch/CUDA environment, but it has not been validated for this repository. No reliable runtime or memory benchmark is available. Actual compute requirements should be recorded after a successful inference run.

Colab's temporary `/content` storage is ephemeral. Copy notebooks, logs, predictions, and figures to persistent storage after execution.

## 10. Configuration and dependency files

The repository includes:

- `configs/experiment.yaml`: model, dataset, retrieval, evaluation, and output settings.
- `configs/label_policy.md`: support labels and separate evidence-availability labels.
- `requirements-core.txt`: core Python dependencies (currently unpinned).
- `notebooks/00_run_pipeline_colab.ipynb`: Colab entry notebook.
- `.gitignore`: excludes local environments, secrets, raw/interim/annotation data, checkpoints, and results.

There is no fully pinned lockfile. Record `python --version` and `pip freeze` (or the equivalent from the `uv` environment) for each final run. The current notebook uses `/content/alignscore-env/bin/python`; update the path if the environment is created elsewhere.

`configs/experiment.yaml` records intended defaults, but `scripts/run_pipeline.py` currently reads its settings from command-line arguments and does not parse that YAML file. Keep command-line values synchronized with the YAML manually until configuration loading is implemented.

## 11. Limitations

- The AlignScore pipeline in this repository has not been successfully run end to end.
- The included JSONL fixture is synthetic and is not research data.
- The separate SciFact/DeBERTa experiment is not implemented as a reproducible script in this repository.
- SciFact is a scientific claim-verification benchmark, not a direct benchmark of AI-generated literature summaries and their citation links.
- The DeBERTa results are from the development split; no independent test-set result is reported here.
- AlignScore produces a continuous score and is not automatically a four-class citation-drift classifier.
- BM25 helper code exists, but the current `scripts/run_pipeline.py` CLI does not expose a `--use-bm25` argument. BM25 retrieval is therefore not wired into the current command-line pipeline.
- The repository does not currently generate a confusion-matrix image.
- Dataset and model redistribution terms must be checked at their original sources before redistribution.

## 12. Credits and citations

### SciFact

D. Wadden, S. Lin, K. Lo, L. L. Wang, M. van Zuylen, A. Cohan, and H. Hajishirzi, “Fact or Fiction: Verifying Scientific Claims,” in *Proceedings of EMNLP*, 2020, pp. 7534–7550. DOI: `10.18653/v1/2020.emnlp-main.609`.

### DeBERTa / DeBERTa-v3

P. He, X. Liu, J. Gao, and W. Chen, “DeBERTa: Decoding-enhanced BERT with Disentangled Attention,” ICLR, 2021.

P. He, J. Gao, and W. Chen, “DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Gradient-Disentangled Embedding Sharing,” ICLR, 2023.

### AlignScore

Y. Zha, Y. Yang, R. Li, and Z. Hu, “AlignScore: Evaluating Factual Consistency with a Unified Alignment Function,” ACL, 2023. Official implementation: <https://github.com/yuh-zha/AlignScore>.

### NLI model

Model identifier used in the separate Colab baseline: <https://huggingface.co/cross-encoder/nli-deberta-v3-base>. Cite the model card and its stated upstream model/license terms when using or redistributing it.

## 13. License

No project-level `LICENSE` file is currently included. Therefore, this repository should be treated as having **no explicit open-source license** until the project owner adds one.

Dataset and pretrained-weight licenses are separate from the repository license. Check the SciFact dataset terms, the Hugging Face model card, and the AlignScore repository/checkpoint terms independently. Do not redistribute datasets, PDFs, or weights unless their terms permit it.

## 14. Minimum reproduction checklist for a second student

A second student should complete and record each item:

- [ ] Obtain this repository and record its commit hash or archive checksum.
- [ ] Read `configs/label_policy.md` and understand that support labels and evidence-availability labels are separate.
- [ ] Create a fresh Colab runtime and record date, Python version, OS, CPU/GPU, PyTorch, CUDA, and memory.
- [ ] Create the Python environment and install `requirements-core.txt`.
- [ ] Record the complete installed dependency versions.
- [ ] Run `python -m pytest -q`; save the output. **[TEST REQUIRED]**
- [ ] Obtain the dataset from its official source and verify its version and license.
- [ ] Prepare a JSONL file with the required schema; validate unique example IDs and non-empty claim/evidence fields.
- [ ] Keep source-paper groups separated across train/dev/test partitions.
- [ ] Obtain the AlignScore checkpoint from its official source, review its terms, and record its SHA-256 hash.
- [ ] Confirm `from alignscore import AlignScore` succeeds in the selected interpreter. **[TEST REQUIRED]**
- [ ] Run the AlignScore pipeline on a small permitted test subset. **[TEST REQUIRED]**
- [ ] Run the full planned dataset only after the smoke test succeeds. **[TEST REQUIRED]**
- [ ] Save predictions, run metadata, score histogram, and logs.
- [ ] If binary evaluation is used, document the development-only threshold-selection procedure and freeze the threshold before test evaluation.
- [ ] Confirm that no API keys, private annotations, restricted full-text PDFs, or unlicensed weights are committed.
- [ ] Do not claim that the AlignScore baseline is reproduced until inference and output files have been successfully generated.

---

**Reproduction status at the time this README was written:** the separate SciFact/DeBERTa NLI baseline has reported Colab results; the AlignScore pipeline in this repository remains **not reproduced**.
