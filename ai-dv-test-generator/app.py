import streamlit as st

from src.generator import generate_plan, plan_to_csv, plan_to_json

st.set_page_config(page_title="AI DV Test Generator", layout="wide")

st.title("AI-Powered Design Verification Test Generator")
st.caption(
    "Generate candidate verification scenarios, coverage ideas, and assertion concepts from a hardware requirement."
)

st.warning(
    "Generated content must be reviewed by a verification engineer. "
    "Do not paste confidential or proprietary specifications into external models."
)

default_requirement = """APB transfer behavior:
A transfer starts when PSEL is asserted. PENABLE must be asserted in the access phase.
The transfer completes only when PREADY is high. PSLVERR indicates an error response."""

requirement = st.text_area(
    "Verification requirement",
    value=default_requirement,
    height=180,
)

provider = st.selectbox(
    "Model provider",
    options=["mock", "openai"],
    help="Mock mode works offline. OpenAI mode requires OPENAI_API_KEY.",
)

if st.button("Generate verification plan", type="primary"):
    try:
        with st.spinner("Generating candidate verification plan..."):
            plan = generate_plan(requirement, provider)

        st.success(f"Generated {len(plan.tests)} candidate tests.")

        if plan.assumptions:
            st.subheader("Assumptions")
            for assumption in plan.assumptions:
                st.write(f"- {assumption}")

        st.subheader("Candidate tests")

        for index, test in enumerate(plan.tests, start=1):
            with st.expander(
                f"{index}. {test.test_name} - {test.category} / {test.priority}",
                expanded=index == 1,
            ):
                st.markdown(f"**Objective:** {test.objective}")

                st.markdown("**Preconditions**")
                for item in test.preconditions:
                    st.write(f"- {item}")

                st.markdown("**Stimulus**")
                for item in test.stimulus:
                    st.write(f"- {item}")

                st.markdown("**Expected result**")
                for item in test.expected_result:
                    st.write(f"- {item}")

                st.markdown("**Coverage ideas**")
                for item in test.coverage_points:
                    st.write(f"- {item}")

                st.markdown("**Candidate assertion ideas**")
                for item in test.assertion_ideas:
                    st.write(f"- {item}")

                st.markdown(f"**Rationale:** {test.rationale}")

        json_data = plan_to_json(plan)
        csv_data = plan_to_csv(plan)

        left, right = st.columns(2)
        with left:
            st.download_button(
                "Download JSON",
                data=json_data,
                file_name="verification_plan.json",
                mime="application/json",
            )
        with right:
            st.download_button(
                "Download CSV",
                data=csv_data,
                file_name="verification_plan.csv",
                mime="text/csv",
            )

    except Exception as exc:
        st.error(str(exc))
