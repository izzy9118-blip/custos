# Hermeneutic Object LC-020 Operationalization — v0.1

This package operationalizes:

- **LC-020 — Hint**

## Strauss's documentary distinction

A hint is a small textual indication that assists the attentive reader in:

- discovering a contradiction; or
- determining how contradictory statements should be weighed.

Recognizing a hint requires more independent understanding than recognizing an
obvious contradiction.

## Governing safeguard

A small feature is not a hint merely because it appears unusual or suggestive.

The evaluator requires:

- an exact bounded cue;
- an independently documented contradiction or discernment problem;
- a finite ordered discovery path;
- documentary support for every inferential step;
- proof that the cue materially narrows or redirects inquiry;
- alternative-target and counterpath testing;
- review of adjacent techniques that may explain the cue;
- source-language, translation, witness, and context controls.

Free association, hindsight, and unbounded chains are prohibited.

## Local outcomes

1. `NOT_TRIGGERED`
2. `BLOCKED_MISSING_EVIDENCE`
3. `CANDIDATE_HINT_PATH`
4. `CORROBORATED_HINT_PATH`

A corroborated outcome establishes only the cue-to-inquiry path. It does not
establish hidden teaching, doctrinal truth, authorial intention, intended
audience, or concealment.

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

Operationalize **LC-021 — Inappropriate Expression** while preserving Strauss's
warning that the expression may be merely inappropriate and therefore does not
compel inquiry as strongly as a contradiction.
