import csv
import io

from .llm import get_provider
from .models import VerificationPlan
from .validators import parse_and_validate_plan


def generate_plan(
    requirement: str, provider_name: str | None = None
) -> VerificationPlan:
    cleaned = requirement.strip()
    if len(cleaned) < 10:
        raise ValueError("Please enter a more detailed requirement.")

    provider = get_provider(provider_name)
    raw = provider.generate(cleaned)
    return parse_and_validate_plan(raw)


def plan_to_json(plan: VerificationPlan) -> str:
    return plan.model_dump_json(indent=2)


def plan_to_csv(plan: VerificationPlan) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(
        [
            "test_name",
            "objective",
            "category",
            "priority",
            "preconditions",
            "stimulus",
            "expected_result",
            "coverage_points",
            "assertion_ideas",
            "rationale",
        ]
    )

    for test in plan.tests:
        writer.writerow(
            [
                test.test_name,
                test.objective,
                test.category,
                test.priority,
                " | ".join(test.preconditions),
                " | ".join(test.stimulus),
                " | ".join(test.expected_result),
                " | ".join(test.coverage_points),
                " | ".join(test.assertion_ideas),
                test.rationale,
            ]
        )

    return output.getvalue()
