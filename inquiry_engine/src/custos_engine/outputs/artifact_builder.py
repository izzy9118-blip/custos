from __future__ import annotations

from typing import Any

from custos_engine.models.artifacts import CandidateArtifact


def build_candidate_artifact(
    candidate_id: str,
    declared_class: str,
    title: str,
    run_id: str,
    content: dict[str, Any],
    documentary_basis_ids: list[str],
    governing_specification_ids: list[str],
) -> CandidateArtifact:
    return CandidateArtifact(
        candidate_id=candidate_id,
        declared_class=declared_class,
        title=title,
        run_id=run_id,
        content=content,
        documentary_basis_ids=documentary_basis_ids,
        governing_specification_ids=governing_specification_ids,
    )
