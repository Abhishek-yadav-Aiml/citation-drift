# Baseline Reproduction / Validation Report

**Project:** Detecting Citation Drift in AI-Generated Literature Summaries  
**Baseline under review:** AlignScore (Zha et al., 2023), intended checkpoint: AlignScore-base  
**Target runtime:** Google Colab, CPU execution intended  
**Report status:** PRELIMINARY — implementation audit blocked pending source artifacts  
**Audit date:** 2026-11-17

## 1. Executive status

A methodological validation cannot yet be completed. The user’s request contains the placeholder `[FILES]`, but no implementation files, dataset partition files, configuration files, complete actual logs, or measured result files were attached to this request.

A program running successfully is not sufficient evidence that a published baseline has been reproduced. The report therefore records only facts supported by the conversation and explicitly leaves uninspected items unresolved.

## 2. Evidence received so far

| Evidence item | Current evidence | Status |
|---|---|---|
| Published baseline selection | AlignScore, Zha et al. (2023), AlignScore-base intended | VERIFIED as project selection only |
| Official implementation source | User previously cloned the official repository in Colab; exact commit/hash not supplied | UNCERTAIN |
| Environment | Colab Python 3.13.16; x86_64; PyTorch 2.14.1+cu130; NumPy 2.4.6; Transformers 5.22.1 in one diagnostic | VERIFIED as a reported diagnostic snapshot |
| CPU tensor operation | 1000×1000 matrix multiplication succeeded in 0.158 seconds | VERIFIED as a basic CPU test only |
| Isolated environment | Python 3.10 environment at `/content/alignscore-env` was created according to conversation; final package state not supplied | UNCERTAIN |
| AlignScore import/inference | Import initially failed because spaCy was missing; later spaCy import failed because click was missing; later fixes were discussed but no successful inference log supplied | NEEDS CORRECTION / NOT VERIFIED |
| Dataset | CS-PaperSum is the planned candidate source pool; no actual corpus file or manifest supplied | UNCERTAIN |
| Data partition | No split manifest or source-paper grouping file supplied | NOT AUDITABLE |
| Preprocessing | M1 JSONL loader synthetic sanity test passed; M2 preprocessing code was supplied but execution output was not provided | PARTIALLY VERIFIED |
| Hyperparameters | Intended settings discussed: AlignScore-base, CPU, batch size 1; exact runtime config not supplied | UNCERTAIN |
| Random seeds | Project plan proposed seed 42; no executable seed log supplied | UNCERTAIN |
| Evaluation | Planned macro-F1 and related metrics; no prediction file, gold labels, or measured metrics supplied | NOT AUDITABLE |
| Benchmark protocol | Research design discussed, but no frozen protocol/config or run manifest supplied | UNCERTAIN |
| Measured results | No actual baseline score or evaluation output supplied | NOT RECEIVED |

## 3. Preliminary methodological audit

### 3.1 Preprocessing

**VERIFIED**
- A JSONL loader was executed on two synthetic records.
- Reported output: 2 records loaded, 0 validation errors, 2 unique source papers, 1 labeled record; sanity test passed.

**UNCERTAIN**
- Whether the actual research corpus uses the same schema.
- Whether original claim/evidence text is preserved alongside processed text.
- Whether preprocessing preserves scientific qualifiers, negation, numbers, units, equations, and citation markers.
- Whether long evidence is truncated, chunked, or passed as multiple contexts.

**Required checks**
1. Inspect the actual preprocessing source code.
2. Compare raw and processed text for a stratified sample, including negation, numerical values, units, symbols, and multi-sentence claims.
3. Record tokenizer, maximum input length, truncation behavior, chunking, and aggregation.
4. Confirm that the AlignScore model receives the intended context/claim order.

### 3.2 Architecture and checkpoint

**VERIFIED**
- AlignScore-base was selected as the intended published baseline.

**NEEDS CORRECTION / NOT VERIFIED**
- No successful AlignScore import and scoring output has been supplied.
- The previously reported missing `spacy` and `click` errors show that the package environment was not yet validated at those points.
- No checkpoint file checksum, model revision, or source repository commit has been supplied.

**Required checks**
1. Provide the exact official repository URL and Git commit hash.
2. Provide checkpoint source/revision, file size, and SHA-256.
3. Provide the exact constructor arguments and inference code.
4. Run a minimal real inference example and retain its full stdout/stderr.
5. Verify whether any checkpoint conversion or architecture modification occurred.

### 3.3 Hyperparameters and inference settings

**UNCERTAIN**
- Intended batch size 1 and CPU device were discussed, but the final executed configuration is unknown.
- Model name, evaluation mode, maximum sequence length, precision, and batching behavior are not evidenced by a successful run.

**Required checks**
- Supply the exact config file and complete constructor call.
- Record model/checkpoint name, batch size, device, evaluation mode, max length, truncation, precision, and any score normalization.
- Confirm model is in evaluation mode and gradients are disabled during inference, as appropriate to the official implementation.

### 3.4 Randomness and reproducibility

**UNCERTAIN**
- Seed 42 was proposed in the project plan, but no code or runtime log demonstrates seed control.
- Hosted generation may remain nondeterministic even when a local seed is set.

**Required checks**
- Supply seed-setting code for Python, NumPy, and PyTorch.
- Record whether deterministic algorithms were enabled and any performance implications.
- Record hosted model/provider, model version, prompt, temperature, timestamp, and raw response if summaries or atomic facts were generated through an API.
- Do not imply a seed controls nondeterministic hosted services.

### 3.5 Dataset and partition protocol

**NOT AUDITABLE**
- No actual dataset, annotation file, source manifest, or split manifest was supplied.

**Required checks**
1. Supply dataset version, source URL, license, access date, and checksum.
2. Supply the exact row/claim counts and label distribution.
3. Supply train/development/validation/test assignment file.
4. Verify all claims from the same canonical source paper remain in one partition.
5. Check paper versions, duplicate papers, duplicate claims, and cross-partition leakage.
6. Confirm test labels were not used for threshold selection, prompt tuning, retrieval tuning, or model selection.
7. Explain handling of multiple citations, partial support, insufficient evidence, and contradictory evidence.

### 3.6 Evaluation and benchmark protocol

**NOT AUDITABLE**
- No gold-label file, prediction file, metric script, or actual measured result was supplied.

**Required checks**
- Supply adjudicated gold labels and raw independent annotator labels.
- Supply prediction outputs with example IDs and continuous AlignScore values.
- Supply the exact score-to-label rule and thresholds.
- Confirm thresholds were selected using development/validation data only.
- Supply metric code and per-class precision/recall/F1, macro-F1, confusion matrix, and denominators.
- Report agreement between annotators and adjudication procedure.
- Ensure a continuous AlignScore is not described as a four-class contradiction classifier unless a separately validated mapping supports that claim.

## 4. Acceptable adaptations versus comparison-invalidating changes

| Change | Assessment |
|---|---|
| Running the official checkpoint on CPU instead of GPU | Usually acceptable for inference if checkpoint, preprocessing, numerical precision, and scoring are unchanged; report runtime and any numerical differences |
| Using batch size 1 | Usually acceptable if inference is independent per example and no batch-dependent behavior changes |
| Applying the baseline to computer-science claims rather than its original benchmark domain | Acceptable domain adaptation, but not an exact reproduction of the original benchmark |
| Using human-annotated claim–citation pairs instead of the original benchmark | Acceptable new evaluation task; results must not be presented as directly comparable to original paper benchmark scores |
| Changing checkpoint or architecture | Changes the baseline; must be reported and justified |
| Changing tokenization, truncation, context/claim order, or aggregation | Potentially material; requires explicit audit and sensitivity checks |
| Tuning score thresholds on the test set | Invalidates held-out evaluation |
| Random claim-level splitting when papers overlap across partitions | Risks leakage; invalid for the intended source-paper generalization claim |
| Treating retrieval failure as NOT_SUPPORTED | Invalid label conflation |
| Treating AlignScore similarity/alignment score as a contradiction detector without validation | Invalid interpretation |
| Reporting macro-F1 without gold labels and a predeclared score-to-label mapping | Invalid evaluation claim |

## 5. Required unit and sanity tests

The following tests should be run once source code and data are available:

1. **Loader tests:** malformed JSONL, missing required fields, duplicate IDs, invalid labels, empty strings, non-string values.
2. **Preprocessing invariance tests:** repeated whitespace changes should not alter meaning; negation, numbers, units, entities, and punctuation should remain intact.
3. **Model smoke test:** one known context/claim pair produces one finite numeric score; model loads from the recorded checkpoint; CPU execution is confirmed.
4. **Determinism test:** score the same fixed pair twice in the same runtime and compare within a declared tolerance.
5. **Batch consistency test:** compare single-item and batched scores if batching is used.
6. **Input-order test:** verify contexts and claims are passed in the official expected order.
7. **Evaluation tests:** hand-computed confusion matrix and macro-F1 on a tiny fixture.
8. **Split integrity test:** no canonical source-paper ID occurs in more than one partition.
9. **Leakage test:** no exact duplicate claim/evidence pair crosses partitions.
10. **Artifact test:** predictions, configs, logs, package freeze, checkpoint hash, and run metadata are saved.

## 6. Artifacts required to complete the audit

Please upload or paste:

- `test_alignscore.py` and all project source files involved in loading, preprocessing, scoring, and evaluation.
- The exact AlignScore repository commit hash (`git rev-parse HEAD`).
- `pip freeze` from `/content/alignscore-env`.
- The final complete AlignScore import/inference log, including any errors.
- The checkpoint filename, file size, source URL/revision, and SHA-256.
- Dataset sample/schema and source manifest (remove private or restricted content if necessary).
- Annotation guideline and adjudicated label file.
- Partition/split manifest grouped by source-paper ID.
- Experiment config and seed-setting code.
- Raw predictions with example IDs, scores, predicted labels, and gold labels.
- Metric script and actual evaluation output.

Do not upload API keys, credentials, or copyrighted full-text PDFs unless sharing is permitted. A metadata manifest and short permitted excerpts are sufficient for initial review.

## 7. Current verdict

**Baseline reproduction status: NOT VALIDATED.**

This is not a finding that the method is incorrect. It means the evidence needed to judge fidelity has not yet been provided. The successful synthetic loader test and CPU tensor test establish only those narrow checks; they do not validate AlignScore inference or the research benchmark.

## 8. Audit decision gate

No extensions, alternative verifiers, or performance comparisons should be started until:
- official baseline source and checkpoint are pinned;
- successful real inference is demonstrated;
- preprocessing and model inputs are audited;
- data partitions are checked for source-paper leakage;
- gold labels and score-to-label mapping are defined;
- evaluation metrics are independently sanity-tested;
- all deviations are recorded.
