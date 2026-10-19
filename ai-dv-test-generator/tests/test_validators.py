import pytest

from src.validators import PlanValidationError, parse_and_validate_plan


def test_rejects_invalid_json():
    with pytest.raises(PlanValidationError):
        parse_and_validate_plan("not-json")


def test_accepts_valid_minimal_plan():
    raw = """
    {
      "requirement": "A transfer completes only when ready is asserted.",
      "assumptions": [],
      "tests": [
        {
          "test_name": "ready_completion",
          "objective": "Verify completion requires ready.",
          "category": "positive",
          "priority": "high",
          "preconditions": ["Transfer is active."],
          "stimulus": ["Toggle ready."],
          "expected_result": ["Completion occurs only with ready."],
          "coverage_points": ["Cover ready low and high."],
          "assertion_ideas": ["Candidate property: complete implies ready."],
          "rationale": "Directly checks the stated requirement."
        }
      ]
    }
    """

    plan = parse_and_validate_plan(raw)
    assert plan.tests[0].test_name == "ready_completion"
