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


## 11. Feasibility decisions confirmed by user (2026-11-17)

- **Domain:** Computer Science.
- **Source access:** Both abstracts and full text are available.
- **Annotation resources:** Two annotators are available.

**Status:** These are user-confirmed project constraints. They do not yet establish that every selected paper is legally reusable, machine-readable, or accessible in full text.

### Updated plan decisions
1. Use Computer Science as the initial domain; do not claim cross-domain generalization from this pilot.
2. Prefer papers with both an accessible abstract and accessible full text. Record exceptions and exclude or separately flag sources without adequate text.
3. Use two independent annotators for the pilot. Both should label the same pilot items before discussion/adjudication.
4. Exploit abstract/full-text availability as a controlled evidence condition: assess whether a claim can be supported from the abstract alone and whether additional full-text evidence changes the decision. Keep the claim-support ground truth tied to the full source, not merely the abstract.
5. Start with a pilot of approximately 20–30 Computer Science papers and 50–100 claim-citation pairs. These remain planning targets, not statistically justified final sample sizes.
6. Freeze an annotation guide and pilot sampling rules before annotators begin. Do not change labels silently mid-pilot; version the guide and document revisions.

### New immediate deliverable
Create `annotation_guideline_pilot_spec.md` with:
- unit of annotation and inclusion/exclusion rules;
- evidence availability and support labels;
- decision rules and difficult examples;
- abstract-only versus full-text evidence procedure;
- two-annotator workflow and adjudication;
- pilot sampling and data schema;
- quality checks and stop/go criteria.

### Updated status
- Domain selected: **VERIFIED (user-confirmed)**
- Abstract and full-text access available in principle: **VERIFIED (user-confirmed; individual document access still to be checked)**
- Two annotators available: **VERIFIED (user-confirmed)**
- Individual source licenses/accessibility checked: **NO**
- Annotation guideline drafted: **YES — draft; requires pilot validation**
- Pilot items collected: **NO**
- Human labels collected: **NO**
- Inter-annotator agreement measured: **NO**
- Final sample size justified: **NO**


# 12. Literature-to-experiment method shortlist (2026-11-17)

The user asked for three implementable published methods from the review. The shortlist below uses references already present in the review:
- [5] FActScore
- [6] AlignScore
- [21] CiteCheck

The user wrote `[GAPS]` as a placeholder rather than supplying a separate gap list. Accordingly, this mapping uses the gaps recorded in Sections 9–10 of this log and the original review.

## 12.1 Method 1 — FActScore [5]
**Original paper:** Sewon Min et al. (2023), *FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation*, EMNLP 2023. DOI: 10.18653/v1/2023.emnlp-main.741.  
**Review mapping:** Section 3.1 and Table 1; atomic facts and evidence-supported factual precision.

- **Algorithm:** Decompose a long generation into atomic facts; retrieve/consult a knowledge source for each fact; estimate the proportion supported by evidence. The original task is factual precision of long-form generation, not citation-to-cited-paper verification.
- **Original evaluation setting/data:** Human-evaluated people biographies generated by InstructGPT, ChatGPT and PerplexityAI; the official package distributes associated data/annotations and a knowledge source. The input format uses a topic corresponding to a Wikipedia title.
- **Code access:** **VERIFIED** — public official repository https://github.com/shmsw25/FActScore and pip package are documented by the repository.
- **Model access:** **VERIFIED** — the package documents a ChatGPT/API path and an Inst-LLAMA/LLAMA 7B path. LLAMA weights must be obtained separately; they are not bundled as universally accessible weights. ChatGPT use requires an API key. No claim is made that a current API model reproduces the original model/version.
- **Evaluation:** FActScore is the percentage/proportion of atomic facts supported by a reliable knowledge source; the paper reports human evaluation and an automated estimator. For our benchmark, additionally report atomic-claim support precision/recall/F1 against adjudicated human labels.
- **Known limitations for our task:** Original knowledge source and task are biography/Wikipedia-oriented; its topic-entity and retrieval assumptions do not map directly to arbitrary CS papers. Fact-level support is not equivalent to whether the specific cited paper supports the claim. Atomic decomposition and retrieval can introduce errors. Do not treat FActScore output as citation correctness.
- **Compute burden:** Medium–high if using API-based fact generation/verification and retrieval; low local training burden if using released components. API cost, rate limits, source retrieval and caching matter. The repository estimates about USD 1 per 100 sentences for its documented API setup; this is a repository estimate, not a current quote.
- **Use in our study:** Adapt the atomic-fact decomposition/evidence-precision idea to the cited paper as the evidence source; preserve citation marker and source ID. This is an adaptation, not a faithful reproduction of the original task.

## 12.2 Method 2 — AlignScore [6]
**Original paper:** Yuheng Zha, Yichi Yang, Ruichen Li and Zhiting Hu (2023), *AlignScore: Evaluating Factual Consistency with a Unified Alignment Function*, ACL 2023. DOI: 10.18653/v1/2023.acl-long.634.  
**Review mapping:** Section 3.1 and Table 1; alignment-based factual consistency.

- **Algorithm:** Encode a context and a claim; split context into roughly 350-token chunks and claim into sentences; score chunk-sentence alignment with a learned RoBERTa-based function; aggregate the maximum alignment per claim sentence into an example score. The repository documents `nli_sp`, `nli`, `bin_sp`, and `bin` modes.
- **Original training/evaluation resources:** Trained on 4.7 million examples drawn from seven task families (NLI, QA, paraphrasing, fact verification, information retrieval, semantic similarity and summarization). Evaluated on 22 datasets, including SummaC, TRUE and other factual-consistency datasets. It is not a citation-drift benchmark.
- **Code access:** **VERIFIED** — public repository https://github.com/yuh-zha/AlignScore.
- **Model/weight access:** **VERIFIED** — repository documents AlignScore-base (RoBERTa-base, 125M parameters) and AlignScore-large (RoBERTa-large, 355M parameters) checkpoints. Weights are available via the linked Hugging Face checkpoint files. This verifies public links/documentation, not that weights have been downloaded or run in the user's environment.
- **Evaluation:** Original paper reports AUC-ROC on SummaC and TRUE and Spearman correlation with human judgments on several other datasets. For our benchmark, evaluate score discrimination against human support labels using AUROC where appropriate, and thresholded per-class precision/recall/F1 after threshold calibration on development data.
- **Known limitations for our task:** A high alignment score is not proof that the cited paper is the correct source or that a claim is supported at the required scientific specificity. It can reward topical/semantic overlap. The original score is a scalar and does not inherently provide the four human support categories or calibrated abstention. Long papers require chunking/retrieval; aggregation and retrieval choices can change results.
- **Compute burden:** Medium for inference, low relative to training because released checkpoints can be used. Base is preferable to large for a constrained local machine; batch size should be reduced. Exact Apple Silicon/MPS/CPU compatibility, memory footprint and runtime remain **UNKNOWN until tested**. Full retraining is not recommended for the pilot.
- **Use in our study:** Principal semantic evidence-alignment baseline. Input context should be the cited paper's abstract, full text or retrieved passage; test these conditions separately.

## 12.3 Method 3 — CiteCheck [21]
**Original paper:** Khashayar Khajavi, Shaghayegh Sadeghi, Rise Adhikari and Alexander Tessier (2026), *CiteCheck: Retrieval-Grounded Detection of LLM Citation Hallucinations in Scientific Text*. The review cites the arXiv version arXiv:2605.27700. A later ACL Anthology record lists the paper in GroundLM 2026, pages 779–795: https://aclanthology.org/2026.groundlm-1.58/. Update the review bibliography from the preprint-only description if confirmed against the proceedings PDF.
**Review mapping:** Section 3.5 and Table 3; citation metadata corruption and retrieval-grounded verification.

- **Algorithm:** Parse citation text; retrieve candidate scholarly records through an external-source cascade (arXiv, Crossref, Semantic Scholar, OpenAlex, with web fallback); compare candidate metadata using a structured-output LLM verifier; optionally use a second-pass reviewer for weak matches; threshold the score into Exact/Minor/Major (repository labels: exact_match/minor_hallucination/major_hallucination).
- **Original benchmark:** 982 physics citations from 42 collections, with controlled metadata corruptions; three classes: valid, minor hallucination, major hallucination. The repository describes nine scientific topics and deterministic collection-level splits.
- **Code access:** **VERIFIED** — public companion repository https://github.com/FirstPrinciplesLabs/citecheck. The README documents a default command intended to reproduce the headline evaluation. Repository source code states MIT license.
- **Dataset access:** **VERIFIED at repository level** — dataset files are present in the public repository. **UNKNOWN** — exact dataset redistribution terms must be checked in `dataset/SCHEMA.md` before reuse or redistribution.
- **Model access:** **VERIFIED** — implementation uses external LLM API providers (OpenAI, Anthropic and/or Google) and scholarly APIs; `.env.example` and README describe API-key configuration. No local verifier weights are provided/required by the documented default route. Provider availability, model IDs, pricing and current API compatibility must be checked before running.
- **Evaluation:** Original paper reports 88.7 macro-F1 and 88.9% accuracy on its held-out benchmark. These are the paper's reported numbers, not reproduced by us. The repository includes evaluation, splits, threshold tuning and metrics.
- **Known limitations for our task:** It verifies reference authenticity and metadata fidelity, not whether the cited paper supports the generated scientific claim. Its three labels cannot be substituted for supported/partial/unsupported/contradicted. Its physics benchmark may not transfer directly to computer-science literature summaries. API verifier judgments and scholarly retrieval coverage can fail.
- **Compute burden:** Low local GPU burden; medium operational/API burden due to external scholarly services and LLM calls. Internet access, API keys, rate limits, request costs and deterministic logging are required.
- **Use in our study:** Metadata-validity baseline/control only. Run separately from claim-support classifiers; do not compare its three-class metadata F1 directly with claim-support macro-F1 as if they were the same task.

## 12.4 Literature-to-experiment mapping table

| Review reference/method | Reproduced component | Dataset/source context | Code/weights status | Main metric | Role in our experiment |
|---|---|---|---|---|---|
| [5] FActScore | Atomic fact decomposition + evidence-based fact precision | Original biographies/Wikipedia; adapt cited CS paper passages | Code verified; ChatGPT API route documented; LLAMA weights separate | FActScore; our human-label macro-F1/precision/recall | Fine-grained evidence baseline |
| [6] AlignScore | Context-claim alignment scoring and chunk/sentence aggregation | Original 22 factuality datasets; adapt cited CS paper abstract/full text/passages | Code and base/large checkpoints verified as publicly documented | AUROC/Spearman originally; our AUROC and calibrated class metrics | Principal semantic support baseline |
| [21] CiteCheck | Citation parsing, scholarly lookup and metadata verification | Original 982-citation physics benchmark; use only as metadata control | Code and benchmark files public; LLM/API credentials required; dataset license details pending | Macro-F1 and accuracy originally | Bibliographic-validity baseline, not support verifier |

## 12.5 Three study designs compared

### Study A — Reproduction plus extension
- **Smallest working baseline:** Reproduce AlignScore inference using its released base checkpoint on a small, documented factuality sample; separately reproduce CiteCheck's default evaluation on its bundled benchmark if API access is available. Then evaluate/adapt the methods on the new annotated CS claim-citation set.
- **Testable question:** Do existing factuality/alignment and citation-metadata methods retain useful performance when moved to claim-to-cited-paper support judgments?
- **Extension:** Evaluate AlignScore on cited-paper evidence and FActScore-style atomic claims; report CiteCheck metadata validity as a separate layer.
- **Resource burden:** High relative to a short project: multiple environments, API access, reproducing original settings, data mapping and new annotations.
- **Evidence required:** Original benchmark outputs and configurations; downloaded checkpoint hashes; API/model versions; exact splits; original-metric reproduction table; human-labeled CS benchmark; separate results for metadata and support tasks.
- **Risk:** A reproduction may fail due to API/model drift or old dependencies. A failed reproduction must be reported, not silently replaced with a modified run.

### Study B — Controlled comparison
- **Smallest working baseline:** On one frozen pilot set of claim-citation pairs, compare (1) metadata validity (CiteCheck or a simpler DOI/metadata lookup), (2) AlignScore on abstract/full-text/evidence passages, and (3) FActScore-style atomic decomposition/evidence support. Keep metadata and support labels separate.
- **Testable question:** On the same human-annotated CS claim-citation examples, which existing signal best discriminates supported, partially supported, unsupported and contradicted relationships? Does evidence context (abstract vs full text vs gold passage) change AlignScore performance?
- **Resource burden:** Medium. No model training required; needs annotation, source access, one released checkpoint and possibly API calls for FActScore/CiteCheck.
- **Evidence required:** Frozen data/splits; annotation guide; two annotators' raw labels and agreement; method versions/configs; thresholds selected only on development data; confusion matrices; macro-F1/per-class metrics; AUROC where scores apply; retrieval coverage; runtime/API cost.
- **Risk:** The three systems do not solve identical tasks. Compare only on shared support labels where appropriate; report CiteCheck as metadata-only control, not a direct competitor for support classification.

### Study C — Targeted modification
- **Smallest working baseline:** Use AlignScore unchanged with cited-paper context and claim input.
- **Targeted modification:** Replace whole-document context with top-k retrieved passages from the cited paper (BM25 first); optionally compare against the gold evidence passage as an oracle upper-bound condition. Do not add a new neural architecture.
- **Testable question:** Does passage-level evidence localization improve support classification over feeding the whole cited paper/abstract to a fixed AlignScore checkpoint, and how much of the gain depends on retrieval quality?
- **Resource burden:** Medium. Requires chunking/indexing and BM25, but no model training. Oracle evidence annotations are required for the upper-bound comparison.
- **Evidence required:** Same examples and labels; fixed AlignScore checkpoint; fixed chunking and k; retrieval Recall@k; score distributions; thresholded macro-F1/per-class metrics; error analysis separating retrieval misses from verifier errors; runtime.
- **Risk:** The result may be driven by passage selection or leakage. Retrieval must use only source material available to the verifier; gold passages must be clearly marked as oracle analysis, not a deployable system.

## 12.6 Recommended minimum viable experiment

**Recommendation: Study B — controlled comparison, with a deliberately small scope.**

Why:
- It answers a clean, testable question without requiring model training.
- It uses two existing released methods with different roles (AlignScore for claim-evidence alignment; CiteCheck for reference metadata validity) and a FActScore-inspired atomic-fact baseline.
- It can be run on the user's confirmed CS corpus and two-annotator setup.
- It avoids claiming a new architecture.
- It makes it possible to expose the key distinction: a valid reference may still fail to support its attached claim.

### Minimum viable protocol
1. Select 20–30 CS papers with accessible abstracts and full text, verifying licenses/access individually.
2. Generate or collect a small frozen set of summaries and preserve their raw outputs and generation metadata.
3. Annotate 50–100 claim-citation pairs with two annotators; preserve independent labels and adjudication.
4. Freeze source-level development/test partitions. If the sample is too small for a stable held-out test, call it a pilot and avoid generalization claims.
5. Run:
   - DOI/metadata existence and metadata consistency check (CiteCheck only if its API requirements and dataset terms are acceptable);
   - AlignScore-base on abstract, full-text/chunked context, and annotated evidence span conditions;
   - FActScore-style atomic claim decomposition and evidence scoring, using the cited paper as evidence source rather than Wikipedia.
6. Report support labels separately from reference-validity labels.
7. Report macro-F1, per-class precision/recall, confusion matrix, AUROC for continuous scores where valid, inter-annotator agreement, retrieval coverage, abstention/insufficient-evidence rate, runtime and API cost.
8. Perform qualitative error analysis on partial claims, missing evidence, retrieval misses, contradictory passages and multi-source claims.

**Do not train a custom classifier in the MVP.** Do not claim benchmark novelty until a separate systematic search has been completed.

## 12.7 What must be personally verified before coding

### Papers and protocols
- Read the full FActScore, AlignScore and CiteCheck papers, not only abstracts/README files.
- Confirm that our descriptions match the exact original algorithms, thresholds, input formats and evaluation procedures.
- For CiteCheck, update reference [21] from the arXiv-only citation if the GroundLM proceedings version is the version being cited.
- Confirm whether any code changes after the paper materially alter the reported configuration.

### Access and licenses
- Clone the exact repositories and record commit hashes.
- Confirm FActScore data/knowledge-source download works and inspect its license/terms.
- Confirm AlignScore checkpoint files download and record hashes.
- Confirm CiteCheck dataset schema and licensing terms; MIT code license does not automatically establish dataset license.
- Check API keys, provider model availability, pricing, rate limits and data-use terms before sending research text to an external API.

### Environment
- Test package installation in a clean environment.
- Confirm Python/PyTorch/spaCy versions and dependency conflicts.
- Test AlignScore-base inference on the actual Mac M1/8 GB machine with batch size 1 or 2; record peak memory/runtime. CPU/MPS support is not assumed.
- Confirm whether API-based FActScore/CiteCheck runs are affordable and cache outputs.

### Dataset and annotations
- Verify full-text access and permitted reuse for each CS paper.
- Verify DOI/title/author/year resolution.
- Freeze the summary prompt/model/version/parameters and preserve raw generations.
- Have both annotators independently label a calibration subset.
- Calculate agreement and revise the guide before scaling.
- Confirm source-level splits prevent paper/evidence leakage.
- Decide how to handle multi-source claims and inaccessible sources before evaluating.

### Evaluation
- Predefine the primary label set and metric calculation.
- Tune thresholds on development data only.
- Do not compare CiteCheck metadata labels directly with semantic support labels.
- Report class distribution and confidence intervals where sample size supports them.
- Preserve raw predictions, model outputs, logs and failed cases.

## 12.8 Current status
- Three method shortlist selected from review: **PROPOSED**
- Official code links verified for FActScore, AlignScore and CiteCheck: **VERIFIED at repository/documentation level**
- Public checkpoint links verified for AlignScore: **VERIFIED at documentation level**
- FActScore ChatGPT/API and separate LLAMA-weight routes documented: **VERIFIED**
- CiteCheck API-based verifier and public benchmark files documented: **VERIFIED**
- Dataset licenses fully checked: **UNKNOWN**
- Packages installed or methods run on user's Mac: **NO**
- Original metrics reproduced: **NO**
- New benchmark data annotated: **NO**
- Minimum viable Study B selected: **RECOMMENDED, pending user confirmation**


## 13. User-requested method-to-experiment mapping (2026-11-17)

### Selected published methods from the review
The user wrote `[GAPS]` as a placeholder rather than supplying a separate gap list. The mapping therefore uses the five gaps already recorded in this log and the original review.

1. **FActScore [5] — Min et al. (EMNLP 2023), DOI 10.18653/v1/2023.emnlp-main.741.**
   - Method: atomic-fact decomposition, evidence retrieval, factual precision over supported atomic facts.
   - Original setting: long-form people biographies, Wikipedia-oriented knowledge source, human annotations and automated evaluation.
   - Code: official public implementation and pip package verified at https://github.com/shmsw25/FActScore.
   - Model access: documented ChatGPT/API route; separate Inst-LLAMA route requires separately obtained LLAMA 7B weights. No claim that original model versions remain accessible.
   - Metrics: FActScore/factual precision and human evaluation. For our task add macro-F1 and per-class metrics against human labels.
   - Limitation: original task is not citation-specific; factual truth is not proof that a particular cited paper supports the fact; original topic/Wikipedia assumptions need adaptation.
   - Compute: medium-high operational/API and retrieval burden; no custom training needed for an initial adaptation. Repository's historical API-cost estimate is not a current quote.
   - Intended role: atomic-claim evidence baseline/adaptation.

2. **AlignScore [6] — Zha, Yang, Li and Hu (ACL 2023), DOI 10.18653/v1/2023.acl-long.634.**
   - Method: context/claim alignment; context chunking (roughly 350 tokens), claim sentence splitting, chunk-sentence scoring and aggregation.
   - Original training/evaluation: 4.7M examples across seven task families; 22 factuality evaluation datasets including TRUE and SummaC.
   - Code: public official repository verified at https://github.com/yuh-zha/AlignScore.
   - Weights: public AlignScore-base (RoBERTa-base, 125M) and AlignScore-large (RoBERTa-large, 355M) checkpoints documented.
   - Metrics: original AUC-ROC on SummaC/TRUE and Spearman correlation on other datasets; for our task use AUROC where appropriate and thresholded macro-F1/per-class precision/recall.
   - Limitation: alignment is not proof of citation correctness; scalar output does not inherently provide the four support labels; long-context chunking/retrieval can affect scores.
   - Compute: medium inference burden; no retraining recommended. Apple Silicon/CPU/MPS memory and runtime are UNKNOWN until tested on user's machine.
   - Intended role: principal semantic evidence-alignment baseline.

3. **CiteCheck [21] — Khajavi, Sadeghi, Adhikari and Tessier (2026), arXiv:2605.27700; later GroundLM 2026 proceedings record at https://aclanthology.org/2026.groundlm-1.58/.**
   - Method: citation parsing; scholarly candidate retrieval (arXiv, Crossref, Semantic Scholar, OpenAlex, web fallback); structured LLM metadata comparison; optional reviewer; thresholded Exact/Minor/Major labels.
   - Original benchmark: 982 physics citations, 42 collections, nine topics, controlled metadata corruptions.
   - Code: public companion repository verified at https://github.com/FirstPrinciplesLabs/citecheck; source-code MIT license documented.
   - Dataset: files are present in repository; redistribution terms still need inspection in dataset/SCHEMA.md.
   - Model access: API-based LLM verifier and scholarly APIs documented; no local verifier weights required by default route. Provider availability, model ID, price and terms need checking.
   - Metrics: paper reports 88.7 macro-F1 and 88.9% accuracy on its held-out benchmark. These are published, not reproduced results.
   - Limitation: verifies reference authenticity/metadata, not claim-to-source support; keep it as a metadata-validity control and do not compare its labels directly to support labels.
   - Compute: low local GPU requirement; medium API/network operational burden.
   - Intended role: bibliographic-validity baseline only.

### Literature-to-experiment mapping
| Method | Reproduced component | Adaptation | Role |
|---|---|---|---|
| FActScore [5] | Atomic facts and evidence-based precision | Use cited CS paper as evidence rather than the original Wikipedia-oriented setting | Fine-grained evidence baseline |
| AlignScore [6] | Context-claim alignment | Abstract, full-text chunk or retrieved passage as context | Main semantic support baseline |
| CiteCheck [21] | Citation parsing and metadata verification | Apply to CS summary references | Separate reference-validity control |

### Study comparison

**A — Reproduction plus extension**
- Smallest baseline: reproduce AlignScore-base inference on a documented factuality sample; reproduce CiteCheck's default bundled evaluation if API access permits; then evaluate on the new CS set.
- Question: Do existing factuality and citation-metadata methods retain useful performance on claim-to-cited-paper support?
- Burden: high; multiple original environments, APIs, benchmarks and reproduction records.
- Evidence: original configurations, raw runs, checkpoint hashes, model/API versions, original-versus-reproduced metrics, human labels, new test predictions and error analysis.
- Risk: implementation drift/API changes can make exact reproduction difficult.

**B — Controlled comparison**
- Smallest baseline: one frozen pilot of 50–100 claim-citation pairs; metadata validity (CiteCheck or DOI lookup), AlignScore-base, FActScore-inspired atomic-fact evidence evaluation, and human labels.
- Question: On the same human-annotated CS examples, how well do factuality methods distinguish supported, partially supported, unsupported and contradicted citation relationships? Does abstract/full-text/evidence context change performance?
- Burden: medium; no model training, but annotation and evidence preparation required.
- Evidence: two annotators' raw labels, agreement, adjudication, frozen source-level splits, method configs, dev-only threshold calibration, macro-F1, per-class metrics, confusion matrices, AUROC for continuous scores, retrieval coverage, runtime/API costs.
- Risk: methods do not have identical output tasks. Keep CiteCheck's metadata labels separate from support classification.

**C — Targeted modification**
- Smallest baseline: AlignScore-base on claim versus cited-paper context.
- Modification: replace full-document context with BM25 top-k retrieved passages; optionally compare with human gold passage as an oracle diagnostic.
- Question: Does passage-level evidence localization improve claim-support classification over abstract/full-text context, and how much depends on retrieval quality?
- Burden: medium; chunking, BM25, evidence annotations; no model training.
- Evidence: fixed examples and checkpoint, chunking/k, Recall@k, score distributions, macro-F1, per-class recall, error analysis separating retrieval misses from verifier errors, runtime.
- Risk: gains may reflect retrieval quality or leakage; oracle evidence must not be presented as deployable.

### Recommended minimum viable experiment
**Study B — Controlled comparison.** This is recommended because it answers a focused question with no custom model training and uses the two-annotator CS benchmark already planned.

Minimum protocol:
1. Select 20–30 CS source papers with verified full-text access and reuse terms.
2. Freeze a small set of generated summaries and preserve prompts/model/configurations.
3. Annotate 50–100 claim-citation pairs with two independent annotators.
4. Keep source-paper groups intact across development/test splits; if too small for stable test estimates, report a pilot rather than generalizable results.
5. Run metadata lookup/CiteCheck as a separate validity control.
6. Run AlignScore-base on abstract, full-text/chunked context and evidence-span conditions.
7. Run a FActScore-inspired atomic-fact/evidence procedure using the cited source as evidence; clearly label this as an adaptation, not a faithful reproduction of the original biography/Wikipedia task.
8. Report macro-F1, per-class precision/recall, confusion matrix, AUROC where valid, agreement, retrieval coverage, abstention, runtime and API cost.
9. Do not train a custom classifier or propose a new architecture in this MVP.

### Personal verification checklist before coding
- Read the full original papers and verify algorithms, inputs, thresholds, splits and original metrics.
- Clone repositories and record exact commit hashes.
- Check FActScore data/knowledge-source download and license.
- Download AlignScore-base; record checksum and test batch 1–2 on actual M1/8GB environment; CPU/MPS support and memory remain unverified.
- Inspect CiteCheck dataset/SCHEMA.md licensing; MIT code license does not imply dataset redistribution permission.
- Verify current API model IDs, prices, rate limits, data-use terms and access.
- Confirm full-text access and reuse terms for each CS source paper.
- Freeze generation model, prompt, parameters, raw outputs and source versions.
- Complete two-annotator calibration and agreement before scaling.
- Predefine label handling, thresholds, source-level splits and metric calculations.
- Do not compare CiteCheck metadata labels directly with semantic support labels.
- Preserve failed retrievals, raw predictions, API responses and logs.

### Current decision
**Study B is RECOMMENDED, not yet executed or user-confirmed.** No packages have been installed, code run, datasets annotated, or original results reproduced.
