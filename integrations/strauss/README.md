# Strauss harness consumer

`izzy9118-blip/Strauss` uses this repository's Strauss Reader for source examination.
Custos owns the reading instructions, five-stage outer protocol, literary inventory,
and Reader execution. Strauss owns ministerial context and reporting. This integration
does not make a Reader result an admitted or certified Strauss finding.

The public activation interface is:

```bash
custos --repo-root /path/to/custos context
```

It emits `custos.reader-context.v1` with full current `CUSTOS.md` wording, repository
commit, configuration, both gates, and SHA-256 hashes of all four authority documents.
It loads no default source or inquiry, creates no run, and claims no analysis.

Reader requests (`custos.reader-request.v1`) carry the same full instructions and
authority hashes, so an external reasoner does not need filesystem access to Custos.

After activation the consumer supplies exactly one source or registered Custos inquiry
to the existing `prepare` or `read` command, with `--mode close` or `--mode sweep`.
`prepare` stops at `PREPARED_FOR_REASONER`. `read` executes the supplied reasoner and
validates its structured response before writing `examination.md` and the completion
record. The consumer must propagate failures and must not call preparation analysis.

Strauss pins a tested Custos commit in its reader binding. Updating that pin is a
Strauss repository change; this repository has no reverse dependency on Strauss and
no global active inquiry. The active conversational reasoner can consume the same
instructions and gates when reading directly with the user.
