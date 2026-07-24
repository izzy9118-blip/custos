# Custos

Custos is a documentary reading system for reconstructing Leo Strauss's practice of inquiry.

> We examine the text; Git records the inquiry.

## Start here

An LLM or investigator reads exactly one active instruction file:

1. [`CUSTOS.md`](CUSTOS.md) — governing instructions.
2. [`custos.yaml`](custos.yaml) — machine-readable configuration.
3. The active inquiry named in `custos.yaml`.

Historical systems before this rewrite are preserved in Git and on the branch
`archive/pre-streamline-custos-2026-07-23`. They do not govern the active tree.

## Method

Each inquiry follows five stages:

1. encounter Strauss;
2. recover the documentary chain;
3. reconstruct each cited author independently;
4. return comparatively to Strauss;
5. preserve findings, alternatives, and uncertainty.

The literary-technique inventory is available throughout all five stages. Its
availability is not evidence that a technique is present. Evidence alone may
activate a bounded technique evaluation.

## Current inquiry

[`Thoughts on Machiavelli`, Chapter I, note 1](inquiries/thoughts-on-machiavelli/chapter-01-note-01/inquiry.md)

## Commands

```bash
python -m pip install -e '.[dev]'
custos validate
custos show
custos analyze
pytest
```

`custos analyze` automatically loads the repository configuration, records the
current Git commit, verifies source excerpts, and writes an auditable request
package. Add `--reasoner-command` to execute an external JSON reasoner.

Sanctum federation is isolated under [`integrations/sanctum`](integrations/sanctum/README.md).
It does not govern ordinary Custos reading.
