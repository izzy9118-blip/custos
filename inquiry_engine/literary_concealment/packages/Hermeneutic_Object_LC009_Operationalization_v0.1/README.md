# Hermeneutic Object LC-009 Operationalization — v0.1

This package continues the technique-by-technique executable projection of
**Strauss's Taxonomy of Literary Concealment**.

It operationalizes only:

- **LC-009 — Secret Terminology**

## Authority boundary

The authoritative human-readable source remains:

`engine_training/Hermeneutic_Object_Strauss_Taxonomy_of_Literary_Concealment_v1.0.txt`

The source is pinned to repository commit:

`7100700ef10d68621f4859b5fe94fac6e5e0fcea`

This package is **DEVELOPMENT ONLY**. It assigns no canonical identifier,
confers no admission or certification, and authorizes no production use.

## Corpus-level rule

LC-009 cannot be established from a single occurrence.

The evaluator requires a declared scope, an occurrence index, normalized
variants, usage classifications, contextual and architectonic distributions,
negative cases, ordinary alternatives, and independent corroboration.

Frequency alone is never sufficient.

## Distinctions

- LC-006 concerns ambiguity in a bounded passage.
- LC-008 concerns a common word in a low-prominence location.
- LC-009 concerns a recurrent terminology system across a declared corpus.

The techniques remain separate.

## Local outcomes

1. `NOT_TRIGGERED`
2. `BLOCKED_MISSING_EVIDENCE`
3. `CANDIDATE_SECRET_TERMINOLOGY_PATTERN`
4. `CORROBORATED_SECRET_TERMINOLOGY_PATTERN`

Even the strongest outcome does not establish concealment, hidden meaning,
authorial intention, audience, or doctrinal truth.

## Run tests

```bash
python -m pip install -e '.[dev]'
pytest -q
```

## Next production unit

Operationalize **LC-010 — Intentional Sophism** while preserving Strauss's
documentary limit: the source names the device but does not yet classify its subtypes.
