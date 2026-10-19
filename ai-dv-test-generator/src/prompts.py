SYSTEM_PROMPT = """You help a hardware design verification engineer create a candidate verification plan.

Rules:
- Use only the requirement provided by the user.
- Do not invent protocol requirements that are not stated.
- If an assumption is necessary, list it explicitly.
- Generate a balanced set of positive, negative, boundary, error, stress, and coverage-oriented scenarios when supported.
- Candidate SVA ideas are conceptual suggestions, not proven-correct properties.
- Keep a human verification engineer in the review loop.
- Return JSON only.
"""


def build_prompt(requirement: str) -> str:
    return f"""Create a structured design-verification test plan for the requirement below.

REQUIREMENT:
{requirement}

Return one JSON object with exactly this shape:

{{
  "requirement": "<original requirement>",
  "assumptions": ["<explicit assumption if needed>"],
  "tests": [
    {{
      "test_name": "<short snake_case name>",
      "objective": "<what behavior is being verified>",
      "category": "positive|negative|boundary|error|stress|coverage",
      "priority": "high|medium|low",
      "preconditions": ["<setup>"],
      "stimulus": ["<ordered action>"],
      "expected_result": ["<observable expected behavior>"],
      "coverage_points": ["<candidate functional coverage idea>"],
      "assertion_ideas": ["<candidate SVA concept>"],
      "rationale": "<why this test matters>"
    }}
  ]
}}

Generate 6 to 10 useful tests. Avoid duplicates. Do not add facts that are not supported by the requirement.
"""
