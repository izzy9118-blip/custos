from __future__ import annotations

from custos_engine.models.artifacts import ValidationIssue, ValidationReport


def report_from_errors(
    validation_id: str,
    target_id: str,
    errors: list[str],
) -> ValidationReport:
    return ValidationReport(
        validation_id=validation_id,
        target_id=target_id,
        valid=not errors,
        issues=[
            ValidationIssue(
                code="VALIDATION_ERROR",
                severity="ERROR",
                message=message,
            )
            for message in errors
        ],
    )
