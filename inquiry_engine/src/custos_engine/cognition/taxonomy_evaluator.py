from __future__ import annotations

from custos_engine.models.taxonomy import TaxonomyComponent, TaxonomyEvaluation


def evaluate_taxonomy_component(
    component: TaxonomyComponent,
    observed_features: set[str],
) -> TaxonomyEvaluation:
    """Deterministic threshold evaluator; it does not infer hidden teaching."""

    triggers = set(component.minimum_trigger_features)
    corroboration = set(component.required_corroboration_features)
    disqualifiers = set(component.disqualifying_conditions)

    matched_triggers = sorted(triggers.intersection(observed_features))
    missing_triggers = sorted(triggers.difference(observed_features))
    matched_corroboration = sorted(corroboration.intersection(observed_features))
    matched_disqualifiers = sorted(disqualifiers.intersection(observed_features))

    minimum_satisfied = not missing_triggers
    disqualifier_present = bool(matched_disqualifiers)

    if not minimum_satisfied:
        triggered = False
        conclusion = "Minimum documentary trigger is not satisfied."
        action = None
    elif disqualifier_present:
        triggered = False
        conclusion = "A disqualifying ordinary explanation is present."
        action = None
    elif corroboration and not matched_corroboration:
        triggered = False
        conclusion = "Trigger is present, but required corroboration is absent."
        action = None
    else:
        triggered = True
        conclusion = (
            "The component is eligible for bounded investigation; "
            "no conclusion about concealed teaching is authorized."
        )
        action = component.authorized_engine_action

    return TaxonomyEvaluation(
        component_id=component.component_id,
        triggered=triggered,
        minimum_trigger_satisfied=minimum_satisfied,
        corroboration_count=len(matched_corroboration),
        disqualifier_present=disqualifier_present,
        matched_features=sorted(set(matched_triggers + matched_corroboration)),
        missing_features=missing_triggers,
        matched_disqualifiers=matched_disqualifiers,
        authorized_action=action,
        conclusion=conclusion,
    )
