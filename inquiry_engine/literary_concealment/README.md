# Literary Concealment Integration

This directory preserves the independently completed development packages for
`LC-001` through `LC-022` and records their integration into the Custos Inquiry
Engine.

## Authority boundary

Repository integration means that the files are versioned, importable, and
tested together. It does **not** mean that the underlying Hermeneutic Object or
any LC component has received:

- a canonical identifier;
- constitutional admission;
- certification;
- Cognitive Memory integration;
- production-engine authorization.

All components remain `DEVELOPMENT_ONLY`. The authoritative human-readable
source remains:

`engine_training/Hermeneutic_Object_Strauss_Taxonomy_of_Literary_Concealment_v1.0.txt`

## Preserved source packages

The `packages/` directory preserves the submitted operationalization packages.
Their original directory structures and source files remain documentary input
to this integration. The upload commits on `main` preserve the exact submitted
state.

## Active engine projection

The active development integration is under:

`inquiry_engine/src/custos_engine/literary_concealment/`

Each technique has an isolated namespace (`lc001` through `lc022`) so that its
models, outcome vocabulary, and evaluator cannot overwrite or silently merge
with those of another technique. `registry.py` supplies bounded discovery,
loading, schema access, and dispatch across the 22 isolated runtimes.

The integration tests are under:

`inquiry_engine/tests/literary_concealment/`

`INTEGRATION_MANIFEST.json` records the source and active paths and their
cryptographic hashes. `INTEGRATION_AUDIT.md` records the cross-package findings
and the limits of this action.
