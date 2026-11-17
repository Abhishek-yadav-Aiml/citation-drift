# Annotation Guideline and Pilot Dataset Specification

**Project:** Detecting Citation Drift in AI-Generated Literature Summaries  
**Version:** 0.1 — draft for pilot  
**Date:** 2026-11-17  
**Domain:** Computer Science  
**Annotators:** Two independent annotators  
**Source condition:** Abstract and full text available in principle; verify access and reuse terms for every item.

> This is a proposed annotation protocol. It has not yet been validated on real examples. Revise it after a small calibration exercise and record every change.

## 1. Annotation objective

For each claim in an AI-generated scientific literature summary, determine whether the publication(s) cited alongside that claim provide evidence for the claim.

The task is **citation-to-claim support verification**, not just:
- checking whether a reference exists;
- checking whether a paper is topically relevant;
- deciding whether a claim is generally true based on annotator background knowledge.

Annotators must judge the relationship between the claim and the cited source content supplied in the annotation record.

## 2. Unit of annotation

Primary unit: one **claim–citation relationship**.

A sentence containing two separable factual claims may produce two claim records. If one claim cites two or more papers, create:
1. one source-level record for each claim–paper pair; and
2. one group-level record for the complete cited source set, where the claim appears to rely on the papers collectively.

Always preserve the original sentence and its surrounding context. Do not retain only the decomposed atomic claim.

### Claim segmentation rules
- Split a sentence when it contains independently verifiable propositions.
- Preserve qualifiers, uncertainty, negation, population, time period, comparison, and numerical conditions.
- Do not split a proposition if doing so changes its meaning or removes a necessary relationship.
- Keep a record of the original sentence and the exact text span used for each atomic claim.
- If segmentation is genuinely ambiguous, flag `SEGMENTATION_UNCERTAIN` and explain why; do not silently force a split.

## 3. Evidence availability labels

Choose one:

| Label | Operational definition |
|---|---|
| `AVAILABLE` | The cited source was identified and sufficient source text was inspected to make a support judgment. |
| `INSUFFICIENT_ACCESS` | The source or relevant full text could not be accessed, or only incomplete text was available. |
| `INSUFFICIENT_RETRIEVAL` | The source is available, but the retrieval/extraction process did not locate adequate passages. |
| `INSUFFICIENT_CONTEXT` | The claim or source context is too ambiguous to decide reliably. |

Do not assign `UNSUPPORTED` or `CONTRADICTED` when evidence availability is one of the insufficient states.

## 4. Support judgment labels

Assign a support label only when evidence availability is `AVAILABLE`.

| Label | Operational definition |
|---|---|
| `SUPPORTED` | The inspected cited source explicitly or clearly supports all material parts of the claim at the stated level of specificity. |
| `PARTIALLY_SUPPORTED` | The source supports at least one material component, but another material component, qualifier, comparison, causal relation, number, or scope is not supported. |
| `NOT_SUPPORTED_IN_INSPECTED_SOURCE` | After inspecting the relevant source content, no adequate support for the claim is found. This is a source-relative judgment, not proof that the claim is false or unsupported by all literature. |
| `CONTRADICTED` | The inspected source contains evidence that directly conflicts with a material part of the claim. Mere absence of a statement is not contradiction. |

### Important distinctions
- **Not supported is not contradicted.** Silence or omission is not counter-evidence.
- **Not retrieved is not not supported.** Retrieval failure belongs in evidence availability.
- **Topical relevance is not support.** A paper can discuss the same topic without establishing the particular claim.
- **A real DOI is not support.** Bibliographic validity and claim support are separate dimensions.
- **A citation can be partially correct.** Do not force a binary label if the source supports only part of the statement.
- **Do not use outside knowledge to fill gaps.** Annotate the cited source evidence. If external evidence is needed to resolve a claim's truth, that is a different task.

## 5. Abstract-only versus full-text procedure

Because the project has access to abstracts and full text, use a two-pass protocol.

### Pass A — Abstract-only
1. Give the annotator the generated claim, citation metadata, and the cited paper's abstract.
2. Ask whether the abstract alone provides sufficient evidence.
3. Record `ABSTRACT_SUPPORT_LABEL` using the same support labels, or `INSUFFICIENT_ABSTRACT` if the abstract does not contain enough information to decide.
4. Record the exact abstract sentence(s) used.

### Pass B — Full text
1. Provide the full text (or the accessible relevant sections) of the same cited paper.
2. Ask the annotator to make a fresh full-text judgment without being forced to preserve the abstract-only decision.
3. Record `FULLTEXT_SUPPORT_LABEL` and exact page/section/paragraph or other stable location.
4. Record whether full-text evidence changed the decision and why.

**Ground-truth rule:** The principal citation-support label for the benchmark should be based on the full source when adequate full text is available. The abstract-only label is a separate evidence-condition result, not a substitute for full-text ground truth.

Do not claim the full text was comprehensively reviewed if only selected sections were inspected. Record the inspected scope.

## 6. Multi-citation and multi-document claims

For a claim with several citations:
- annotate each claim–paper pair separately;
- then annotate the cited set collectively if the summary plausibly presents the papers as joint evidence;
- record which source supports which claim component;
- use `PARTIALLY_SUPPORTED` when only some components are supported;
- do not infer collective support simply because several papers are topically related.

For the first pilot, multi-source examples may be included but should be flagged as a separate subset. If annotation consistency is poor, defer collective-support evaluation to a later study rather than merging uncertain labels into the main single-source task.

## 7. Required annotation record

Recommended CSV columns:

```text
sample_id
summary_id
source_paper_id
source_title
source_doi
source_url
source_version_or_access_date
summary_model
summary_model_version
generation_prompt_id
generation_parameters
original_sentence
claim_id
atomic_claim
claim_span_start
claim_span_end
citation_marker
cited_paper_id
abstract_text
abstract_evidence_span
abstract_support_label
fulltext_access_status
fulltext_inspected_scope
fulltext_evidence_span
evidence_page
evidence_section
evidence_availability
fulltext_support_label
multi_source_group_id
annotator_id
annotation_notes
adjudication_label
adjudication_notes
annotation_guide_version
```

Keep raw summary output, source files/identifiers, retrieval logs, and annotation data as separate versioned artifacts. Avoid putting copyrighted full-text content into a dataset intended for redistribution unless the license/terms permit it.

## 8. Inclusion and exclusion rules

### Include
- Computer Science research papers with stable bibliographic metadata.
- Papers with an accessible abstract and accessible full text for the primary pilot where possible.
- AI-generated literature-summary outputs with identifiable citation markers.
- Claims that can be stated as propositions and linked to one or more citations.
- Sources for which the cited publication can be resolved with reasonable confidence.

### Exclude or separately flag
- References that cannot be resolved to a unique publication.
- Claims with no citation marker, unless they are intentionally collected as a separate uncited-claim control.
- Pure opinions, recommendations, or vague rhetorical statements with no verifiable proposition.
- Source files with extraction corruption that prevents meaningful inspection.
- Duplicate summary/source pairs.
- Items where the cited source is inaccessible; retain these in an access-failure log rather than labeling them unsupported.

Record exclusion reasons. Do not silently delete difficult examples.

## 9. Pilot sampling plan

### Initial planning target
- 20–30 Computer Science source papers.
- 50–100 claim–citation pairs.
- Both abstract and full-text evidence conditions.
- Two independent annotators for all pilot items if workload permits.
- Include a mix of claim types: empirical findings, method descriptions, dataset properties, comparative claims, numerical claims, and limitations.

These numbers are initial workload targets only. They are not a power calculation and do not establish statistical representativeness.

### Sampling safeguards
- Sample across several CS subareas if source availability permits, but do not describe the pilot as cross-domain.
- Avoid selecting only easy claims or only papers that appear to support the generated summary.
- Record how papers and claims were selected.
- Keep source-paper groups intact when creating development/test splits; do not split claims from the same source paper across train and test.
- If the dataset is too small for a meaningful held-out test set, report the work as a pilot benchmark and avoid strong generalization claims.

## 10. Two-annotator workflow

1. **Calibration set:** Both annotators independently label 5–10 examples.
2. **Discussion:** Compare disagreements and identify unclear instructions. Do not count calibration labels as final independent labels after discussion unless they are re-annotated independently under the frozen guide.
3. **Freeze guide v1.0:** Record changes and examples.
4. **Independent annotation:** Both annotators label the same pilot records without seeing each other's decisions.
5. **Agreement calculation:** Report raw agreement and an appropriate chance-corrected statistic. Cohen's kappa may be used for two annotators and categorical labels; report class distribution because prevalence can affect interpretation. Consider a separate agreement analysis for evidence availability and support judgment.
6. **Adjudication:** Resolve disagreements after independent labels are saved. Record original labels, final adjudicated label, reason, and adjudicator.
7. **Guide revision:** If rules change materially, version the guide and re-annotate affected items.

Do not overwrite the two original annotations with the adjudicated label.

## 11. Quality checks

Before model evaluation, verify:
- Every claim has its original sentence and citation marker.
- Every cited paper has a stable identifier or an explicit unresolved status.
- Evidence spans are copied exactly and have a location.
- Support labels are consistent with evidence availability.
- `CONTRADICTED` has explicit conflicting evidence.
- `NOT_SUPPORTED_IN_INSPECTED_SOURCE` records what source scope was inspected.
- Partial labels identify which claim components are supported and unsupported.
- Duplicate items and source-level leakage are checked.
- Both annotators' independent labels are preserved.
- All label changes are traceable to a guide version or adjudication record.

## 12. Proposed pilot stop/go criteria

These are operational review criteria, not universal standards. Revisit them after the calibration set.

Proceed to a larger annotation round only if:
- the cited source can be resolved for most selected items;
- full-text access is adequate for the planned task;
- annotators can apply the labels consistently after guideline revision;
- evidence spans and locations can be recorded reliably;
- the workload is manageable;
- no major label definition remains ambiguous.

Pause and revise if:
- annotators frequently confuse `NOT_SUPPORTED_IN_INSPECTED_SOURCE` with `CONTRADICTED`;
- retrieval failure is routinely mislabeled as unsupported;
- claim segmentation changes meaning;
- full-text access is systematically missing;
- source-paper leakage cannot be controlled.

Do not set an arbitrary agreement threshold as proof of validity. Report the actual agreement, prevalence, disagreements, and adjudication process.

## 13. Decisions still open

- Exact source corpus/repository and its license.
- Whether summaries will be generated from individual papers or multi-paper literature sets.
- Exact generation model/version and prompt.
- Whether multi-source collective support belongs in the first pilot or a separate extension.
- Final sample size and split strategy after the pilot.
- Exact evidence-span scoring rule.
- Whether the test set can be large enough for stable per-class metrics.

## 14. Next actions

1. Select a candidate set of Computer Science papers and verify full-text access and reuse terms.
2. Create 5–10 calibration examples.
3. Have both annotators independently apply this draft guide.
4. Review disagreements and revise to version 1.0.
5. Freeze the pilot sampling manifest and annotation CSV schema.
6. Only then begin full pilot annotation.
