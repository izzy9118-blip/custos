# Custos

## A living documentary inquiry into Leo Strauss’s practice of reading

> **We examine the text together; GitHub remembers the inquiry.**

Custos is a research repository built to reconstruct Leo Strauss’s mode of
inquiry as accurately as the documentary evidence permits.

The project has two inseparable activities:

1. **Shared textual examination.** Custos reads Strauss in the user’s
   presence, follows his citations, reconstructs the cited authors, states and
   tests the strongest reading, and preserves uncertainty. The user may
   intervene, disagree, correct, or redirect at any point.
2. **Documentary preservation.** GitHub records the sources, witnesses,
   provenance, versions, disagreements, decisions, and limits needed for
   another investigator to reproduce the inquiry.

Custos is not a Strauss persona, an automated summary generator, or a system
for producing hidden teachings on demand. Its software, schemas, graph, and
governance exist only to support disciplined reading and to preserve its path.

The structural maxim remains:

> **The corpus governs the system; the system exists to serve the inquiry.**

## The ordinary unit: a Citation Object

A Citation Object begins from a complete documentary unit established by
Strauss—normally one governing passage together with one complete note. It
does not begin from an isolated quotation, an attractive theme, or a
conclusion selected in advance.

Each Citation Object moves through five stages:

1. **First encounter with Strauss:** Establish the exact passage, immediate
   context, complete note, and explicit citations. Expose and begin examining
   the problem before allowing the cited source to settle its meaning.
2. **Documentary recovery:** Fix identifiable textual witnesses; record
   editions, translations, locations, hashes, editorial work, OCR limits, and
   unresolved source problems.
3. **Independent reconstruction:** Read and reconstruct each cited author in
   that author’s own context and terms before comparing the author with
   Strauss.
4. **Comparative return to Strauss:** Return to Strauss and ask what remained
   constant, what changed, what was selected or omitted, and how following the
   citation transformed the reader’s understanding.
5. **Preservation of the inquiry:** Record evidence, readings, alternatives,
   disagreements, uncertainty, and contribution provenance without forcing
   consensus.

Documentary preparation may be done independently. Substantive inquiry must be
conducted openly in the shared conversation rather than hidden inside a
finished report. Fixing witnesses, filling fields, passing validation, or
committing a candidate does not substitute for examining the central textual
problem. User response is not a gate: Custos bears responsibility for stating
and testing the strongest warranted reading, and the user may intervene.

## Documentary discipline

Custos is governed by the following commitments:

- Primary texts govern secondary sources.
- Documentary evidence precedes interpretation.
- Each author is reconstructed independently before comparison.
- Quotations, contexts, translations, editorial interventions, and
  interpretations remain distinguishable.
- Selection, omission, placement, sequence, repetition, and contradiction are
  preserved as documentary facts before their significance is inferred.
- Missing evidence limits conclusions; it does not license speculation.
- Earlier records are never silently rewritten. Corrections proceed forward
  through linked versions.
- Architecture grows only when actual inquiry demonstrates a need.

Substantive propositions must be identified by kind:

| Kind | Function |
|---|---|
| **Documented Finding** | States what the fixed documentary evidence directly supports. |
| **Supported Inference** | Offers a cautious synthesis built from documented findings. |
| **Working Hypothesis** | Directs further investigation without claiming evidentiary authority. |
| **Comparative Question** | Preserves a text-grounded problem that Custos must investigate and may leave open when the evidence does not resolve it. |
| **Unresolved Uncertainty** | Records a material limit, ambiguity, or missing source. |

Custos also distinguishes an AI judgment, an express user reading, and a
judgment tested together. User silence is neither a blocker nor agreement. No
proposition may silently rise above its evidence or be attributed to the user
without support in the inquiry record.

## Outer Process and Inner Sanctum

The ordinary documentary process is mandatory. It establishes the boundary,
fixes the texts, reconstructs the authors, maps the work’s architecture,
considers ordinary explanations, and forms the genuine problem.

The Inner Sanctum is closed by default. Literary concealment may be
investigated only after the governed documentary phases establish a real
difficulty, historical admissibility, authorial authorization, failed ordinary
explanations, and an auditable evidence path. Opening the gate authorizes a
bounded inquiry—not a conclusion about concealment.

See the active
[Inquiry Architecture Record](records/inquiry-architecture/IAR-000000001.yaml)
and the bounded
[Hermeneutic Object](registers/hermeneutic-object-register/objects/HOC-000000001.yaml).

## Canonical lifecycle

Repository states are not interchangeable:

```text
proposed → produced → validated → committed → admitted → certified
```

A commit proves that an artifact was preserved in GitHub. It does not, by
itself, admit or certify the artifact. Investigation, preservation, validation,
admission, and certification remain distinct functions, and certification is
always limited to an expressly stated scope.

The released cognitive-memory entrypoint is
[MAN-000000001](manifests/cognitive-memory/MAN-000000001.json). The current
ChatGPT Project governance package is
[SPEC-000000004](records/specifications/SPEC-000000004.yaml), certified within
the limits stated by
[CER-000000003](records/certifications/CER-000000003.yaml).

## Current production stage

- **Work:** Leo Strauss, *Thoughts on Machiavelli*, Chapter I, note 1
- **Strauss’s cited passages:** *The Prince*, chapters 1, 2, and 8, beginnings
- **Current state:** `DOCUMENTARY_PREPARATION_READY_FOR_AI_LED_SHARED_EXAMINATION`

The Strauss anchor, complete note boundary, Ricci/Vincent witness, OCR limits,
and recovered English chapter openings have been admitted and certified only
as a bounded Evidence Record:
[EVR-000000001](records/evidence/EVR-000000001.yaml).

The first procedural correction that restored shared examination is admitted
and certified as
[COR-000000002](records/corrections/COR-000000002.yaml). The forward correction
that prevents shared examination from becoming user interrogation is
[COR-000000003](records/corrections/COR-000000003.yaml).

The Citation Object itself is **not complete, admitted, or certified**. It has
no canonical Citation Object identifier. Primary-language verification against
a fixed Italian witness remains unresolved, and the Inner Sanctum decision has
not been reached.

### Resume the inquiry here

Open the historical
[Chapter I, Citation 1 Shared Examination Packet](candidates/citation-objects/chapter-01-citation-01-shared-examination-correction-v1.0.md)
with its
[Interpretive-Initiative Correction](candidates/citation-objects/chapter-01-citation-01-interpretive-initiative-correction-v1.1.md).

Custos must begin by stating and testing its strongest reading of Strauss’s
**“Above all”** and the beginnings of *The Prince* chapters 1, 2, and 8. The
packet’s Comparative Questions are problems for Custos to work through, not a
questionnaire for the user. Custos should continue through the textual evidence
unless the user chooses to intervene.

Do not replace this stage with another source-recovery report or a forced-choice
question. Read Strauss first, follow the three citations, reconstruct
Machiavelli, test the strongest alternative, and then return to Strauss.

## Start or resume work

### Bootstrap a fresh runtime

A new Work environment may have a compatible Python interpreter but none of
Custos's declared packages. From the repository root, bootstrap the Inquiry
Engine before treating missing imports as a blocker:

```bash
python inquiry_engine/bootstrap.py
```

The command creates an isolated `.venv`, installs `inquiry_engine[dev]`, fetches
full Git history when a shallow clone cannot resolve the repository's pinned
commits, runs the complete Inquiry Engine test suite, and verifies the
`custos-inquiry` CLI. Missing declared dependencies alone are ordinary
environment setup—not a runtime defect or lawful stop. Stop only if the
installation or validation command actually fails, and preserve its exact
command and error output.

Before changing the repository:

1. Confirm the repository is `izzy9118-blip/custos`.
2. Inspect `main`, the current branch, `HEAD`, relevant files, and their
   lifecycle states.
3. Verify read and write capability separately.
4. Create or confirm a working branch from the verified base before
   substantive production, unless the repository owner expressly authorizes a
   direct change.
5. Read the active governing package:
   - [Custos Codex v1.0](candidates/chatgpt-project/v1.0/Custos_Codex_Complete_v1.0.txt)
   - [Amendment 001 — Shared Textual Examination](candidates/chatgpt-project/v1.1/Custos_Codex_Amendment_001_Shared_Textual_Examination_v1.0.txt)
   - [Amendment 002 — Interpretive Initiative](candidates/chatgpt-project/v1.2/Custos_Codex_Amendment_002_Interpretive_Initiative_v1.0.txt)
   - [Project Instructions v1.2](candidates/chatgpt-project/v1.2/Custos_ChatGPT_Project_Instructions_v1.2.txt)
   - [Startup Procedure v1.2](candidates/chatgpt-project/v1.2/Custos_Project_Startup_Procedure_v1.2.txt)
6. Resume the last evidenced production phase. Do not redesign the system or
   skip the Shared-Examination Gate. Do not turn that gate into a request for
   the user to perform or approve the interpretation.

Every work session should end with the exact state reached, affected paths,
validation evidence, branch and commit SHA when applicable, preserved
uncertainties, and the next authorized unit.

## Repository map

| Path | Purpose |
|---|---|
| `candidates/` | Produced work awaiting or preserving later lifecycle action. |
| `records/` | Structured evidence, decisions, corrections, validations, versions, admissions, and certifications. |
| `governance/` | Human-readable ratification, admission, integration, and certification decisions. |
| `registers/` | Controlled documentary and cognitive-memory registers. |
| `ledgers/` | Append-only identifier assignments and audit history. |
| `manifests/` | Released, commit-pinned entrypoints for governed runtime use. |
| `engine_training/` | Documentary findings and methodological training materials. |
| `inquiry_engine/` | Deterministic local software for bounded, reproducible candidate production. |

## Inquiry Engine

The Inquiry Engine is an instrument of reconstruction, not the project’s
purpose or authority. It reads declared immutable Git commits, runs the bounded
documentary process, enforces the Inner Sanctum gate, and exports auditable
candidate packages. It cannot admit or certify its own output.

Neo4j, when used, is a derived and rebuildable retrieval projection. Git
remains the source of documentary evidence.

Installation, commands, implementation boundaries, and tests are documented in
the [Inquiry Engine README](inquiry_engine/README.md).

## Status of this README

This README is an orientation and navigation document. It does not replace the
governing instruments or structured lifecycle records linked above. If a
summary here conflicts with a certified record, the certified record governs
and this README must be corrected forward.
