# Hermeneutic Object LC-005 Operationalization — v0.1

This package continues the technique-by-technique executable projection of
**Strauss's Taxonomy of Literary Concealment**.

It operationalizes only:

- **LC-005 — Intermediary Assertion and Creeping Contradiction**

## Authority boundary

The authoritative human-readable source remains:

`engine_training/Hermeneutic_Object_Strauss_Taxonomy_of_Literary_Concealment_v1.0.txt`

The source is pinned to repository commit:

`7100700ef10d68621f4859b5fe94fac6e5e0fcea`

This package is **DEVELOPMENT ONLY**. It:

- assigns no canonical identifier;
- does not admit or certify the Hermeneutic Object;
- does not integrate LC-005 into Cognitive Memory;
- does not authorize production use;
- does not alter the human-readable Taxonomy;
- does not infer concealment, intention, hidden teaching, or truth.

## Distinction from LC-004

LC-004 requires two parallel passages: a later apparent repetition alters an
earlier formulation through a minute addition or omission.

LC-005 requires three ordered stages:

1. a first statement;
2. an intermediary assertion compatible with the first;
3. a final altered repetition of the intermediary that contradicts the first.

Without a distinct intermediary assertion, LC-005 is not triggered.

## What has been made executable

`techniques/LC-005.json` preserves:

- Strauss's formulation and explanation;
- the required three-stage sequence;
- intermediary compatibility;
- altered repetition between intermediary and final passages;
- proposition-level contradiction between first and final passages;
- ordinary alternatives and disqualifying conditions;
- authorized investigative responses;
- prohibited inferences;
- uncertainty and termination rules;
- version history.

`evaluate_lc005()` evaluates a **structured, already reconstructed sequence**.
It does not discover the passages, alignment, semantic effect, contradiction,
or authorial intention from raw prose.

## Local outcomes

1. `NOT_TRIGGERED`
2. `BLOCKED_MISSING_EVIDENCE`
3. `CANDIDATE_CREEPING_CONTRADICTION_SEQUENCE`
4. `CORROBORATED_CREEPING_CONTRADICTION_SEQUENCE`

These are runtime outcomes only. They are not repository lifecycle statuses or
epistemic classifications.

## Run tests

```bash
python -m pip install -e '.[dev]'
pytest -q
```

## Next production unit

Operationalize **LC-006 — Use of Ambiguous Words** while preserving its
distinction from LC-007, LC-008, and LC-009.
