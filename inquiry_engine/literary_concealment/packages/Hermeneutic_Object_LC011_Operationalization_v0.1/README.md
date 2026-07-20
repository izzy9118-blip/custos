# Hermeneutic Object LC-011 Operationalization — v0.1

This package continues the technique-by-technique executable projection of
**Strauss's Taxonomy of Literary Concealment**.

It operationalizes only:

- **LC-011 — Ironical Remark**

## Documentary limit

The authoritative Taxonomy states that Strauss names “ironical remarks” but
does not elaborate their varieties in the immediate source passage.

This package therefore identifies and tests a **surface/nonliteral divergence
structure**. It does not create a canonical taxonomy of irony.

## Required separation

The literal surface proposition and candidate nonliteral proposition are stored
as separate records. The nonliteral proposition must preserve the exact words
and must carry an explicit reconstruction basis.

Irony is not assumed to mean the exact opposite of the surface statement.

## Safeguards

The evaluator requires documentary markers and full testing of:

- literal coherence;
- speaker and dramatic attribution;
- sarcasm, humor, parody, hyperbole, and understatement;
- metaphor, ambiguity, quotation, and characterization;
- translation, punctuation, textual variants, and ordinary inconsistency.

Tone alone cannot trigger LC-011.

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
3. `CANDIDATE_IRONIC_DIVERGENCE`
4. `CORROBORATED_IRONIC_DIVERGENCE`

No outcome establishes intended irony, intended meaning, hidden teaching,
authorial position, or a canonical subtype.

## Run tests

```bash
python -m pip install -e '.[dev]'
pytest -q
```

## Next production unit

Operationalize **LC-012 — Apostrophe to the Reader** while distinguishing
documented reader-address functions from generic rhetorical address.
