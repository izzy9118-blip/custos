# Hermeneutic Object LC-010 Operationalization — v0.1

This package continues the technique-by-technique executable projection of
**Strauss's Taxonomy of Literary Concealment**.

It operationalizes only:

- **LC-010 — Intentional Sophism**

## Documentary limit

The authoritative Taxonomy states that Strauss names “intentional sophisms”
but does not classify their subtypes in the immediate source passage.

This package therefore detects and tests a **sophistic argument structure**. It
does not create a canonical fallacy taxonomy and does not adjudicate intention.

The word “intentional” in the technique name is preserved as Strauss's
terminology; it is not treated as a preauthorized conclusion about any newly
examined passage.

## Authority boundary

The authoritative source remains:

`engine_training/Hermeneutic_Object_Strauss_Taxonomy_of_Literary_Concealment_v1.0.txt`

Pinned repository commit:

`7100700ef10d68621f4859b5fe94fac6e5e0fcea`

This package is **DEVELOPMENT ONLY**. It assigns no canonical identifier,
confers no admission or certification, and authorizes no production use.

## Executable structure

The evaluator requires:

- a bounded argument;
- separately recorded explicit and reconstructed premises;
- ordered inference steps;
- a conclusion;
- a documented defect under an explicit standard;
- a corrected counterfactual argument;
- proof that the defect materially changes support;
- source, context, voice, translation, and variant review;
- ordinary-alternative testing;
- independent corroboration.

Direct intentionality evidence may be preserved, but v0.1 never converts it
into an automated declaration of intentional sophism.

## Local outcomes

1. `NOT_TRIGGERED`
2. `BLOCKED_MISSING_EVIDENCE`
3. `CANDIDATE_SOPHISTIC_STRUCTURE`
4. `CORROBORATED_SOPHISTIC_STRUCTURE`

No outcome establishes intention, concealment, hidden teaching, authorial
position, or a canonical subtype.

## Run tests

```bash
python -m pip install -e '.[dev]'
pytest -q
```

## Next production unit

Operationalize **LC-011 — Ironical Remark** while separating documented
surface-proposition reversal from ordinary humor, sarcasm, ambiguity, and
reader-imposed irony.
