# Hermeneutic Object LC-015 Operationalization — v0.1

This package operationalizes:

- **LC-015 — Deliberate Misquotation Through Omission**

## Documentary operation

LC-015 requires an identifiable quotation or citation, a recovered source or
source-version family, and a complete source-to-quotation collation.

The evaluator asks whether omitted source words materially change:

- meaning;
- scope;
- qualification;
- attribution;
- epistemic or rhetorical status;
- doctrinal force.

A shortened quotation is not automatically a misquotation.

## Deliberateness boundary

The technique name preserves Strauss's reconstruction. The runtime evaluator
does **not** infer deliberate alteration from omission alone.

Even a corroborated result is limited to:

`CORROBORATED_QUOTATION_OMISSION`

Direct intentionality evidence may be preserved for later documentary review,
but v0.1 does not adjudicate it.

## Distinctions

- LC-014 is the broader category of significant omission.
- LC-015 is quotation-specific and requires source collation.
- LC-004 concerns altered repetition and need not involve an external source.

## Authority boundary

The authoritative source remains:

`engine_training/Hermeneutic_Object_Strauss_Taxonomy_of_Literary_Concealment_v1.0.txt`

Pinned repository commit:

`7100700ef10d68621f4859b5fe94fac6e5e0fcea`

This package is **DEVELOPMENT ONLY**. It assigns no canonical identifier,
confers no admission or certification, and authorizes no production use.

## Local outcomes

1. `NOT_TRIGGERED`
2. `BLOCKED_MISSING_EVIDENCE`
3. `CANDIDATE_QUOTATION_OMISSION`
4. `CORROBORATED_QUOTATION_OMISSION`

No outcome establishes deliberate misquotation, concealment, hidden teaching,
intended readership, authorial truth, or falsity of the shortened quotation.

## Run tests

```bash
python -m pip install -e '.[dev]'
pytest -q
```

## Next production unit

Operationalize **LC-016 — Repetition as Leitmotif** while distinguishing
purposeful recurrence from ordinary repetition and preserving altered or
incomplete forms as separate evidence.
