# Repository contents and reproducibility status

This repository combines the code scaffold, research notes, annotation specification, preliminary experiment report, and IEEE/Overleaf source files for the project **Detecting Citation Drift in AI-Generated Literature Summaries**.

## What is included

- AlignScore-oriented Python scaffold, configuration, synthetic input example, notebook, and unit tests.
- Research decisions, annotation guideline/pilot specification, and baseline reproduction validation report.
- A preliminary experiment report document describing the separately reported SciFact/DeBERTa-v3 run.
- IEEE conference-style LaTeX source and BibTeX references.

## What is not included

- Real datasets or downloaded paper corpora.
- Model checkpoint weights.
- Private annotation files, API keys, credentials, or `.env` files.
- The uploaded source PDF/text used during drafting; verify ownership and redistribution rights before publishing source material.

## Reproduction status

The SciFact + DeBERTa-v3 metrics in the report are author-reported from a separate Colab experiment. The executable code/notebook for that experiment is not included here. The AlignScore pipeline is a scaffold and has not been successfully run end-to-end. Treat its import, checkpoint inference, and test commands as pending verification.

## Before making the repository public

1. Verify dataset licenses and cite the exact dataset release/version.
2. Verify the AlignScore checkpoint and Hugging Face model terms.
3. Confirm you have redistribution rights for every paper/report and third-party file.
4. Add a license only for material you own and can license.
5. Run tests and at least one reproducible end-to-end experiment; commit logs/configuration, not restricted data or weights.
