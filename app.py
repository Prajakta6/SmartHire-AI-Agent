import os
import requests
import streamlit as st
from interview_agent import MockInterviewAgent
from questions import questions
from report_generator import save_report

def check_ollama_status() -> bool:
    """Checks if the local Ollama server is running on port 11434."""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        return response.status_code == 200
    except requests.RequestException:
        return False

# ========================
# Streamlit Page Setup
# ========================
st.set_page_config(page_title="SmartHire AI Agent", page_icon="🤖", layout="centered")
st.title("🤖 SmartHire AI Agent")
st.caption("Local LLM-Powered Mock Technical Interview Assistant (Ollama • Llama 3)")

# ========================
# Session State Initialization
# ========================
if "started" not in st.session_state:
    st.session_state.started = False
if "completed" not in st.session_state:
    st.session_state.completed = False
if "agent" not in st.session_state:
    st.session_state.agent = None
if "questions_queue" not in st.session_state:
    st.session_state.questions_queue = []
if "current_idx" not in st.session_state:
    st.session_state.current_idx = 0
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "saved_filepath" not in st.session_state:
    st.session_state.saved_filepath = None
if "saved_report_content" not in st.session_state:
    st.session_state.saved_report_content = None

# ========================
# Sidebar: Setup & Status
# ========================
with st.sidebar:
    st.header("⚙️ Interview Setup")

    # Ollama Server Health Check
    if check_ollama_status():
        st.success("🟢 Ollama Server: Connected (Llama 3)")
    else:
        st.error("🔴 Ollama Server: Offline. Run `ollama serve` in terminal.")

    student_name = st.text_input(
        "Student Name",
        placeholder="e.g., Prajakta",
        disabled=st.session_state.started,
    )

    interview_mode = st.radio(
        "Select Interview Mode",
        ["Full Interview", "Topic-wise Interview"],
        disabled=st.session_state.started,
    )

    # Extract unique topics preserving order from questions.py
    available_topics = list(dict.fromkeys(q["topic"] for q in questions))
    selected_topic = None
    if interview_mode == "Topic-wise Interview":
        selected_topic = st.selectbox(
            "Choose Topic",
            available_topics,
            disabled=st.session_state.started,
        )

    st.divider()

    # Start Interview Button
    if st.button("Start Interview", type="primary", use_container_width=True, disabled=st.session_state.started):
        if not student_name.strip():
            st.warning("Please enter the Student Name first.")
        else:
            # Filter questions based on selected mode
            if interview_mode == "Full Interview":
                queue = list(questions)
            else:
                queue = [q for q in questions if q["topic"] == selected_topic]

            # Initialize your MockInterviewAgent
            st.session_state.agent = MockInterviewAgent(student_name.strip())
            st.session_state.questions_queue = queue
            st.session_state.started = True
            st.session_state.current_idx = 0

            first_q = queue[0]
            welcome_msg = (
                f"Welcome **{student_name.strip()}**! Starting your **{interview_mode}**.\n\n"
                f"**Question 1 of {len(queue)}** *(Topic: {first_q['topic']})*:\n\n"
                f"{first_q['question']}"
            )
            st.session_state.chat_messages.append({"role": "assistant", "content": welcome_msg})
            st.rerun()

    # Reset Button
    if st.button("Reset / New Interview", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# ========================
# Main Interview Area
# ========================
if not st.session_state.started:
    st.info("👈 Enter your name, select an interview mode in the sidebar, and click **Start Interview**.")
else:
    agent = st.session_state.agent
    total_q = len(st.session_state.questions_queue)
    answered_q = len(agent.history)

    # Progress Bar & Live Metrics from MockInterviewAgent
    st.progress(answered_q / total_q if total_q else 0)

    col1, col2, col3 = st.columns(3)
    col1.metric("Progress", f"{answered_q} / {total_q}")
    col2.metric("Total Score", f"{agent.total_score} / {answered_q * 10 if answered_q else 0}")
    if answered_q > 0:
        avg_score = agent.total_score / answered_q
        col3.metric("Average Score", f"{avg_score:.2f} / 10")
    else:
        col3.metric("Average Score", "—")

    st.divider()

    # Display Chat History
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Candidate Answer Input
    if not st.session_state.completed:
        if user_answer := st.chat_input("Type your answer here..."):
            current_q_obj = st.session_state.questions_queue[st.session_state.current_idx]

            # Show user answer in chat
            st.session_state.chat_messages.append({"role": "user", "content": user_answer})
            with st.chat_message("user"):
                st.markdown(user_answer)

            # Call MockInterviewAgent.evaluate_answer()
            with st.spinner("Evaluating your answer with Llama 3..."):
                evaluation_text = agent.evaluate_answer(
                    topic=current_q_obj["topic"],
                    question=current_q_obj["question"],
                    answer=user_answer,
                )

            # Advance to next question or finalize report
            st.session_state.current_idx += 1
            if st.session_state.current_idx < total_q:
                next_q_obj = st.session_state.questions_queue[st.session_state.current_idx]
                reply = (
                    f"### 📝 Evaluation\n{evaluation_text}\n\n---\n"
                    f"**Question {st.session_state.current_idx + 1} of {total_q}** *(Topic: {next_q_obj['topic']})*:\n\n"
                    f"{next_q_obj['question']}"
                )
            else:
                st.session_state.completed = True

                # Generate and save report using your exact backend methods
                raw_report = agent.generate_final_report()
                saved_path = save_report(agent.student_name, raw_report)
                st.session_state.saved_filepath = saved_path

                # Read the saved file so the download button includes your branding headers/footers
                with open(saved_path, "r", encoding="utf-8") as f:
                    st.session_state.saved_report_content = f.read()

                reply = (
                    f"### 📝 Final Question Evaluation\n{evaluation_text}\n\n---\n"
                    f"🎉 **Interview Completed!** Your report has been saved to `{saved_path}`."
                )

            st.session_state.chat_messages.append({"role": "assistant", "content": reply})
            st.rerun()

# ========================
# Final Report Section
# ========================
if st.session_state.completed and st.session_state.saved_filepath:
    st.success(f"Report saved locally at: `{st.session_state.saved_filepath}`")

    with st.expander("📄 Preview Full Interview Report", expanded=True):
        st.text(st.session_state.saved_report_content)

    st.download_button(
        label="⬇️ Download Interview Report (.txt)",
        data=st.session_state.saved_report_content,
        file_name=os.path.basename(st.session_state.saved_filepath),
        mime="text/plain",
        type="primary",
    )
