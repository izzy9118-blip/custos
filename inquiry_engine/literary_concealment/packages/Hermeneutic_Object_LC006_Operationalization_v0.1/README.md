# Hermeneutic Object LC-006 Operationalization — v0.1

This package continues the technique-by-technique executable projection of
**Strauss's Taxonomy of Literary Concealment**.

It operationalizes only:

- **LC-006 — Use of Ambiguous Words**

## Authority boundary

The authoritative human-readable source remains:

`engine_training/Hermeneutic_Object_Strauss_Taxonomy_of_Literary_Concealment_v1.0.txt`

The source is pinned to repository commit:

`7100700ef10d68621f4859b5fe94fac6e5e0fcea`

This package is **DEVELOPMENT ONLY**. It:

- assigns no canonical identifier;
- does not admit or certify the Hermeneutic Object;
- does not integrate LC-006 into Cognitive Memory;
- does not authorize production use;
- does not alter the human-readable Taxonomy;
- does not infer concealment, intended audience, secret terminology, or truth.

## Distinction from LC-007, LC-008, and LC-009

LC-006 concerns multiple viable meanings of one word or compact expression.

LC-007 concerns a broader two-faced speech addressed differently to different
audiences.

LC-008 concerns concealment concentrated in a small, common, unobtrusive word,
which need not itself be ambiguous.

LC-009 concerns recurrent secret terminology requiring corpus-level study.

The techniques must not be silently merged.

## What has been made executable

`techniques/LC-006.json` preserves:

- Strauss's formulation and example;
- explicit sense records;
- source-language and syntactic viability requirements;
- context-preserving renderings;
- materially distinct proposition tests;
- ordinary alternatives and disqualifying conditions;
- authorized investigative responses;
- prohibited inferences;
- uncertainty and termination rules;
- version history.

`evaluate_lc006()` evaluates **structured candidate senses**. It does not
invent meanings from raw prose or select a hidden meaning.

## Local outcomes

1. `NOT_TRIGGERED`
2. `BLOCKED_MISSING_EVIDENCE`
3. `CANDIDATE_LEXICAL_AMBIGUITY`
4. `CORROBORATED_LEXICAL_AMBIGUITY`

These are runtime outcomes only. They are not repository lifecycle statuses or
epistemic classifications.

## Run tests

```bash
python -m pip install -e '.[dev]'
pytest -q
```

## Next production unit

Operationalize **LC-007 — Two-Faced Speech** while preserving its distinction
from lexical ambiguity and from any automatic inference of audience intent.
