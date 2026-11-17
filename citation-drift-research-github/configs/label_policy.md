# Label and score policy

AlignScore's score is a continuous factual-consistency/alignment value. The published interface returns a single numerical value for each context–claim pair. It is not, by itself, evidence that a four-way label prediction has been validated.

Human labels:
- SUPPORTED
- PARTIALLY_SUPPORTED
- NOT_SUPPORTED_IN_INSPECTED_SOURCE
- CONTRADICTED

Evidence availability is separate:
- AVAILABLE
- INSUFFICIENT_ACCESS
- INSUFFICIENT_RETRIEVAL
- INSUFFICIENT_CONTEXT

Default pipeline behavior: save scores only.

Optional binary evaluation:
- Only `SUPPORTED` is positive.
- Only `NOT_SUPPORTED_IN_INSPECTED_SOURCE` is negative.
- Partial and contradicted examples are excluded from this particular binary calculation unless a preregistered alternative mapping is justified.
- Threshold must be chosen on development data, then frozen before test evaluation.
- This binary simplification must be disclosed and cannot be presented as a four-class evaluation.
