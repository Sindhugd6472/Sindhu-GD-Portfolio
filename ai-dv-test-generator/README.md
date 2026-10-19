# AI-Powered Design Verification Test Generator

An AI-assisted verification planning tool for hardware and IP requirements.

The tool accepts a natural-language verification requirement and produces a structured candidate verification plan with positive, negative, boundary, error, stress, and coverage-oriented scenarios. It also suggests functional coverage points and candidate assertion ideas.

The project is intentionally human-in-the-loop. AI output is treated as a starting point for a verification engineer to review, not as automatically correct verification content.

## Why this belongs in a verification portfolio

Modern verification work includes translating specifications into test plans, coverage goals, assertions, and regressions. This project explores how AI can assist that planning work while preserving engineering review.

It demonstrates:
- verification planning
- coverage-driven thinking
- assertion-based verification concepts
- Python automation
- structured data validation
- AI-assisted engineering workflows
- user-facing tooling with Streamlit

## Main flow

Requirement -> Prompt Builder -> LLM Provider -> Structured JSON -> Schema Validation -> Verification Plan -> UI / JSON / CSV export

Two providers are included:
- mock: deterministic offline demo mode, no API key required
- openai: optional model-backed generation using the OpenAI Responses API

## Quick start

1. Open a terminal in this folder.
2. Create a Python virtual environment.
3. Install dependencies with: pip install -r requirements.txt
4. Run: streamlit run app.py

The default provider is mock, so the application works without an API key.

To use an OpenAI model:
1. Copy .env.example to .env
2. Set MODEL_PROVIDER=openai
3. Set OPENAI_API_KEY to your API key
4. Optionally change OPENAI_MODEL
5. Run streamlit run app.py

## Example requirement

APB transfer behavior:

A transfer starts when PSEL is asserted. PENABLE must be asserted in the access phase. The transfer completes only when PREADY is high. PSLVERR indicates an error response.

The generated plan can include:
- normal transfer
- delayed PREADY / wait-state handling
- setup-to-access sequencing
- error-response handling
- back-to-back transfers
- completion-condition coverage
- candidate SVA concepts

## Output fields

Each generated test contains:
- test name
- objective
- category
- priority
- preconditions
- stimulus
- expected result
- functional coverage ideas
- candidate assertion ideas
- rationale

## Project structure

ai-dv-test-generator/
- app.py: Streamlit interface
- cli.py: command-line interface
- requirements.txt: Python dependencies
- .env.example: environment configuration template
- src/models.py: Pydantic data schema
- src/prompts.py: verification-focused prompt construction
- src/validators.py: JSON/schema validation
- src/llm.py: mock and OpenAI provider implementations
- src/generator.py: generation and export logic
- sample_requirements/apb_requirement.md: demo requirement
- tests/: unit tests

## Engineering guardrails

LLMs can hallucinate protocol behavior, invent unsupported corner cases, or generate invalid assertions. This project therefore:
- keeps the original requirement visible
- records assumptions explicitly
- validates output structure before use
- labels assertion ideas as candidates
- requires human review
- defaults to an offline mock provider
- warns against sending proprietary specifications to external models

Do not paste confidential employer specifications or internal IP documentation into this project or an external AI service.

## Future extensions

Possible next versions:
- requirement-to-test traceability matrix
- spec section IDs and coverage mapping
- UVM sequence skeleton generation
- SVA candidate generation with syntax checks
- duplicate test detection
- coverage-gap-driven test suggestions
- simulator feedback loop
- regression result feedback
- local-model support

## Interview explanation

A concise way to describe the project:

"I built an AI-assisted design verification planning tool that converts natural-language hardware requirements into structured verification scenarios, coverage ideas, and candidate assertion concepts. I added schema validation, an offline mock mode, a Streamlit interface, and JSON/CSV export. I kept a human-review step because AI-generated verification content can be technically incorrect."

## Status

Portfolio MVP. The current version focuses on verification-plan generation rather than automatic RTL verification.
