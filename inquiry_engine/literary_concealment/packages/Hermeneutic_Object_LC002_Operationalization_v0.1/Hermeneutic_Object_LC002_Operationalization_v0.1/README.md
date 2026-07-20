# Hermeneutic Object LC-002 Operationalization — v0.1

This package continues the technique-by-technique executable projection of
**Strauss's Taxonomy of Literary Concealment**.

It operationalizes only:

- **LC-002 — Incidental Placement of One Contradictory Statement**

## Authority boundary

The authoritative human-readable source remains:

`engine_training/Hermeneutic_Object_Strauss_Taxonomy_of_Literary_Concealment_v1.0.txt`

The source is pinned to repository commit:

`7100700ef10d68621f4859b5fe94fac6e5e0fcea`

This package is **DEVELOPMENT ONLY**. It:

- assigns no canonical identifier;
- does not admit or certify the Hermeneutic Object;
- does not integrate LC-002 into Cognitive Memory;
- does not authorize production use;
- does not alter the human-readable Taxonomy;
- does not infer hidden teaching from contradiction and unequal prominence alone;
- does not treat the incidental statement as true, superior, or authoritative.

## Distinction from LC-001

LC-001 concerns **positional separation** between contradictory statements.
LC-002 concerns **unequal prominence**: one contradictory statement appears in
passing, parenthetically, incidentally, or as a subordinate remark while the
other receives fuller or more prominent presentation.

Distance is not required for LC-002. The two techniques may co-occur, but the
engine must evaluate and record them separately.

## What has been made executable

`techniques/LC-002.json` preserves:

- Strauss's formulation, page, and identified example;
- the documentary mechanism of unequal prominence;
- the evidence needed to establish incidental placement;
- ordinary alternatives and disqualifying conditions;
- authorized investigative responses;
- prohibited inferences;
- uncertainty and termination rules;
- version history.

`evaluate_lc002()` evaluates a **structured, already extracted contradictory
pair**. It does not determine from raw prose whether a statement is incidental,
prominent, contradictory, or true. Those judgments must be supplied as explicit,
auditable inputs.

## Local outcomes

The evaluator uses four noncanonical development outcomes:

1. `NOT_TRIGGERED`
2. `BLOCKED_MISSING_EVIDENCE`
3. `CANDIDATE_UNEQUAL_PROMINENCE_PAIR`
4. `CORROBORATED_UNEQUAL_PROMINENCE_CONTRADICTION`

These are runtime outcomes only. They are not repository lifecycle statuses or
epistemic classifications.

## Run tests

```bash
python -m pip install -e '.[dev]'
pytest -q
```

## Next production unit

Operationalize **LC-003 — Contradiction of Implications Rather Than Direct
Statement** without collapsing implication reconstruction into LC-001 or LC-002.
