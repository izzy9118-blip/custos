# Custos

Custos is a documentary reading system for reconstructing Leo Strauss's practice of inquiry.

> We examine the text; Git records the inquiry.

## Start here

An LLM or investigator reads:

1. [`CUSTOS.md`](CUSTOS.md) — governing Reader instructions.
2. [`custos.yaml`](custos.yaml) — machine-readable repository roots and protocol paths.
3. The source witness or registered inquiry named explicitly for the current run.

Custos has no global active inquiry. A Reader run must receive either `--source` or
`--inquiry`; changing books never requires rewriting `custos.yaml`.

Historical systems before this rewrite are preserved in Git and on the branch
`archive/pre-streamline-custos-2026-07-23`. They do not govern the active tree.

## Reader modes

The Strauss Reader has two complementary modes.

### Close mode

Close mode performs one slow, bounded textual act. It fixes the immediate evidence,
forms the documentary problem, reconstructs relevant sources independently, returns
to Strauss, tests the strongest rival, records uncertainty, and names the next textual
act. It is designed for methodical examination that can continue with the user over
successive runs.

```bash
custos read --mode close --source "city and man ce.txt" \
  --reasoner-command "your-json-reasoner"

custos read --mode close \
  --inquiry inquiries/thoughts-on-machiavelli/chapter-01-note-01 \
  --reasoner-command "your-json-reasoner"
```

A completed close run must contain substantive examination. It ends with
`CLOSE_READING_ACT_COMPLETE`, never `READY_FOR_REASONER`.

### Sweep mode

Sweep mode examines the supplied witness as a whole. It compiles divisions, citations,
recurring terms, beginnings and endings, architectural patterns, documentary anomalies,
and candidate bounded inquiries.

The sweep passes the whole text through two gates:

- **Outer gate:** the ordered documentary inquiry sequence in `protocol/reading.yaml`.
- **Inner gate:** the source-derived literary discernment inventory in
  `protocol/literary-techniques.yaml`.

The inner gate is always available but activates a named technique only when fixed
textual evidence warrants it. A sweep maps and prioritizes the work; it does not pretend
that every candidate problem has received a complete close reading.

```bash
custos read --mode sweep --source "city and man ce.txt" \
  --reasoner-command "your-json-reasoner"
```

A completed sweep ends with `WHOLE_TEXT_SWEEP_COMPLETE` and identifies the first
warranted close-reading act.

## Preparation is not analysis

`custos prepare` writes the complete Reader request for an external or conversational
reasoner. It deliberately stops at `PREPARED_FOR_REASONER` and makes no claim that the
text has been analyzed.

```bash
custos prepare --mode close --source "city and man ce.txt"
custos prepare --mode sweep --source "city and man ce.txt"
```

`custos read` is the analysis command. It requires a reasoner and must produce
`reader-response.json`, `examination.md`, and a completed run record.

## Method

Each bounded inquiry follows five stages:

1. encounter Strauss;
2. recover the documentary chain;
3. reconstruct each cited author independently;
4. return comparatively to Strauss;
5. preserve findings, alternatives, and uncertainty.

The literary-technique inventory is available throughout all five stages. Its
availability is not evidence that a technique is present. Evidence alone may activate
a bounded technique evaluation.

## Commands

```bash
python -m pip install -e '.[dev]'
custos validate
custos validate --inquiry inquiries/thoughts-on-machiavelli/chapter-01-note-01
custos show --inquiry inquiries/thoughts-on-machiavelli/chapter-01-note-01
custos prepare --mode close --source path/to/witness.txt
custos read --mode close --source path/to/witness.txt --reasoner-command "..."
custos read --mode sweep --source path/to/witness.txt --reasoner-command "..."
pytest
```

Sanctum federation remains isolated under [`integrations/sanctum`](integrations/sanctum/README.md).
It does not govern ordinary Custos reading. Its substantive Strauss Minister will be
rebuilt separately after the Reader is complete.
