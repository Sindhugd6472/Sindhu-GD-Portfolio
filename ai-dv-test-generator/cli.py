import argparse

from src.generator import generate_plan, plan_to_json


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate an AI-assisted design verification test plan."
    )
    parser.add_argument("requirement", help="Natural-language hardware requirement")
    parser.add_argument(
        "--provider",
        choices=["mock", "openai"],
        default="mock",
        help="Model provider",
    )
    args = parser.parse_args()

    plan = generate_plan(args.requirement, args.provider)
    print(plan_to_json(plan))


if __name__ == "__main__":
    main()
