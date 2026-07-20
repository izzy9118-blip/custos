# Literary Concealment Integration

This directory governs the single certified LC-001 through LC-022 integration
used by the Custos Inquiry Engine.

## Certified integration

LC-001 through LC-022 are certified to function together as one executable,
installable, continuously tested Inquiry Engine subsystem. The certification
record is `TECHNICAL_CERTIFICATION_RECORD.md`; GitHub Actions reruns the full
Inquiry Engine test suite on every relevant pull request and push to `main`.

Technical integration certification does **not** itself confer:

- a canonical identifier;
- constitutional admission;
- Cognitive Memory integration;
- authority to certify interpretive conclusions.

The authoritative human-readable source remains:

`engine_training/Hermeneutic_Object_Strauss_Taxonomy_of_Literary_Concealment_v1.0.txt`

## Active engine

The active certified integration is under:

`inquiry_engine/src/custos_engine/literary_concealment/`

Each technique has an isolated namespace (`lc001` through `lc022`) within the
one active package. `registry.py` supplies discovery, loading, schema access,
and dispatch across the 22 runtimes.

The certification tests are under:

`inquiry_engine/tests/literary_concealment/`

`INTEGRATION_MANIFEST.json` records the certified active runtime and its
continuous-validation contract. `INTEGRATION_AUDIT.md` records the
pre-consolidation findings.
