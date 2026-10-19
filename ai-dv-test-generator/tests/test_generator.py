from src.generator import generate_plan, plan_to_csv, plan_to_json


REQUIREMENT = """APB transfer behavior:
A transfer starts when PSEL is asserted. PENABLE is asserted in the access phase.
The transfer completes only when PREADY is high. PSLVERR indicates an error response."""


def test_mock_generator_returns_plan():
    plan = generate_plan(REQUIREMENT, "mock")
    assert plan.requirement == REQUIREMENT
    assert len(plan.tests) >= 1


def test_exports_are_created():
    plan = generate_plan(REQUIREMENT, "mock")

    json_text = plan_to_json(plan)
    csv_text = plan_to_csv(plan)

    assert "basic_transfer" in json_text
    assert "test_name" in csv_text
    assert "basic_transfer" in csv_text
