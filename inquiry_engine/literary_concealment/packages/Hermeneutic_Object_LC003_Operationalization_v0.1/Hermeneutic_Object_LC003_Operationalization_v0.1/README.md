# Hermeneutic Object LC-003 Operationalization — v0.1

This package continues the technique-by-technique executable projection of
**Strauss's Taxonomy of Literary Concealment**.

It operationalizes only:

- **LC-003 — Contradiction of Implications Rather Than Direct Statement**

## Authority boundary

The authoritative human-readable source remains:

`engine_training/Hermeneutic_Object_Strauss_Taxonomy_of_Literary_Concealment_v1.0.txt`

The source is pinned to repository commit:

`7100700ef10d68621f4859b5fe94fac6e5e0fcea`

This package is **DEVELOPMENT ONLY**. It:

- assigns no canonical identifier;
- does not admit or certify the Hermeneutic Object;
- does not integrate LC-003 into Cognitive Memory;
- does not authorize production use;
- does not alter the human-readable Taxonomy;
- does not treat a reconstructed implication as an authorial quotation;
- does not infer hidden teaching, intention, or truth from an implication contradiction.

## Distinction from LC-001 and LC-002

LC-001 concerns **positional distance** between directly incompatible statements.
LC-002 concerns **unequal prominence** between contradictory statements.
LC-003 concerns an **indirect logical relation**: a first statement is not denied
verbatim, but a later statement contradicts a proposition that follows from it
through one or more documented bridge propositions.

Distance and prominence may coexist with LC-003, but they are neither necessary
nor sufficient. Each technique must be evaluated and recorded separately.

## What has been made executable

`techniques/LC-003.json` preserves:

- Strauss's formulation, symbol, pages, and examples;
- the distinction between pronounced statements and reconstructed bracketed
  propositions;
- the minimum evidence required for a valid implication chain;
- ordinary alternatives and disqualifying conditions;
- authorized investigative responses;
- prohibited inferences;
- uncertainty and termination rules;
- version history.

`evaluate_lc003()` evaluates a **structured, already reconstructed implication
chain**. It does not discover propositions, term identity, implication validity,
contradiction, or authorial intention from raw prose. Those judgments must be
supplied as explicit, auditable inputs.

## Local outcomes

The evaluator uses four noncanonical development outcomes:

1. `NOT_TRIGGERED`
2. `BLOCKED_MISSING_EVIDENCE`
3. `CANDIDATE_IMPLICATION_CONTRADICTION`
4. `CORROBORATED_IMPLICATION_CONTRADICTION`

These are runtime outcomes only. They are not repository lifecycle statuses or
epistemic classifications.

## Run tests

```bash
python -m pip install -e '.[dev]'
pytest -q
```

## Next production unit

Operationalize **LC-004 — Apparent Repetition with Minute Addition or Omission**
without treating every wording difference as a contradiction.
