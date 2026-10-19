import json
from typing import Any

from pydantic import ValidationError

from .models import VerificationPlan


class PlanValidationError(ValueError):
    pass


def parse_and_validate_plan(raw_text: str) -> VerificationPlan:
    text = raw_text.strip()

    if text.startswith("~~~"):
        lines = text.splitlines()
        if lines and lines[0].startswith("~~~"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "~~~":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
        if text.lower().startswith("json"):
            text = text[4:].lstrip()

    try:
        payload: Any = json.loads(text)
    except json.JSONDecodeError as exc:
        raise PlanValidationError(f"Model output was not valid JSON: {exc}") from exc

    try:
        return VerificationPlan.model_validate(payload)
    except ValidationError as exc:
        raise PlanValidationError(
            f"Model output did not match the expected schema: {exc}"
        ) from exc
