# Custos Inquiry Engine

A narrow, local, deterministic Python scaffold for the Strauss Inquiry Engine.

## Governing boundary

The runtime operates against:

1. a **declared local Git repository**;
2. a **declared immutable governed repository Git commit**;
3. a **declared immutable manifest Git commit**;
4. a **declared repository-relative Cognitive Memory Manifest path**;
5. a **declared repository-relative Cognitive Memory Manifest schema path**;
6. a **declared repository-relative Taxonomy schema path**;
7. the Taxonomy source path declared by `taxonomy_source.github_path`;
8. the Taxonomy source commit declared by `taxonomy_source.git_commit`;
9. a **declared repository-relative Procedure schema path**;
10. the Procedure source path declared by `procedure_source.github_path`;
11. the Procedure source commit declared by `procedure_source.git_commit`;
12. an optional **declared immutable projection Git commit**;
13. an optional **declared repository-relative Projection Manifest path**;
14. an optional **declared repository-relative Projection Manifest schema path**.

It never reads from the moving repository head after a run begins.

GitHub remains the canonical documentary record. Neo4j remains a derived projection. The engine creates candidate outputs only; it does not certify or admit them.

## Structure

```text
inquiry_engine/
  pyproject.toml
  README.md
  src/custos_engine/
    config/
    models/
    schemas/
    repository/
    graph/
    cognition/
    runtime/
    outputs/
    cli.py
  tests/
    unit/
    integration/
    taxonomy/
    negative/
    fixtures/
```

## Install locally

From inside this directory:

```bash
python -m pip install -e ".[dev]"
```

Neo4j support is optional:

```bash
python -m pip install -e ".[dev,neo4j]"
```

## Create a development run

The repository must already be cloned locally.

```bash
custos-inquiry run \
  --mode DEVELOPMENT \
  --repo-root /path/to/custos \
  --git-commit <governed-commit-sha> \
  --manifest-git-commit <manifest-commit-sha> \
  --manifest tests/fixtures/cognitive_memory_manifest.json \
  --manifest-schema inquiry_engine/src/custos_engine/schemas/cognitive_memory_manifest.schema.json \
  --taxonomy-schema inquiry_engine/src/custos_engine/schemas/taxonomy_component.schema.json \
  --procedure-schema inquiry_engine/src/custos_engine/schemas/procedure.schema.json \
  --question tests/fixtures/inquiry.json \
  --output runs/RUN-000000001
```

The command:

- verifies the declared governed repository commit;
- verifies the declared manifest commit used to pin both the Manifest and Manifest schema;
- loads the Manifest and its validating schema through the pinned manifest commit and repository-relative paths;
- loads the Taxonomy source and Taxonomy schema through the governed `git_commit` using the Taxonomy source path declared by `taxonomy_source.github_path`;
- verifies that `taxonomy_source.git_commit` matches the governed repository commit;
- loads the Procedure source and Procedure schema through the governed `git_commit` using the Procedure source path declared by `procedure_source.github_path`;
- verifies that `procedure_source.git_commit` matches the governed repository commit;
- verifies that the Manifest `repository_commit` matches the governed repository commit;
- reads canonical files through `git show <commit>:<path>`;
- freezes the run configuration;
- executes the deterministic state-machine scaffold;
- writes an auditable candidate inquiry package.

Working-tree edits to the Manifest or Manifest schema cannot affect an Inquiry Run because both artifacts are read from the declared immutable `manifest_git_commit` snapshot.
Working-tree edits to either the Taxonomy source or the Taxonomy schema cannot affect an Inquiry Run because both are read through the same `LocalGitReader` pinned to `git_commit`.
Working-tree edits to either the Procedure source or the Procedure schema cannot affect an Inquiry Run because both are read through the same `LocalGitReader` pinned to `git_commit`.

## Create a production run

A released Cognitive Memory Manifest can govern production without a graph
projection. Neo4j remains an optional, separately pinned retrieval aid.

```bash
custos-inquiry run \
  --mode PRODUCTION \
  --repo-root /path/to/custos \
  --git-commit <governed-commit-sha> \
  --manifest-git-commit <manifest-commit-sha> \
  --manifest manifests/cognitive-memory/MAN-000000001.json \
  --manifest-schema inquiry_engine/src/custos_engine/schemas/cognitive_memory_manifest.schema.json \
  --taxonomy-schema inquiry_engine/src/custos_engine/schemas/taxonomy_component.schema.json \
  --procedure-schema inquiry_engine/src/custos_engine/schemas/procedure.schema.json \
  --question tests/fixtures/inquiry.json \
  --output runs/RUN-000000001
```

### Add an optional projection

```bash
custos-inquiry run \
  --mode PRODUCTION \
  --repo-root /path/to/custos \
  --git-commit <governed-commit-sha> \
  --manifest-git-commit <manifest-commit-sha> \
  --manifest tests/fixtures/cognitive_memory_manifest.json \
  --manifest-schema inquiry_engine/src/custos_engine/schemas/cognitive_memory_manifest.schema.json \
  --taxonomy-schema inquiry_engine/src/custos_engine/schemas/taxonomy_component.schema.json \
  --procedure-schema inquiry_engine/src/custos_engine/schemas/procedure.schema.json \
  --projection-git-commit <projection-commit-sha> \
  --projection-manifest projections/projection_manifest.json \
  --projection-manifest-schema inquiry_engine/src/custos_engine/schemas/projection_manifest.schema.json \
  --question tests/fixtures/inquiry.json \
  --output runs/RUN-000000001
```

When projection inputs are configured, `projection_git_commit` pins both the Projection Manifest and the Projection Manifest schema.

Working-tree edits to either projection artifact cannot affect an Inquiry Run because both are read via `git show <projection_git_commit>:<path>` through one pinned reader.

The Projection Manifest is validated against three bindings before use:

- `projection.git_commit` equals the governed repository commit;
- `projection.cognitive_memory_manifest_id` equals the loaded Cognitive Memory Manifest ID;
- `projection.repository_full_name` equals the loaded Cognitive Memory Manifest repository full name.

## Run tests

```bash
pytest
```

## Present implementation boundary

Implemented:

- strict configuration;
- authority policy;
- canonical models;
- JSON Schemas;
- commit-pinned repository reader;
- manifest validation;
- repository-backed, commit-pinned Taxonomy loading;
- repository-backed, commit-pinned Procedure loading;
- technically certified LC-001–LC-022 combined runtime;
- isolated component models and evaluators for LC-001–LC-022;
- bounded Literary Concealment registry and dispatcher;
- deterministic Taxonomy evaluator;
- deterministic state-machine scaffold;
- candidate package exporter;
- projection-plan and integrity utilities;
- CLI;
- baseline tests.

Not yet implemented:

- Taxonomy population beyond LC-022;
- LLM reasoning adapters;
- production Neo4j projection;
- GitHub writes.

The paired cognitive layer now includes:

- HOC-000000001 as the bounded Inner Sanctum;
- IAR-000000001 as the ten-phase, thirty-seven-step Outer Process;
- an enforced gate that denies Taxonomy invocation until documentary
  difficulty, historical admissibility, authorial authorization, ordinary
  alternatives, and an evidence path have been recorded;
- REG-000000004 as the Cognitive Memory Register; and
- MAN-000000001 as the released, commit-pinned production Manifest.

## Literary Concealment integration status

LC-001 through LC-022 are technically certified as one combined executable
subsystem. Each component retains its own schema, Pydantic models, evaluator,
bounded outcome vocabulary, fixtures, and tests under an isolated namespace.
GitHub Actions runs the complete Inquiry Engine suite for every relevant pull
request and push to `main`.

The repository maintains one active integrated implementation rather than
duplicate package trees. Technical certification does not expand an
evaluator's epistemic authority or itself constitute constitutional admission
or Cognitive Memory integration. No next LC component is authorized by this
change.
