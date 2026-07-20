# Hermeneutic Object LC-001 Operationalization — v0.1

This package begins the technique-by-technique executable projection of
**Strauss's Taxonomy of Literary Concealment**.

It operationalizes only:

- **LC-001 — Separation by Distant Placement**

## Authority boundary

The authoritative human-readable source remains:

`engine_training/Hermeneutic_Object_Strauss_Taxonomy_of_Literary_Concealment_v1.0.txt`

The source is pinned to repository commit:

`7100700ef10d68621f4859b5fe94fac6e5e0fcea`

This package is **DEVELOPMENT ONLY**. It:

- assigns no canonical identifier;
- does not admit or certify the Hermeneutic Object;
- does not integrate LC-001 into Cognitive Memory;
- does not authorize production use;
- does not alter the human-readable Taxonomy;
- does not infer hidden teaching from contradiction and distance alone.

## What has been made executable

`techniques/LC-001.json` preserves:

- Strauss's formulation and source location;
- mechanism and investigative requirement;
- distinctions from neighboring techniques;
- trigger conditions;
- minimum evidence;
- corroboration indicators;
- ordinary alternatives;
- disqualifying conditions;
- authorized responses;
- prohibited inferences;
- uncertainty and termination rules;
- version history.

`evaluate_lc001()` evaluates a **structured, already extracted passage pair**.
It does not perform semantic interpretation of raw prose. Its strongest result is
`CORROBORATED_CONTRADICTION`, not “concealment proven.”

## Local outcomes

The evaluator uses four noncanonical development outcomes:

1. `NOT_TRIGGERED`
2. `BLOCKED_MISSING_EVIDENCE`
3. `CANDIDATE_PAIR`
4. `CORROBORATED_CONTRADICTION`

These are runtime outcomes only and are not repository lifecycle or epistemic classifications.

## Run tests

```bash
python -m pip install -e '.[dev]'
pytest -q
```

## Next production unit

Operationalize **LC-002 — Incidental Placement of One Contradictory Statement**
without merging its unequal-prominence logic into LC-001.
