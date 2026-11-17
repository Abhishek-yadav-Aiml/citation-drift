# Citation Drift Research — Google Colab Scaffold

**Target:** Hosted Google Colab runtime with optional NVIDIA GPU  
**Primary method:** AlignScore-base (frozen inference)  
**Retrieval:** BM25 (`rank-bm25`)  
**Secondary method:** FActScore-inspired atomic-fact decomposition (adaptation)

## Status — read before running

- Repository scaffold: created.
- Colab notebook: created.
- Runtime diagnostic: **NOT RUN**.
- AlignScore compatibility: **UNKNOWN until the Colab runtime is inspected**.
- Dataset: not downloaded.
- Model checkpoint: not downloaded.
- Experiment: not run.

## 1. Open the notebook

Upload `notebooks/00_colab_environment_check.ipynb` to Google Drive and open it with Google Colab.

In Colab choose **Runtime → Change runtime type → T4 GPU** (or another GPU option if available). GPU availability depends on account, quotas and service availability. The notebook also works in CPU mode for the diagnostic.

Colab runtimes are updated and contain preinstalled packages. Record the actual runtime rather than assuming a fixed Python/PyTorch/CUDA version. See:
- https://research.google.com/colaboratory/runtime-version-faq.html
- https://research.google.com/colaboratory/faq.html

## 2. Why we inspect before installing

The current upstream AlignScore `pyproject.toml` specifies:
- `torch>=1.12.1,<2`
- `transformers>=4.20.1,<5`
- `numpy>=1.23.1,<2`
- `pytorch_lightning>=1.7.7,<2`
- `protobuf<=3.20`

Source: https://github.com/yuh-zha/AlignScore/blob/main/pyproject.toml

Colab's published runtime versions have shipped with Python 3.12/3.13, NumPy 2.x and PyTorch 2.x. That is not automatically compatible with the package metadata above. An NVIDIA integration guide describes a PyTorch 2.0.1 installation path, which itself illustrates that installation guidance may differ from current package metadata:
https://docs.nvidia.com/nemo/guardrails/latest/configure-guardrails/guardrail-catalog/third-party/alignscore

Therefore:
1. Run the notebook's diagnostics first.
2. Save the complete output.
3. Do not downgrade PyTorch or replace CUDA packages yet.
4. We will select a tested-compatible route only after seeing the actual runtime output.

## 3. Candidate dependency plan (not a tested lockfile)

Core research packages:
- `numpy`
- `pandas`
- `scikit-learn`
- `rank-bm25`
- `pypdf`
- `PyYAML`
- `tqdm`
- `psutil`

AlignScore candidates:
- `torch` — use the Colab-provided build initially; do not reinstall yet.
- `transformers`
- `spacy`
- `nltk`
- `jsonlines`
- `datasets`
- `pytorch-lightning`
- `scipy`
- `tensorboard`
- `protobuf`

We intentionally do not pin/install the AlignScore stack before runtime inspection. Exact pins depend on Python, torch, CUDA and wheel availability in the active runtime.

## 4. Dataset access (later; do not download yet)

Candidate source pool: CS-PaperSum. First verify its official dataset card, identifier, version, fields, split, license and citation content. Do not assume it already contains claim–citation pairs, full-text PDFs or human support labels.

Procedure:
1. Inspect dataset card and sample rows.
2. Confirm source-paper IDs and citation markers exist in the relevant fields.
3. Check full-text availability and reuse terms per paper.
4. Record source ID, URL, version, access date and checksum in `data/manifests/source_manifest.csv`.
5. Keep raw data separate from processed data.
6. Never commit API keys or copyrighted full-text PDFs.

## 5. Repository structure

```text
citation_drift_research/
├── README.md
├── requirements-core.txt
├── requirements-alignscore-candidate.txt
├── configs/
│   ├── experiment.yaml
│   └── environment.yaml
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   ├── annotations/
│   └── manifests/
├── notebooks/
│   └── 00_colab_environment_check.ipynb
├── src/citation_drift/
│   ├── data/
│   ├── retrieval/
│   ├── verification/
│   └── evaluation/
├── scripts/
├── results/
│   ├── tables/
│   ├── figures/
│   └── logs/
├── paper/
├── tests/
└── .gitignore
```

## 6. Reproducibility

- Python, NumPy and PyTorch seed: `42` for randomized components.
- Record actual runtime, Python, torch, CUDA and GPU model per run.
- Record exact package versions after installation.
- Record model checkpoint revision and SHA-256 after download.
- Group data partitions by canonical source-paper ID.
- Keep test labels hidden during tuning.
- Save prompts, raw model responses and timestamps for hosted model calls.
- Use Google Drive for persistent data/logs; `/content` is ephemeral.

## 7. Stop condition

Run only `00_colab_environment_check.ipynb` now. It reports runtime and library diagnostics and writes an environment log. It does not install AlignScore, download weights, access the dataset or execute research experiments.

Send the complete output from every cell. Stop there until compatibility is reviewed.
