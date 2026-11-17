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
