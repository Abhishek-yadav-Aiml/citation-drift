# Research prompts — preserve with experiment metadata

These are proposed fixed prompts for the user's experiment. Record exact model/provider/version, date, temperature, token limit and raw outputs. Do not treat model-generated references as verified.

## Prompt A — literature-summary generation

You are assisting with a scientific literature review in computer science.

Topic: [INSERT TOPIC]

Use ONLY the source papers and metadata supplied below. Do not invent papers, authors, years, DOIs, URLs, results, or methods. If the supplied sources do not support a statement, omit it or explicitly mark it as uncertain.

Write a concise synthesis that:
1. Identifies the research problem.
2. Compares the methods and contributions of the supplied papers.
3. Reports results only when present in the supplied source material.
4. Places citation markers immediately after the claims they support.
5. Distinguishes findings from limitations and open questions.
6. Does not use a citation to support a claim unless the supplied source content supports that claim.

For every factual sentence, retain a traceable source-paper citation marker such as [P1]. Do not create a bibliography entry unless the metadata is supplied.

SOURCE PAPERS:
[PASTE PAPER IDs, TITLES, ABSTRACTS / EXTRACTED PASSAGES]

Output: approximately [N] words, followed by a numbered list mapping [P1], [P2], etc. to the supplied source IDs.

## Prompt B — claim/citation pair extraction

You are a research data annotator. Extract claim–citation pairs from the supplied generated literature summary.

Rules:
- Preserve each original sentence verbatim.
- Extract each factual claim and its adjacent citation marker(s).
- If a sentence contains multiple independently verifiable factual propositions, split it into atomic claims while retaining the original sentence and shared claim-group ID.
- For multiple citations, create one pair per cited source paper.
- Never invent a citation marker or source-paper ID.
- If no citation is attached, set citation_marker to null.
- Output valid JSON only.

Schema:
[
  {
    "claim_id": "C001",
    "original_sentence": "...",
    "atomic_claim": "...",
    "citation_marker": "[P1]",
    "source_paper_id": "P1"
  }
]

SUMMARY:
[PASTE SUMMARY]

CITATION MAP:
[PASTE EXACT MARKER-TO-SOURCE MAP]

## Prompt C — atomic-fact decomposition (FActScore-inspired adaptation)

Split the input claim into the smallest set of independently verifiable factual propositions.

Rules:
- Preserve named entities, quantities, units, dates, comparison direction, negation, uncertainty and qualifiers.
- Do not add facts that are not in the original claim.
- Do not rewrite a claim to make it easier to support.
- If the sentence contains one proposition, return one item.
- Output valid JSON only.

Schema:
{
  "original_claim": "...",
  "atomic_facts": [
    {"fact_id": "F1", "text": "..."}
  ]
}

CLAIM:
[PASTE CLAIM]

This is an adaptation for atomic decomposition; it is not a faithful reproduction of the original FActScore evaluation pipeline.

## Prompt D — human annotation guideline helper (not an automated gold-labeler)

Annotators must inspect the cited source and record:
- support label: SUPPORTED / PARTIALLY_SUPPORTED / NOT_SUPPORTED_IN_INSPECTED_SOURCE / CONTRADICTED;
- evidence availability: AVAILABLE / INSUFFICIENT_ACCESS / INSUFFICIENT_RETRIEVAL / INSUFFICIENT_CONTEXT;
- exact evidence passage(s), page/section and source version;
- short rationale.

Do not treat failed retrieval or inaccessible full text as NOT_SUPPORTED. Use CONTRADICTED only when the inspected source provides evidence that conflicts with the claim. For synthesis claims requiring multiple sources, annotate each source-pair separately and record the multi-source relationship.
