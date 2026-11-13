
import streamlit as st
import pandas as pd
from pathlib import Path
from chatbot.chatbot import answer_prompt
from models.providers import ask_model
from agent.agent import handle_tool_request
from security.runner import run_suite

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="LLM & Agent Security Lab",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ LLM & Agentic AI Security Testing Lab")
st.caption(
    "Local proof of concept | Fictional data | Defensive testing only"
)

# --------------------------------------------------
# NAVIGATION TABS
# --------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs([
    "Chatbot",
    "Agent tools",
    "Run security tests",
    "Results"
])

# --------------------------------------------------
# TAB 1: CHATBOT
# --------------------------------------------------

with tab1:
    st.subheader("Fake Knowledge-Base Chatbot")

    model = "Gemini"

    st.info("Using Gemini API")

    hardened = st.toggle(
        "Enable mitigations",
        value=True,
        key="chat_hardened"
    )

    prompt = st.text_area(
        "Enter a test prompt",
        "What are Northstar's support hours?"
    )

    if st.button("Ask chatbot"):
        try:
            reply = answer_prompt(
                prompt,
                model,
                hardened,
                ask_model
            )

            st.subheader("Chatbot response")

            # Display model output as plain text.
            # Do not interpret model output as executable HTML.
            st.code(reply, language="text")

        except Exception as e:
            st.error(f"Chatbot error: {e}")


# --------------------------------------------------
# TAB 2: CONTROLLED AGENT TOOLS
# --------------------------------------------------

with tab2:
    st.subheader("Controlled Agent Tools")

    st.info(
        "Tools are local mocks. Email is draft-only; "
        "HTTP calls never leave this app."
    )

    tool = st.selectbox(
        "Select a tool",
        [
            "read_file",
            "draft_email",
            "http_get",
            "calculator"
        ]
    )

    hardened_agent = st.toggle(
        "Enforce tool allowlists and authorization",
        value=True
    )

    authorized = st.checkbox(
        "I explicitly authorize this demo action",
        value=False
    )

    args_text = st.text_area(
        "Tool arguments (JSON)",
        '{"filename":"public_faq.txt"}'
    )

    if st.button("Run tool"):
        import json

        try:
            arguments = json.loads(args_text)

            result = handle_tool_request(
                tool,
                arguments,
                hardened=hardened_agent,
                user_authorized=authorized
            )

            st.subheader("Tool result")
            st.json(result)

        except json.JSONDecodeError:
            st.error("Invalid JSON. Please check your tool arguments.")

        except Exception as e:
            st.error(f"Tool error: {e}")


# --------------------------------------------------
# TAB 3: AUTOMATED SECURITY TEST SUITE
# --------------------------------------------------

with tab3:
    st.subheader("Automated Security Attack Suite")

    st.write(
        "30 test cases × 1 model × 2 phases = 60 executions."
    )

    st.warning(
        "API usage may incur charges. "
        "Use only your own API key and fictional test data."
    )

    models = ["Gemini"]

    st.info("Security tests will run against Gemini only.")

    phases = st.multiselect(
        "Select testing phases",
        ["Before", "After"],
        default=["Before", "After"]
    )

    if st.button(
        "Start security test suite",
        type="primary",
        disabled=not phases
    ):
        progress_bar = st.progress(0)

        try:
            rows, path = run_suite(
                tuple(models),
                tuple(phases),
                progress=progress_bar.progress
            )

            st.success(
                f"Completed {len(rows)} executions. "
                f"Results saved to: {path}"
            )

            results_df = pd.DataFrame(rows)

            display_columns = [
                "Phase",
                "Risk_ID",
                "Case_ID",
                "Model",
                "Result",
                "Error"
            ]

            st.dataframe(
                results_df[display_columns],
                use_container_width=True
            )

        except Exception as e:
            st.error(f"Security test error: {e}")


# --------------------------------------------------
# TAB 4: RESULTS AND SUMMARY
# --------------------------------------------------

with tab4:
    st.subheader("Latest Security Test Results")

    results_path = Path("results/results.csv")

    if results_path.exists():

        try:
            df = pd.read_csv(results_path)

            st.dataframe(
                df,
                use_container_width=True
            )

            st.download_button(
                label="Download Results CSV",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name="results.csv",
                mime="text/csv"
            )

            st.subheader("Security Test Summary")

            if all(
                column in df.columns
                for column in ["Phase", "Model", "Result"]
            ):

                summary = (
                    df.groupby(
                        ["Phase", "Model", "Result"]
                    )
                    .size()
                    .reset_index(name="Count")
                )

                st.dataframe(
                    summary,
                    use_container_width=True
                )

            st.subheader("Risk-wise Summary")

            if all(
                column in df.columns
                for column in ["Risk_ID", "Phase", "Result"]
            ):

                risk_summary = (
                    df.groupby(
                        ["Risk_ID", "Phase", "Result"]
                    )
                    .size()
                    .reset_index(name="Count")
                )

                st.dataframe(
                    risk_summary,
                    use_container_width=True
                )

        except Exception as e:
            st.error(f"Could not read results: {e}")

    else:
        st.info(
            "No security test results found. "
            "Run the test suite first."
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "AI Security Internship POC | Gemini | "
    "Fictional demonstration environment"
)
