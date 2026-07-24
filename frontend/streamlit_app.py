import streamlit as st
import requests

API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Travel Agent MVP", page_icon="🧳")
st.title("Travel Agent MVP")

SAMPLE_PROMPTS = [
    "Plan a four-day Goa trip from Delhi for two people under ₹40,000. We like beaches, local food, and a relaxed pace.",
    "Suggest and plan a three-day trip from Bengaluru under ₹25,000 for one person. I enjoy nature and quiet places.",
    "Plan a trip to Jaipur.",
    "Plan a seven-day international trip from Mumbai for two people under ₹20,000.",
    "Plan a five-day Kerala trip for a family of four.",
]


def start_new_session() -> str:
    response = requests.post(f"{API_BASE_URL}/sessions")
    response.raise_for_status()
    return response.json()["session_id"]


# Runs only once per browser tab — st.session_state persists across reruns
# but resets if the tab is closed or the page is reloaded.
if "session_id" not in st.session_state:
    st.session_state.session_id = start_new_session()
    st.session_state.messages = []

with st.sidebar:
    st.subheader("Sample prompts")
    for prompt in SAMPLE_PROMPTS:
        if st.button(prompt, use_container_width=True):
            st.session_state.pending_prompt = prompt

    st.divider()
    if st.button("Start new conversation"):
        st.session_state.session_id = start_new_session()
        st.session_state.messages = []
        st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Describe the trip you want to plan...")
if "pending_prompt" in st.session_state:
    user_input = st.session_state.pop("pending_prompt")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Planning..."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/chat",
                    json={
                        "session_id": st.session_state.session_id,
                        "message": user_input,
                    },
                    timeout=120,
                )
                if response.status_code == 200:
                    reply = response.json()["response"]
                    st.markdown(reply)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": reply}
                    )
                else:
                    detail = response.json().get("detail", "Unknown error")
                    st.error(f"Something went wrong: {detail}")
            except requests.exceptions.RequestException as e:
                st.error(f"Could not reach the backend: {e}")
