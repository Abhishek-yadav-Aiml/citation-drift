# AI Assistance / Debugging Log

| ID | Date | Component | Observed issue | Confirmed evidence | Hypotheses | Correction | Verification | Earlier results rerun? |
|---|---|---|---|---|---|---|---|---|
| DBG-001 | 2026-11-17 | AlignScore environment | `ModuleNotFoundError: spacy`, then `ModuleNotFoundError: click`; environment lacked `pip` module | These exact import errors were reported by user | Dependency installation was incomplete because AlignScore source was installed with `--no-deps`; exact final environment state unknown | Install missing dependencies using the same interpreter/uv environment; then run import and inference smoke test | Pending user console output | No AlignScore results confirmed; rerun required once inference works |
| DBG-002 | 2026-11-17 | Dataset loader | Synthetic JSONL test | User reported 2 records, 0 errors, 2 source papers, 1 labeled record; M1 sanity test passed | None needed for that fixture | No correction | Passed on synthetic fixture only | No research data results exist from this test |
