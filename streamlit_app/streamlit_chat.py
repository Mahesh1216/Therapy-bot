import streamlit as st
import requests

# Persona options
PERSONAS = {
    "professional": "Professional Therapist",
    "companion": "Companion & Friendly Therapist",
    "yap": "Yap (Gen-Z Friend)"
}

st.title("Therapeutic Chatbot")

# Session state for chat history and persona
if "messages" not in st.session_state:
    st.session_state.messages = []
if "persona" not in st.session_state:
    st.session_state.persona = "professional"

# Persona selection (locked after first message)
if not st.session_state.messages:
    persona = st.selectbox("Choose a persona", list(PERSONAS.keys()), format_func=lambda x: PERSONAS[x])
    st.session_state.persona = persona
else:
    st.write(f"**Persona:** {PERSONAS[st.session_state.persona]} (locked for this session)")

# Chat history display
for msg in st.session_state.messages:
    if msg["sender"] == "user":
        st.markdown(f"**You:** {msg['text']}")
    else:
        st.markdown(f"**Bot:** {msg['text']}")

# Input box
user_input = st.text_input("Type your message...", key="input")

if st.button("Send") and user_input.strip():
    # Add user message to history
    st.session_state.messages.append({"text": user_input, "sender": "user"})
    # Prepare payload for FastAPI backend
    payload = {
        "message": user_input,
        "history": [m["text"] for m in st.session_state.messages if m["sender"] == "user"],
        "persona": st.session_state.persona
    }
    try:
        response = requests.post(
            "http://127.0.0.1:8000/api/v1/chat",
            json=payload,
            timeout=30
        )
        if response.ok:
            data = response.json()
            st.session_state.messages.append({"text": data["response"], "sender": "bot"})
        else:
            st.session_state.messages.append({"text": "Sorry, backend error.", "sender": "bot"})
    except Exception as e:
        st.session_state.messages.append({"text": f"Error: {e}", "sender": "bot"})

# New session button
if st.button("New Session"):
    st.session_state.messages = []
    st.session_state.persona = "professional"
    st.experimental_rerun()
