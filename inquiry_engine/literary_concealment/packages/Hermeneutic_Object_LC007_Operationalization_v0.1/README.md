# Hermeneutic Object LC-007 Operationalization — v0.1

This package continues the technique-by-technique executable projection of
**Strauss's Taxonomy of Literary Concealment**.

It operationalizes only:

- **LC-007 — Two-Faced Speech**

## Authority boundary

The authoritative human-readable source remains:

`engine_training/Hermeneutic_Object_Strauss_Taxonomy_of_Literary_Concealment_v1.0.txt`

The source is pinned to repository commit:

`7100700ef10d68621f4859b5fe94fac6e5e0fcea`

This package is **DEVELOPMENT ONLY**. It:

- assigns no canonical identifier;
- does not admit or certify the Hermeneutic Object;
- does not integrate LC-007 into Cognitive Memory;
- does not authorize production use;
- does not alter the human-readable Taxonomy;
- does not infer concealment, persecution, actual reception, or truth.

## Distinction from LC-006, LC-008, and LC-009

LC-006 concerns multiple viable meanings of a word.

LC-007 concerns a broader communicative structure: the same verbal surface
supports an exterior and an interior reading with distinct functions and
audience horizons.

LC-008 concerns concealment concentrated in a small common word.

LC-009 concerns recurrent secret terminology.

The techniques must remain separate.

## What has been made executable

`techniques/LC-007.json` preserves:

- Strauss's two-faced-speech description;
- separate exterior and interior reading records;
- proposition, textual support, function, and audience-horizon fields;
- same-verbal-surface requirements;
- ordinary alternatives and disqualifying conditions;
- authorized responses and prohibited inferences;
- uncertainty and termination rules;
- version history.

`evaluate_lc007()` evaluates **structured reading records**. It does not invent
an interior reading, infer an audience, or select a true teaching.

## Local outcomes

1. `NOT_TRIGGERED`
2. `BLOCKED_MISSING_EVIDENCE`
3. `CANDIDATE_TWO_FACED_SPEECH`
4. `CORROBORATED_TWO_FACED_SPEECH`

These are runtime outcomes only. They are not repository lifecycle statuses or
epistemic classifications.

## Run tests

```bash
python -m pip install -e '.[dev]'
pytest -q
```

## Next production unit

Operationalize **LC-008 — Concealment in a Single Common Word** while
preserving its distinction from semantic ambiguity and secret terminology.
