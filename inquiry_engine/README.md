# Custos Inquiry Engine

A narrow, local, deterministic Python scaffold for the Strauss Inquiry Engine.

## Governing boundary

The runtime operates against:

1. a **declared local Git repository**;
2. a **declared immutable governed repository Git commit**;
3. a **declared immutable manifest Git commit**;
4. a **declared repository-relative Cognitive Memory Manifest path**;
5. a **declared repository-relative Cognitive Memory Manifest schema path**;
6. an optional **declared Neo4j Projection Manifest**.

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
  --question tests/fixtures/inquiry.json \
  --output runs/RUN-000000001
```

The command:

- verifies the declared governed repository commit;
- verifies the declared manifest commit used to pin both the Manifest and Manifest schema;
- loads the Manifest and its validating schema through the pinned manifest commit and repository-relative paths;
- verifies that the Manifest `repository_commit` matches the governed repository commit;
- reads canonical files through `git show <commit>:<path>`;
- freezes the run configuration;
- executes the deterministic state-machine scaffold;
- writes an auditable candidate inquiry package.

Working-tree edits to the Manifest or Manifest schema cannot affect an Inquiry Run because both artifacts are read from the declared immutable `manifest_git_commit` snapshot.

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
- deterministic Taxonomy evaluator;
- deterministic state-machine scaffold;
- candidate package exporter;
- projection-plan and integrity utilities;
- CLI;
- baseline tests.

Not yet implemented:

- full Taxonomy population;
- full DF-000001–DF-000150 procedure;
- LLM reasoning adapters;
- production Neo4j projection;
- Repository admission or certification;
- GitHub writes.

## Immediate next production unit

Populate `taxonomy_component.schema.json` with the complete machine-readable projection of the Hermeneutic Object Taxonomy and add positive, negative, ambiguous, near-miss, and adversarial fixtures.
