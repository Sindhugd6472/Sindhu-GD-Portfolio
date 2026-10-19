import json
import os
from abc import ABC, abstractmethod

from dotenv import load_dotenv

from .prompts import SYSTEM_PROMPT, build_prompt

load_dotenv()


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, requirement: str) -> str:
        raise NotImplementedError


class MockLLMProvider(LLMProvider):
    """Deterministic offline provider for demos and tests."""

    def generate(self, requirement: str) -> str:
        payload = {
            "requirement": requirement,
            "assumptions": [
                "The sample requirement describes APB-style transfer behavior."
            ],
            "tests": [
                {
                    "test_name": "basic_transfer",
                    "objective": "Verify a normal transfer completes when the required phases occur and ready is asserted.",
                    "category": "positive",
                    "priority": "high",
                    "preconditions": ["Interface is out of reset."],
                    "stimulus": [
                        "Assert select to start a transfer.",
                        "Assert enable in the access phase.",
                        "Assert ready to complete the transfer."
                    ],
                    "expected_result": [
                        "The transfer completes only when ready is high."
                    ],
                    "coverage_points": [
                        "Cover a completed transfer with no wait state."
                    ],
                    "assertion_ideas": [
                        "Candidate property: access phase follows a selected setup phase."
                    ],
                    "rationale": "This is the fundamental transaction path."
                },
                {
                    "test_name": "wait_state_transfer",
                    "objective": "Verify the transfer remains active while ready is low.",
                    "category": "positive",
                    "priority": "high",
                    "preconditions": ["A transfer has entered the access phase."],
                    "stimulus": [
                        "Keep ready low for multiple cycles.",
                        "Then assert ready."
                    ],
                    "expected_result": [
                        "The transfer does not complete while ready is low.",
                        "The transfer completes when ready becomes high."
                    ],
                    "coverage_points": ["Cover multiple wait-state lengths."],
                    "assertion_ideas": [
                        "Candidate property: completion must not occur while ready is low."
                    ],
                    "rationale": "Wait-state handling is a common protocol corner case."
                },
                {
                    "test_name": "enable_phase_check",
                    "objective": "Check setup-to-access sequencing for enable.",
                    "category": "negative",
                    "priority": "high",
                    "preconditions": ["Interface is out of reset."],
                    "stimulus": [
                        "Create a selected setup phase and observe the following access phase."
                    ],
                    "expected_result": [
                        "The expected setup-to-access ordering is preserved."
                    ],
                    "coverage_points": ["Cover setup followed by access."],
                    "assertion_ideas": [
                        "Candidate property: selected setup phase implies enable in the following access phase."
                    ],
                    "rationale": "Phase sequencing is central to the stated transfer behavior."
                },
                {
                    "test_name": "error_response",
                    "objective": "Verify an error indication is observed on an error response.",
                    "category": "error",
                    "priority": "medium",
                    "preconditions": ["The requirement supports an error indication."],
                    "stimulus": [
                        "Complete a transfer while asserting the error response signal."
                    ],
                    "expected_result": [
                        "The completing transfer is identified as an error response."
                    ],
                    "coverage_points": ["Cover successful and error responses."],
                    "assertion_ideas": [
                        "Candidate property: error indication is sampled on a completing transfer."
                    ],
                    "rationale": "The requirement explicitly identifies an error-response signal."
                },
                {
                    "test_name": "back_to_back_transfers",
                    "objective": "Exercise consecutive legal transfers.",
                    "category": "stress",
                    "priority": "medium",
                    "preconditions": ["Interface supports consecutive transfers."],
                    "stimulus": [
                        "Issue multiple transfers with minimal idle time between them."
                    ],
                    "expected_result": [
                        "Each transfer follows required setup, access, and completion behavior."
                    ],
                    "coverage_points": ["Cover consecutive completed transfers."],
                    "assertion_ideas": [
                        "Candidate property: every access phase corresponds to a selected transfer."
                    ],
                    "rationale": "Repeated transactions can expose sequencing bugs."
                },
                {
                    "test_name": "completion_condition",
                    "objective": "Verify ready is required for transfer completion.",
                    "category": "coverage",
                    "priority": "high",
                    "preconditions": ["A transfer is active."],
                    "stimulus": ["Toggle ready across active transfer cycles."],
                    "expected_result": [
                        "Completion is observed only in a cycle where ready is high."
                    ],
                    "coverage_points": ["Cross access phase with ready low and high."],
                    "assertion_ideas": [
                        "Candidate property: transfer completion implies ready."
                    ],
                    "rationale": "This directly targets the stated completion rule."
                }
            ]
        }
        return json.dumps(payload, indent=2)


class OpenAIProvider(LLMProvider):
    def __init__(self) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set.")

        from openai import OpenAI

        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-6-luna")

    def generate(self, requirement: str) -> str:
        response = self.client.responses.create(
            model=self.model,
            instructions=SYSTEM_PROMPT,
            input=build_prompt(requirement),
        )
        return response.output_text


def get_provider(name: str | None = None) -> LLMProvider:
    provider_name = (name or os.getenv("MODEL_PROVIDER", "mock")).strip().lower()

    if provider_name == "mock":
        return MockLLMProvider()
    if provider_name == "openai":
        return OpenAIProvider()

    raise ValueError(f"Unsupported MODEL_PROVIDER: {provider_name}")
