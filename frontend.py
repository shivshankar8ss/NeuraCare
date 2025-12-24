import streamlit as st
import requests
BACKEND_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(
    page_title="NeuraCare",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# css for ui
st.markdown(
    """
    <style>
    /* App background */
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: #ffffff;
    }

    /* Title */
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(90deg, #7f7fd5, #86a8e7, #91eae4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.2em;
    }

    .subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #d1d5db;
        margin-bottom: 2rem;
    }

    /* Chat bubbles */
    .chat-bubble {
        padding: 1rem 1.2rem;
        border-radius: 16px;
        margin-bottom: 1rem;
        max-width: 80%;
        line-height: 1.5;
        font-size: 1rem;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }

    .user-bubble {
        background: rgba(255, 255, 255, 0.15);
        margin-left: auto;
        border-top-right-radius: 4px;
    }

    .assistant-bubble {
        background: rgba(0, 0, 0, 0.35);
        margin-right: auto;
        border-top-left-radius: 4px;
    }

    /* Tool badge */
    .tool-badge {
        display: inline-block;
        margin-top: 0.4rem;
        padding: 0.25rem 0.6rem;
        font-size: 0.75rem;
        border-radius: 999px;
        background: rgba(145, 234, 228, 0.2);
        color: #91eae4;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# heading
st.markdown('<div class="main-title">🧠 NeuraCare</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">AI that listens. Support that cares.</div>',
    unsafe_allow_html=True,
)


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# chat input
user_input = st.chat_input("Share what’s on your mind…")

if user_input:
    st.session_state.chat_history.append(
        {"role": "user", "content": user_input}
    )

    with st.spinner("Thinking with care…"):
        try:
            response = requests.post(
                BACKEND_URL,
                json={"message": user_input},
                timeout=60,
            )
            response.raise_for_status()
            data = response.json()

            assistant_message = data.get(
                "response",
                "I couldn't generate a response right now.",
            )
            tool_used = data.get("tool_called", "None")

        except requests.exceptions.RequestException:
            assistant_message = (
                "I'm having trouble reaching the server right now. "
                "Please try again shortly."
            )
            tool_used = "error"

    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "content": assistant_message,
            "tool": tool_used,
        }
    )

# -----------------------------
# Render chat history
# -----------------------------
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(
            f"""
            <div class="chat-bubble user-bubble">
                {msg["content"]}
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        tool_html = ""
        if msg.get("tool"):
            tool_html = f'<div class="tool-badge">🛠 {msg["tool"]}</div>'

        st.markdown(
            f"""
            <div class="chat-bubble assistant-bubble">
                {msg["content"]}
                {tool_html}
            </div>
            """,
            unsafe_allow_html=True,
        )
