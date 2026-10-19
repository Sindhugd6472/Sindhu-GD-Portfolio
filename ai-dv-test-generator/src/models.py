from typing import Literal

from pydantic import BaseModel, Field


Category = Literal["positive", "negative", "boundary", "error", "stress", "coverage"]
Priority = Literal["high", "medium", "low"]


class VerificationTest(BaseModel):
    test_name: str = Field(min_length=3)
    objective: str = Field(min_length=5)
    category: Category
    priority: Priority
    preconditions: list[str] = Field(default_factory=list)
    stimulus: list[str] = Field(default_factory=list)
    expected_result: list[str] = Field(default_factory=list)
    coverage_points: list[str] = Field(default_factory=list)
    assertion_ideas: list[str] = Field(default_factory=list)
    rationale: str = Field(min_length=5)


class VerificationPlan(BaseModel):
    requirement: str = Field(min_length=10)
    assumptions: list[str] = Field(default_factory=list)
    tests: list[VerificationTest] = Field(min_length=1)
