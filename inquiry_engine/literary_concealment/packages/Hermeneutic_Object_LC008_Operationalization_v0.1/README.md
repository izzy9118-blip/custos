# Hermeneutic Object LC-008 Operationalization — v0.1

This package continues the technique-by-technique executable projection of
**Strauss's Taxonomy of Literary Concealment**.

It operationalizes only:

- **LC-008 — Concealment in a Single Common Word**

## Authority boundary

The authoritative human-readable source remains:

`engine_training/Hermeneutic_Object_Strauss_Taxonomy_of_Literary_Concealment_v1.0.txt`

The source is pinned to repository commit:

`7100700ef10d68621f4859b5fe94fac6e5e0fcea`

This package is **DEVELOPMENT ONLY**. It assigns no canonical identifier,
confers no admission or certification, and authorizes no production use.

## Anti-overreading rule

The engine must not search every ordinary word for secrets.

LC-008 may be evaluated only after an independent documentary trigger—such as
a contradiction, source comparison, repetition, omission, architectural
pattern, or explicit authorial indication—directs attention to the word.

## Distinctions

- LC-006 concerns semantic ambiguity.
- LC-008 concerns a common word's smallness, unobtrusive placement, and
  independently documented material effect.
- LC-009 concerns recurrent secret terminology.
- LC-002 concerns an incidental statement rather than a word-level carrier.
- LC-020 concerns hints generally.

The techniques remain separate.

## Local outcomes

1. `NOT_TRIGGERED`
2. `BLOCKED_MISSING_EVIDENCE`
3. `CANDIDATE_COMMON_WORD_SIGNAL`
4. `CORROBORATED_COMMON_WORD_SIGNAL`

Even the strongest outcome does not establish concealment, hidden meaning,
authorial intention, audience, or doctrinal truth.

## Run tests

```bash
python -m pip install -e '.[dev]'
pytest -q
```

## Next production unit

Operationalize **LC-009 — Secret Terminology** as a corpus-level lexical
system without converting every repeated word into a secret term.
