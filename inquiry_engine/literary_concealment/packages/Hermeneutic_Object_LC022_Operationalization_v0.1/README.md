# Hermeneutic Object LC-022 Operationalization — v0.1

This package operationalizes:

- **LC-022 — Clumsy Transition**

## Strauss's documentary limit

An awkward movement between subjects may signal a concealed relationship or
structural break.

Strauss also warns that it may be **mere clumsiness unless corroborated**.
LC-022 therefore has weaker evidentiary force than a contradiction.

## Required structure

The evaluator requires:

- two adjacent or explicitly linked textual units;
- independent reconstruction of the subject or argumentative task on each side;
- an exact transition boundary and connective record;
- an independent, historically appropriate transition-coherence baseline;
- a typed mismatch;
- a documented material structural effect;
- evidence that the transition functions as an attention-directing anomaly;
- a bounded question that asserts no concealed relation;
- source-language, discourse-marker, translation, paragraphing, witness,
  speaker, authorial-practice, and adjacent-technique review;
- testing of ellipsis, topic change, pedagogy, genre, speaker shift, source
  compilation, translation, editorial segmentation, textual damage, revision,
  and mere clumsiness.

## Governing safeguard

Even the strongest outcome preserves:

- `evidentiary_force = WEAK_POSSIBLE_SIGNAL`
- `inquiry_compelled_as_contradiction = false`
- `concealed_relation_inferred = false`
- `mere_clumsiness_excluded_with_certainty = false`

The engine may ask why the transition occurs. It may not invent the relation
between the two subjects.

## Local outcomes

1. `NOT_TRIGGERED`
2. `BLOCKED_MISSING_EVIDENCE`
3. `CANDIDATE_CLUMSY_TRANSITION_SIGNAL`
4. `CORROBORATED_CLUMSY_TRANSITION_SIGNAL`

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

## Completion point

LC-022 completes the v1.0 operationalization sequence for LC-001 through LC-022.

The next production step is a cross-package consistency and integration review
before any repository admission, certification, or expansion to the v1.1 draft.
