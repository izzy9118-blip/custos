# Hermeneutic Object LC-004 Operationalization — v0.1

This package continues the technique-by-technique executable projection of
**Strauss's Taxonomy of Literary Concealment**.

It operationalizes only:

- **LC-004 — Apparent Repetition with Minute Addition or Omission**

## Authority boundary

The authoritative human-readable source remains:

`engine_training/Hermeneutic_Object_Strauss_Taxonomy_of_Literary_Concealment_v1.0.txt`

The source is pinned to repository commit:

`7100700ef10d68621f4859b5fe94fac6e5e0fcea`

This package is **DEVELOPMENT ONLY**. It:

- assigns no canonical identifier;
- does not admit or certify the Hermeneutic Object;
- does not integrate LC-004 into Cognitive Memory;
- does not authorize production use;
- does not alter the human-readable Taxonomy;
- does not treat every wording difference as significant;
- does not infer concealment, intention, hidden teaching, or truth.

## Distinction from adjacent techniques

LC-003 concerns a contradiction recovered through an unpronounced implication.

LC-004 concerns a later passage that appears to repeat an earlier passage but
adds or omits a minute expression whose documented semantic effect produces a
contradiction.

LC-005 requires an intermediary assertion through which the final
contradiction “creeps in.” No intermediary assertion is required for LC-004.

Each technique must be evaluated and recorded separately.

## What has been made executable

`techniques/LC-004.json` preserves:

- Strauss's formulation and source page;
- the absence of a worked documentary example in the authoritative entry;
- the apparent-repetition requirement;
- explicit addition and omission records;
- word-by-word alignment requirements;
- semantic-effect and proposition-level contradiction requirements;
- ordinary alternatives and disqualifying conditions;
- authorized investigative responses;
- prohibited inferences;
- uncertainty and termination rules;
- version history.

`evaluate_lc004()` evaluates a **structured, already aligned passage pair**. It
does not discover parallelism, textual differences, semantic effect,
contradiction, or authorial intention from raw prose. Those judgments must be
supplied as explicit, auditable inputs.

## Local outcomes

The evaluator uses four noncanonical development outcomes:

1. `NOT_TRIGGERED`
2. `BLOCKED_MISSING_EVIDENCE`
3. `CANDIDATE_MINUTE_VARIATION_CONTRADICTION`
4. `CORROBORATED_MINUTE_VARIATION_CONTRADICTION`

These are runtime outcomes only. They are not repository lifecycle statuses or
epistemic classifications.

## Run tests

```bash
python -m pip install -e '.[dev]'
pytest -q
```

## Next production unit

Operationalize **LC-005 — Intermediary Assertion and Creeping Contradiction**
without collapsing it into LC-004.
