# Hermeneutic Object LC-018 Operationalization — v0.1

This package operationalizes:

- **LC-018 — Rare Statement of the Unconventional Teaching**

## Strauss's rule of discernment

The authoritative Taxonomy records:

> Of two contradictory statements, the statement occurring least frequently is
> presumptively the one Maimonides considered true.

This package preserves that rule as a **rebuttable procedural presumption**.

It does not weaken the rule into mere frequency reporting, but it also does not
convert the presumption into adjudicated doctrinal truth.

## Required structure

The evaluator requires:

- exactly two contradictory proposition-families;
- aligned scope, modality, qualification, and attribution;
- at least one occurrence of each family;
- unequal occurrence counts;
- a complete occurrence index for the declared scope;
- independent evidence that the frequent family is conventional;
- independent evidence that the rarer family is unconventional;
- source-language, translation, witness, and negative-search review;
- testing of topic, genre, pedagogy, quotation, scope, classification, textual,
  and revision alternatives.

Frequency is counted by proposition-family, not raw words.

## Local outcomes

1. `NOT_TRIGGERED`
2. `BLOCKED_MISSING_EVIDENCE`
3. `CANDIDATE_RARITY_PRESUMPTION`
4. `CORROBORATED_RARITY_PRESUMPTION`

Candidate and corroborated outcomes may set:

`straussian_presumption_applicable = true`

They must also preserve:

`doctrinal_truth_selected = false`

## Distinctions

- LC-019 reconstructs frequent repetition of the conventional view.
- LC-018 supplies the rule of discernment favoring the rarer contradictory statement.
- LC-002 concerns unequal prominence, not work-wide frequency.
- LC-003 implicational occurrences require separate documentary reconstruction.

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

Operationalize **LC-019 — Frequent Repetition of the Conventional View** while
keeping it distinct from the LC-018 rule of discernment and from ordinary
pedagogical or topical repetition.
