import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(
    page_title="AI Mental Health Therapist",
    layout="wide",
)

st.title("🧠 SafeSpace – AI Mental Health Therapist")
st.caption("A supportive AI companion for mental well-being")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
# chat input
user_input = st.chat_input("What's on your mind today?")

if user_input:
    st.session_state.chat_history.append(
        {"role": "user", "content": user_input}
    )

    with st.spinner("Thinking…"):
        try:
            response = requests.post(
                BACKEND_URL,
                json={"message": user_input},
                timeout=60,
            )
            response.raise_for_status()
            data = response.json()

            assistant_message = data.get("response", "I couldn't generate a response.")
            tool_used = data.get("tool_called", "None")

        except requests.exceptions.RequestException as e:
            assistant_message = (
                "I'm having trouble reaching the server right now. "
                "Please try again in a moment."
            )
            tool_used = "error"

    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "content": assistant_message,
            "tool": tool_used,
        }
    )

# displaying chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant" and msg.get("tool"):
            st.caption(f"🛠 Tool used: {msg['tool']}")
