# Research Decisions Log

## Project
**Detecting Citation Drift in AI-Generated Literature Summaries**

## Source audited
- File: `mcl2026008_updated (1).pdf`
- Length: 7 pages
- Scope: 28 numbered references; five-layer taxonomy; methods, resources, limitations, and proposed workflow.
- Audit status: review inspected; original publications have not yet been independently re-verified in this audit.

## Evidence-label convention
- **VERIFIED**: directly supported by the inspected review or an inspected primary source.
- **INFERRED**: research interpretation or proposed hypothesis, not established by the review.
- **UNKNOWN**: evidence is not available or has not been checked.

## 1. Scope established
**VERIFIED:** The review treats citation drift as a multi-level reliability problem involving bibliographic validity, citation relevance, evidence alignment, evidence-grounded support, and stability across generations.

**Source:** Review pp. 1–3, Sections 1–5.

## 2. Central methodological families
1. Source-summary factuality: [1]–[3].
2. Sampling disagreement: SelfCheckGPT [4].
3. Atomic-fact evaluation: FActScore [5].
4. Semantic alignment: AlignScore [6].
5. Bibliographic/reference verification: [7]–[10], CiteCheck [21].
6. Citation attribution and evidence-grounded verification: CiteME [11], OpenScholar [15], SourceCheckup [22], RefLens [23], SemanticCite [24].
7. Repeated-generation citation stability: Seetha Ram [17].

**VERIFIED from review:** The review describes these families and their intended roles.
**UNKNOWN:** Comparative performance of these methods on one shared citation-drift dataset.

## 3. Datasets and resources identified
| Resource | Use described in review | Caveat in review |
|---|---|---|
| TRUE [3] | Factual-consistency evaluation across 11 datasets | Not citation-specific |
| TreatFact [14] | Long-document factuality evaluation | News/clinical focus |
| CiteME [11] | Citation attribution | Not full summary verification |
| CiteCheck [21] | Structured citation metadata verification | Emphasis on metadata corruption |
| SumPubMed [25] | Scientific source-summary pairs | No citation-drift labels |
| CS-PaperSum [26] | Scientific paper summaries; review reports 91,919 papers | Not a citation benchmark |
| MASSW [27] | AI-assisted scientific workflow data | Citation drift not primary label |
| PlainFact [20] | Biomedical factuality resource | Specialized domain |

**Decision:** Do not select a dataset based on size alone. First inspect its actual fields, access conditions, licenses, full-text availability, and whether it contains claim-reference-evidence annotations.

## 4. Candidate research gaps

### G1 — Claim-level citation verification benchmark
- **Review evidence:** p. 2, Section 3.4 says scientific-summary datasets do not automatically provide claim-level citation-drift labels; p. 5, Section 10 proposes linking claims, references, evidence spans, and support labels.
- **Reported limitation in review:** Existing resources lack the required citation-drift annotations.
- **Inference:** A curated, smaller benchmark could connect generated claims to cited papers and evidence spans.
- **Experimental question:** Can evidence-based claim-level verification distinguish supported, partially supported, unsupported, contradictory, and unverified citation relationships better than metadata-only or relevance-only checks?
- **Test evidence:** Annotated claim-reference pairs, evidence spans, support labels, inter-annotator agreement, per-class precision/recall/F1, and error analysis.
- **Feasibility:** Medium; annotation effort is the main cost.

### G2 — Multi-document citation support
- **Review evidence:** p. 4, Section 9.3 explains that literature reviews synthesize evidence across papers and that single-source entailment may be too restrictive.
- **Reported limitation in review:** Multi-document synthesis complicates support assessment.
- **Inference:** Aggregating evidence across cited papers may correctly validate claims that no single source supports alone.
- **Experimental question:** Does multi-source evidence aggregation improve support classification compared with evaluating each cited source independently?
- **Test evidence:** Human-annotated multi-source claims, evidence spans per source, macro-F1, class-wise precision/recall, and false-positive/negative analysis.
- **Feasibility:** Medium-low; multi-source ground truth is expensive.

### G3 — Retrieval failure versus unsupported citation
- **Review evidence:** p. 3, Section 4.3 identifies retrieval quality as a dependency; p. 4, Section 9.1 discusses PDF/OCR/metadata/database coverage problems.
- **Reported limitation in review:** Retrieval and extraction failures can cause false alarms.
- **Inference:** A verifier should distinguish unsupported claims from cases where evidence was not successfully retrieved.
- **Experimental question:** Does an uncertainty-aware three-state verifier reduce false positives compared with a binary supported/unsupported verifier?
- **Test evidence:** Controlled retrieval success, omission, irrelevant retrieval and partial-evidence conditions; false-positive rate, macro-F1, and correct abstention/insufficient-evidence rate.
- **Feasibility:** High for a controlled corpus.

### G4 — Long-document and cross-domain robustness
- **Review evidence:** pp. 2 and 4, Sections 3.4, 9.4 and 9.6.
- **Reported limitation in review:** Long-document factuality metrics can be unreliable; domain, citation convention and temporal variation matter.
- **Inference:** A pipeline tested on abstracts or one discipline may not generalize to full papers or other disciplines.
- **Experimental question:** How do document length and scientific domain affect evidence retrieval and citation-support classification?
- **Test evidence:** Abstract/full-text conditions, document lengths, domain labels, evidence localization, retrieval recall and verification F1.
- **Feasibility:** Medium; full-text access and parsing are bottlenecks.

### G5 — Citation stability versus correctness across repeated generations
- **Review evidence:** p. 3, Sections 4.5 and 5; p. 5, Section 10. The review gives Jaccard citation-set stability and recommends controlled repeated-generation protocols.
- **Reported limitation in review:** Repeated-generation stability is a separate reliability dimension that should be evaluated.
- **Inference:** Stability and correctness are distinct; a consistently wrong citation can have high stability.
- **Experimental question:** How are citation-set stability and claim-level correctness related under repeated generations and controlled prompt/sampling changes?
- **Test evidence:** Repeated outputs, fixed model/configuration records, citation-claim labels, Jaccard stability, correctness, and variation across conditions.
- **Feasibility:** High, assuming model access and a manageable source corpus.

## 5. Preliminary priority ranking
Scores are planning judgments, not measured findings. Scale: 1 (low) to 5 (high).

| Gap | Significance | Resource availability | Implementation feasibility | Priority rationale |
|---|---:|---:|---:|---|
| G5 Stability vs correctness | 4 | 4 | 5 | Controlled repeated generations and separate correctness labels are implementable on a small corpus. |
| G3 Retrieval failure vs unsupported | 5 | 4 | 4 | Strong practical value; controlled evidence omission can create test cases without requiring a huge dataset. |
| G1 Claim-level benchmark | 5 | 3 | 3 | Foundational and potentially reusable, but careful annotation and agreement checks take time. |
| G4 Long-document/cross-domain | 4 | 3 | 3 | Valuable robustness study; full-text access and domain coverage add cost. |
| G2 Multi-document synthesis | 5 | 2 | 2 | Important, but reliable multi-source annotations and attribution are difficult. |

**Current recommended implementation direction:** Start with G3 or G5 as a feasible controlled experiment. Build a small G1-style annotated subset to provide ground truth. Treat G2 and broad G4 evaluation as extensions unless resources permit.

## 6. Claims requiring primary-source verification
The following are **UNKNOWN until the original publications or official records are checked**. The descriptions below are claims made by the review, not independently confirmed findings.

1. [3] TRUE: exact dataset composition, eleven-dataset scope, and the stated complementarity of NLI and QA methods.
2. [5] FActScore: exact atomic-fact procedure, evidence source requirements, and reported limitations.
3. [6] AlignScore: exact evaluation scope and whether the review's generalization claim accurately reflects the paper.
4. [8] Reference Hallucination Score: domain, formula, validation protocol, and reported performance.
5. [9] Chelli et al.: exact comparison setup, reference ground truth, and precision/recall/F1/hallucination-rate results.
6. [11] CiteME: benchmark construction, task definition, and scope of citation attribution.
7. [14] TreatFact: dataset composition, domains, evaluator setup, and exact failure findings.
8. [15] OpenScholar: corpus size, retrieval/generation design, citation-grounding procedure, and publication metadata.
9. [16] SurveyGen/QUAL-SG: dataset relationship, quality dimensions, and citation-quality conclusions.
10. [17] Seetha Ram: definitions and formulas for stability, drift rate, drift entropy, fabrication rate, and willingness-to-cite; confirm whether the Jaccard expression in the review matches the source.
11. [18] Long-document stress testing: exact metrics, transformations, datasets, and scope of reported inconsistency.
12. [19] Prompt constraints: exact experimental conditions and reference-validation sources.
13. [20] PlainQAFact/PlainFact: distinction between metric and dataset, data access, and evaluation protocol.
14. [21] CiteCheck: benchmark size, corruption categories, retrieval method, and metadata-versus-support scope.
15. [22] SourceCheckup: exact support labels, medical QA setting, and evaluation results.
16. [23] RefLens: publication status, PDF parsing method, evidence reporting, and evaluation scale.
17. [24] SemanticCite: preprint status, full-text method, support categories, and validation evidence.
18. [25] SumPubMed: exact dataset size, fields, source-summary construction, and bibliographic record.
19. [26] CS-PaperSum: verify the reported 91,919-paper count, summary provenance, license, and availability.
20. [27] MASSW: verify dataset scope, annotations, and whether it can support citation-level experiments.
21. [28] Badalova and Mayr: verify preprint status and the review's characterization of metadata-based tool limitations.

Also verify all bibliographic metadata (author lists, titles, year, venue, page numbers, DOI/URL) against publisher or official repository records. Particular attention is warranted for recent 2025–2026 works, preprints, and references whose bibliographic entries continue across PDF pages [25]–[28].

## 7. What is not established
- No research gap above is claimed to be novel.
- No original publication has been independently checked as part of this review-only audit.
- No dataset has yet been downloaded or inspected.
- No code has been executed.
- No experiment or metric has been produced.
- No baseline has been reproduced.

## 8. Next actions
1. Obtain the original review bibliography/BibTeX if available.
2. Verify the highest-impact primary references, starting with [17], [21], [22], [23], [24], and the datasets [25]–[27].
3. Choose a feasible gap (recommended initial candidates: G3 or G5).
4. Inspect candidate dataset schemas, access, licenses, and full-text availability.
5. Define annotation guidelines and a small pilot sample.
6. Freeze the baseline, model/version, prompts, sampling parameters, and evaluation protocol before running experiments.
7. Record actual commands, configurations, raw outputs, and metrics; never enter planned results as completed results.

## Decision history
| Decision | Reason | Evidence | Next action |
|---|---|---|---|
| Treat citation drift as layered, not a single binary error | Review separates metadata, relevance, evidence support and stability | Review pp. 1–3 | Preserve separate labels and metrics |
| Keep stability separate from correctness | Set overlap does not establish semantic support | Review pp. 3 and 5; inference | Evaluate both on the same repeated outputs |
| Include an insufficient-evidence state | Retrieval failure can create false alarms | Review pp. 3–4 | Test controlled retrieval omissions |
| Do not claim novelty yet | Review-only analysis cannot establish field-wide novelty | No separate search performed | Conduct a targeted literature search after narrowing the question |


# 9. Direction C selected: claim-level citation verification benchmark

**User decision:** Option C — build a claim-level citation verification benchmark.

**Status:** Design stage only. No data collection, annotation, implementation, or experiment has been completed.

## 9.1 Refined research problem

The benchmark should evaluate the relationship between a claim in an AI-generated scientific literature summary and the publication(s) cited for that claim. It should not collapse this task into reference-existence checking or general claim truthfulness.

### Primary research question (proposed)
Can a claim-level citation verification framework reliably distinguish supported, partially supported, unsupported, and contradicted citation-claim relationships in AI-generated scientific literature summaries by linking generated claims to evidence passages in the cited publication(s), while separately identifying cases where evidence is insufficient?

### Secondary research questions (proposed)
- RQ2: Does evidence-based verification outperform bibliographic-validity-only verification?
- RQ3: Does atomic-claim decomposition improve detection of partially supported citations compared with sentence-level assessment?
- RQ4: How does retrieval failure affect citation-support classification?
- RQ5: Can the verifier distinguish insufficient evidence from contradictory evidence?

### Hypotheses (to be tested, not assumed true)
- H1: Evidence-based verification will identify unsupported citation relationships better than metadata-only checking.
- H2: Atomic-claim decomposition will improve identification of partial support.
- H3: Retrieval omissions will increase false unsupported classifications unless retrieval failure is represented separately.
- H4: An explicit insufficient-evidence state will reduce false accusations of citation drift.

## 9.2 Important refinement after preliminary external search

A preliminary web search found closely related work that narrows the defensible scope:

1. **CiteME (Press et al., NeurIPS 2024):** citation attribution from scientific text excerpts; it asks whether a model can identify the cited paper. Official source: https://proceedings.neurips.cc/paper_files/paper/2024/hash/0ef47f7b768e1a012e3d995ac8d8fac7-Abstract-Datasets_and_Benchmarks_Track.html
2. **CiteAudit (Yuan et al., 2026 preprint):** its abstract describes a multi-agent pipeline including claim extraction, evidence retrieval and passage matching. However, the inspected formal problem definition and benchmark labels focus on whether references are real/fake and metadata-consistent. It therefore overlaps with citation auditing, but is not identical to a benchmark whose primary unit is support of a generated summary claim by the publication cited for it. Source: https://arxiv.org/abs/2602.23452
3. **SciClaimEval (Ho et al., LREC 2026):** scientific claim verification with cross-modal evidence; reports 1,664 annotated samples from 180 papers across ML, NLP and medicine. Its task is not identical to generated-summary citation-to-source support. Official source: https://aclanthology.org/2026.lrec-1.864/
4. **CliVER (2024):** retrieval-augmented scientific claim verification using clinical-trial abstracts and evidence sentences. Its clinical setting and claim-verification framing are relevant; exact task overlap and transferability need full-paper review. Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC10919922/

**Research implication:** Do not claim that claim extraction, evidence retrieval, passage matching, or scientific claim verification is new. The narrower candidate task is citation-support relationship evaluation in AI-generated scientific literature summaries, including partial support and multi-source attribution. This is a scope refinement, not a novelty conclusion.

**Search status:** Preliminary targeted search only; not exhaustive. A systematic novelty search is still required before any novelty statement.

## 9.3 Proposed unit of analysis and annotation schema

Primary unit: a claim-citation relationship. For claims supported by multiple cited papers, preserve the group of cited sources and annotate both per-source contribution and collective support where feasible.

Recommended fields:
- `sample_id`, `summary_id`, `claim_id`
- `original_sentence` (retain full original context)
- `atomic_claim` (if decomposed)
- `citation_marker`
- `cited_paper_id` (DOI or stable identifier where available)
- `source_title`, `source_url`, `source_version_or_access_date`
- `source_text_location` (page/section/paragraph)
- `evidence_span`
- `support_label`
- `evidence_status`
- `annotator_id`, `adjudication_status`, `annotation_notes`

Do not discard the original sentence after atomic decomposition. Decomposition can remove qualifiers, scope, modality, or relationships between facts.

### Proposed labels
Use two distinct dimensions rather than one flat label.

**Evidence availability**
- `AVAILABLE`: relevant source content was retrieved and inspected.
- `INSUFFICIENT`: source/evidence could not be retrieved or the available text is insufficient to decide. Record the reason (e.g., inaccessible full text, retrieval miss, extraction failure, ambiguous source).

**Support judgment, only when evidence is adequate**
- `SUPPORTED`
- `PARTIALLY_SUPPORTED`
- `UNSUPPORTED`: evidence does not establish the claim; absence of support is not itself contradiction.
- `CONTRADICTED`: inspected evidence conflicts with the claim.

For multi-source claims, add a collective support judgment and retain source-level labels. Define annotation rules for whether several sources jointly support a synthesized claim. Do not infer collective support merely from topical relevance.

## 9.4 Proposed experimental conditions / baselines

All systems must be evaluated on the same held-out claim-citation examples and against the same adjudicated labels.

| ID | Condition | Purpose |
|---|---|---|
| B0 | Bibliographic metadata validation | Establish whether the cited work exists and metadata resolves |
| B1 | Semantic/topic relevance matching | Test whether the cited work is topically related |
| B2 | Single-source evidence verification | Test whether the cited publication supports the claim |
| B3 | Atomic-claim evidence verification | Test partial support at finer granularity |
| B4 | Multi-source evidence verification | Test collective support across cited publications |

B0 and B1 are deliberately limited baselines, not equivalent support verifiers. Report their results separately and explain their task limitations. B2 is the principal evidence-based baseline; B3/B4 are proposed extensions.

### Evaluation metrics
- Macro-F1 and per-class precision/recall/F1 for support labels.
- Confusion matrix.
- Evidence retrieval Recall@k (where a gold evidence passage exists).
- Evidence localization hit rate or span-level metric with a predeclared matching rule.
- Inter-annotator agreement (e.g., Cohen's kappa for two annotators on categorical labels; select a statistic appropriate to the annotation design).
- Coverage/abstention rate for `INSUFFICIENT`.
- False unsupported rate on examples where evidence was missed by retrieval.

Do not report accuracy alone. Predefine how `INSUFFICIENT` cases are handled in classification metrics.

## 9.5 Dataset construction plan

1. **Source corpus:** begin with one manageable discipline (computer science is a candidate, not a final decision). Record source provenance, access route, license/terms, document version, and full-text availability.
2. **Summary generation:** freeze the model identifier/version, prompt, date, sampling settings, and source set. Preserve raw outputs without post-hoc correction.
3. **Claim/citation extraction:** extract citation-bearing sentences, citation markers and claims. Manually audit a sample of extraction outputs.
4. **Evidence retrieval:** retrieve the cited publication and relevant passages. Preserve retrieval queries, ranking, top-k, raw passages and failures.
5. **Annotation:** annotate evidence availability, source-level support, collective support (if applicable), and evidence spans.
6. **Quality control:** use two independent annotators on a pilot/subset, calculate agreement, adjudicate disagreements, and revise guidelines before scaling.
7. **Dataset freeze:** version the data, annotation guide, source manifest, and split assignments.

### Pilot size (planning target only)
- 20–30 source papers.
- 50–100 candidate claim-citation pairs.
- Two annotators for at least a subset.
- Five comparison conditions (B0–B4).

These are proposed pilot targets, not a statistically justified final sample size and not completed data collection. Reassess after measuring class balance, annotation time, retrieval coverage and agreement.

### Leakage control
Split by source paper (or another source-level grouping), not by randomly splitting claim rows, so claims/evidence from the same paper do not leak across development and test sets. Keep a separate development set for threshold/prompt tuning. Freeze the test set before final evaluation.

## 9.6 Feasibility plan

Known environment from prior user-provided context: Mac M1, 8 GB RAM. Treat this as a constraint to confirm before implementation; do not assume current software installation state.

| Component | Candidate tool | Feasibility / caution |
|---|---|---|
| PDF extraction | PyMuPDF | High; inspect extraction errors |
| Metadata resolution | Crossref/OpenAlex | High; coverage and API limits need checking |
| Retrieval baseline | BM25 | High; good simple baseline |
| Semantic retrieval | Sentence Transformers | Medium; choose a small model compatible with memory |
| Claim extraction | Manual pilot or controlled LLM/API | High; log model, prompt, cost and raw output |
| NLI/LLM verification | Small NLI model or API verifier | Medium; calibrate and audit evaluator errors |
| Metrics | scikit-learn | High |
| Annotation | CSV/Spreadsheet with guidelines | High; human time is the main bottleneck |

Do not train a custom neural classifier until there are enough reliable labels. Begin with retrieval and transparent baseline rules/models.

## 9.7 Risks and mitigations
- **Ambiguous claims:** define claim segmentation rules and retain sentence context.
- **Citation marker resolution errors:** manually audit reference linking.
- **Full-text access failures:** mark `INSUFFICIENT`; do not label as unsupported.
- **Retrieval misses:** preserve retrieval logs and evaluate recall separately.
- **Annotation disagreement:** pilot guidelines, calculate agreement, adjudicate and report uncertainty.
- **Multi-source complexity:** treat as a separate condition; if annotation is too costly, defer it rather than weakening labels.
- **Data leakage:** split by source paper and freeze test data.
- **LLM evaluator bias:** compare with human labels and keep evidence spans visible.
- **Copyright/licensing:** verify each dataset and source-document license/terms before redistribution; consider releasing annotations/identifiers rather than copyrighted full text where required.

## 9.8 Updated next actions
1. Read the full CiteAudit paper and determine precisely which benchmark fields, labels, data, and code are available; distinguish its metadata-authenticity task from citation-support judgments.
2. Inspect CiteME, SciClaimEval and CliVER task definitions, annotation protocols, dataset access and licenses.
3. Search systematically for benchmarks specifically evaluating citation-support relationships in LLM-generated literature summaries, including work published after the reviewed paper.
4. Select a source corpus only after checking access, license, identifiers and full-text availability.
5. Draft an annotation guideline with positive, partial, unsupported, contradicted and insufficient-evidence examples.
6. Run a small pilot and measure annotation time, retrieval coverage, class balance and inter-annotator agreement.
7. Revise the research question and sample-size plan based on pilot evidence.
8. Freeze baselines, prompts, model versions, data splits and metrics before the main evaluation.

## 9.9 Updated decision history
| Decision | Reason | Evidence | Next action |
|---|---|---|---|
| User selected Option C | Explicit user choice | Conversation decision | Develop benchmark design |
| Refine benchmark around citation-support relationships in generated summaries | Existing work covers attribution, reference authenticity and general scientific claim verification | CiteME (2024), CiteAudit (2026 preprint), SciClaimEval (LREC 2026), CliVER (2024); see URLs above | Complete full related-work comparison |
| Use two annotation dimensions: evidence availability and support judgment | Retrieval failure must not be confused with lack of support or contradiction | Review pp. 3–4; proposed design inference | Pilot annotation guidelines |
| Preserve sentence context alongside atomic claims | Decomposition may remove qualifiers or change meaning | Review p. 4, Section 9.2; proposed design inference | Audit claim segmentation |
| Split by source paper | Reduce evidence/source leakage between development and test | Experimental-design safeguard | Define source-level split manifest |
| Pilot before fixing final dataset size | Annotation cost, class balance and retrieval coverage are currently unknown | No pilot data yet | Collect pilot only after source/license checks |

## 10. Current status snapshot
- Literature review inspected: **VERIFIED**
- Option C selected by user: **VERIFIED**
- Preliminary external related-work search performed: **VERIFIED**
- Final novelty established: **NO**
- Research question and hypotheses: **PROPOSED**
- Dataset selected and downloaded: **NO**
- Annotation guidelines validated: **NO**
- Human annotations collected: **NO**
- Baselines implemented: **NO**
- Experiments run: **NO**
- Metrics/results available: **NO**
