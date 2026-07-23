from __future__ import annotations

import json
import math
import subprocess
from datetime import datetime, timezone
from typing import Any, Protocol, Sequence

from custos_engine.cognition.hermeneutic_gate import EPISTEMIC_LIMIT
from custos_engine.models.base import EpistemicClassification, InquiryState
from custos_engine.models.inquiry import InquiryRun, StateTransition
from custos_engine.models.reasoning import (
    DocumentaryInput,
    PhaseInstruction,
    PhaseReasoningRecord,
    PhaseReasoningRequest,
    PhaseReasoningResponse,
)
from custos_engine.models.taxonomy import TaxonomyComponent

from .state_machine import InquiryStateMachine


class PhaseReasoner(Protocol):
    adapter_id: str

    def reason(self, request: PhaseReasoningRequest) -> PhaseReasoningResponse: ...


def validate_reasoning_response(
    request: PhaseReasoningRequest,
    response: PhaseReasoningResponse,
) -> None:
    if response.run_id != request.run_id:
        raise ValueError("Reasoner response run_id does not match the request")
    if response.state != request.state:
        raise ValueError("Reasoner response state does not match the request")

    permitted_technique_ids = {
        component.component_id for component in request.permitted_taxonomy_techniques
    }
    unauthorized = sorted(
        set(response.requested_taxonomy_technique_ids).difference(
            permitted_technique_ids
        )
    )
    if unauthorized:
        raise PermissionError(
            "Reasoner requested unauthorized Taxonomy techniques: "
            + ", ".join(unauthorized)
        )

    supplied_evidence_ids = {
        documentary_input.evidence_id
        for documentary_input in request.documentary_inputs
    }
    unknown_evidence_ids = sorted(
        {
            evidence_id
            for statement in response.candidate_statements
            for evidence_id in statement.evidence_record_ids
        }.difference(supplied_evidence_ids)
    )
    if unknown_evidence_ids:
        raise ValueError(
            "Reasoner cited evidence absent from the fixed documentary inputs: "
            + ", ".join(unknown_evidence_ids)
        )


class SubprocessPhaseReasoner:
    """Provider-neutral JSON adapter whose outputs confer no engine authority."""

    adapter_id = "SUBPROCESS_JSON_V1"

    def __init__(
        self,
        command: Sequence[str],
        timeout_seconds: float = 120.0,
        max_response_bytes: int = 1_000_000,
    ) -> None:
        if not command:
            raise ValueError("Reasoner command must not be empty")
        if timeout_seconds <= 0 or not math.isfinite(timeout_seconds):
            raise ValueError("Reasoner timeout must be positive")
        if max_response_bytes <= 0:
            raise ValueError("Reasoner response limit must be positive")
        self.command = tuple(command)
        self.timeout_seconds = timeout_seconds
        self.max_response_bytes = max_response_bytes

    def reason(self, request: PhaseReasoningRequest) -> PhaseReasoningResponse:
        try:
            completed = subprocess.run(
                self.command,
                input=json.dumps(request.model_dump(mode="json"), ensure_ascii=False),
                text=True,
                capture_output=True,
                timeout=self.timeout_seconds,
                check=False,
                shell=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError(
                f"Reasoner timed out after {self.timeout_seconds:g} seconds"
            ) from exc
        except OSError as exc:
            raise RuntimeError("Reasoner process could not be started") from exc

        if completed.returncode != 0:
            raise RuntimeError(
                f"Reasoner exited unsuccessfully with status {completed.returncode}"
            )
        if not completed.stdout.strip():
            raise RuntimeError("Reasoner returned no JSON response")
        if len(completed.stdout.encode("utf-8")) > self.max_response_bytes:
            raise RuntimeError("Reasoner response exceeds the configured size limit")

        try:
            raw = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            raise RuntimeError("Reasoner returned invalid JSON") from exc

        response = PhaseReasoningResponse.model_validate(raw)
        validate_reasoning_response(request, response)
        return response


class InquiryReasoningExecutor:
    def __init__(
        self,
        reasoner: PhaseReasoner,
        state_machine: InquiryStateMachine | None = None,
    ) -> None:
        self.reasoner = reasoner
        self.state_machine = state_machine or InquiryStateMachine()

    @staticmethod
    def _phase_map(procedure: dict[str, Any]) -> dict[InquiryState, dict[str, Any]]:
        stages = procedure.get("ordered_stages")
        if not isinstance(stages, list):
            raise ValueError("Procedure ordered_stages must be an array")

        phase_map: dict[InquiryState, dict[str, Any]] = {}
        for phase in stages:
            state = InquiryState(phase["state"])
            if state in phase_map:
                raise ValueError(f"Procedure repeats inquiry state {state}")
            phase_map[state] = phase

        expected = set(InquiryState).difference(
            {InquiryState.CERTIFICATION_PREPARATION, InquiryState.TERMINATED}
        )
        missing = sorted(state.value for state in expected.difference(phase_map))
        if missing:
            raise ValueError(f"Procedure is missing reasoning phases: {missing}")
        return phase_map

    @staticmethod
    def _record_candidate_ids(
        run: InquiryRun,
        response: PhaseReasoningResponse,
    ) -> None:
        for statement in response.candidate_statements:
            run.candidate_statement_ids.append(statement.candidate_id)
            if (
                statement.epistemic_classification
                == EpistemicClassification.UNRESOLVED_QUESTION
            ):
                run.unresolved_questions.append(statement.text)
        run.unresolved_questions.extend(response.unresolved_questions)

    @staticmethod
    def _terminate_from_response(
        run: InquiryRun,
        response: PhaseReasoningResponse,
    ) -> None:
        if response.termination_reason is None:
            raise ValueError("Incomplete reasoning response lacks a termination reason")
        prior = run.current_state
        run.termination_reason = response.termination_reason
        run.current_state = InquiryState.TERMINATED
        run.state_history.append(
            StateTransition(
                from_state=prior,
                to_state=InquiryState.TERMINATED,
                reason=response.summary,
            )
        )
        run.updated_at = datetime.now(timezone.utc)

    def run_to_termination(
        self,
        run: InquiryRun,
        procedure: dict[str, Any],
        documentary_inputs: list[DocumentaryInput],
        *,
        inner_sanctum_authorized: bool = True,
        permitted_taxonomy_techniques: Sequence[TaxonomyComponent] = (),
        maximum_steps: int = 32,
    ) -> list[PhaseReasoningRecord]:
        if not inner_sanctum_authorized:
            raise ValueError(
                "The Inner Sanctum cannot be closed during a text-analysis run"
            )

        techniques = list(permitted_taxonomy_techniques)
        if not techniques:
            raise ValueError(
                "Text analysis requires the always-open Inner Sanctum Taxonomy"
            )
        technique_ids = [component.component_id for component in techniques]
        if len(technique_ids) != len(set(technique_ids)):
            raise ValueError("Taxonomy technique identifiers must be unique")

        phase_map = self._phase_map(procedure)
        records: list[PhaseReasoningRecord] = []
        prior_summaries: list[str] = []
        seen_candidate_ids: set[str] = set()

        for _ in range(maximum_steps):
            if run.current_state == InquiryState.TERMINATED:
                return records
            if run.current_state == InquiryState.CERTIFICATION_PREPARATION:
                self.state_machine.step(run)
                continue

            phase = phase_map[run.current_state]
            phase_number = int(phase["phase"])
            request = PhaseReasoningRequest(
                run_id=run.run_id,
                repository_full_name=run.repository_full_name,
                git_commit=run.git_commit,
                cognitive_memory_manifest_id=run.cognitive_memory_manifest_id,
                governing_specification_ids=run.governing_specification_ids,
                state=run.current_state,
                phase_number=phase_number,
                phase_name=phase["name"],
                instructions=[
                    PhaseInstruction.model_validate(step) for step in phase["steps"]
                ],
                initiating_question=run.initiating_question,
                documentary_boundary=run.documentary_boundary,
                documentary_inputs=documentary_inputs,
                prior_phase_summaries=prior_summaries,
                inner_sanctum_authorized=True,
                permitted_taxonomy_techniques=techniques,
                epistemic_limit=EPISTEMIC_LIMIT,
            )
            response = self.reasoner.reason(request)
            validate_reasoning_response(request, response)
            candidate_ids = {
                statement.candidate_id for statement in response.candidate_statements
            }
            repeated_candidate_ids = sorted(candidate_ids.intersection(seen_candidate_ids))
            if repeated_candidate_ids:
                raise ValueError(
                    "Reasoner repeated candidate identifiers across phases: "
                    + ", ".join(repeated_candidate_ids)
                )
            seen_candidate_ids.update(candidate_ids)
            record_id = f"{run.run_id}-PHASE-{phase_number:02d}"
            records.append(
                PhaseReasoningRecord(
                    record_id=record_id,
                    adapter_id=self.reasoner.adapter_id,
                    request=request,
                    response=response,
                )
            )
            run.reasoning_record_ids.append(record_id)
            self._record_candidate_ids(run, response)
            prior_summaries.append(response.summary)

            if not response.completed:
                self._terminate_from_response(run, response)
                return records
            self.state_machine.step(run)

        raise RuntimeError(
            f"Reasoning inquiry did not terminate within {maximum_steps} steps"
        )
