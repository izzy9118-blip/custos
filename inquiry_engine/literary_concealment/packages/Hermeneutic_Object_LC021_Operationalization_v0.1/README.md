# Hermeneutic Object LC-021 Operationalization — v0.1

This package operationalizes:

- **LC-021 — Inappropriate Expression**

## Strauss's documentary limit

A seemingly ill-fitting expression may function as a stumbling block directing
attention beneath the surface.

Strauss also warns that it may be dismissed as **merely inappropriate**.
LC-021 therefore has weaker evidentiary force than a contradiction.

## Required structure

The evaluator requires:

- an exact bounded expression;
- an independent, historically appropriate fit baseline;
- a typed and documented mismatch;
- material disruption of the surface reading;
- evidence that the mismatch functions as a possible stumbling block;
- a bounded textual question that asserts no hidden answer;
- source-language, grammar, translation, witness, speaker, genre, technical
  usage, and authorial-usage review;
- testing of ordinary repairs and the merely-inappropriate explanation;
- independent corroboration before the signal can be strengthened.

## Governing safeguard

Even the strongest outcome preserves:

- `evidentiary_force = WEAK_POSSIBLE_SIGNAL`
- `inquiry_compelled_as_contradiction = false`
- `merely_inappropriate_excluded_with_certainty = false`

The engine may ask why the expression occurs. It may not answer that question
by inventing a hidden teaching.

## Local outcomes

1. `NOT_TRIGGERED`
2. `BLOCKED_MISSING_EVIDENCE`
3. `CANDIDATE_INAPPROPRIATE_EXPRESSION_SIGNAL`
4. `CORROBORATED_INAPPROPRIATE_EXPRESSION_SIGNAL`

## Authority boundary

The authoritative source remains:

`engine_training/Hermeneutic_Object_Strauss_Taxonomy_of_Literary_Concealment_v1.0.txt`

Pinned repository commit:

`7100700ef10d68621f4859b5fe94fac6e5e0fcea`

This package is **DEVELOPMENT ONLY**. It assigns no canonical identifier,
confers no admission or certification, and authorizes no production use.

## Run tests

```bash
python -m pip install -e '.[dev]'
pytest -q
```

## Next production unit

Operationalize **LC-022 — Clumsy Transition** while preserving Strauss's
warning that an awkward transition may be mere clumsiness unless independently
corroborated.
