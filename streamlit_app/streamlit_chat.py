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
for i, msg in enumerate(st.session_state.messages):
    if msg["sender"] == "user":
        st.markdown(f"**You:** {msg['text']}")
    else:
        st.markdown(f"**Healix:** {msg['text']}")
        # Feedback buttons for the last bot message
        if i == len(st.session_state.messages) - 1:
            if "feedback" not in st.session_state:
                st.session_state.feedback = []
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👍 Like", key=f"like_{i}"):
                    st.session_state.feedback.append({"msg_idx": i, "feedback": "like"})
                    # Send feedback to backend
                    requests.post(
                        "https://therapy-bot-o8uo.onrender.com/api/v1/feedback",
                        json={
                            "feedback": "like",
                            "message": st.session_state.messages[i]["text"],
                            "history": [m["text"] for m in st.session_state.messages[:i] if m["sender"] == "user"]
                        },
                        timeout=10
                    )
            with col2:
                if st.button("👎 Dislike", key=f"dislike_{i}"):
                    st.session_state.feedback.append({"msg_idx": i, "feedback": "dislike"})
                    # Send feedback to backend
                    requests.post(
                        "https://therapy-bot-o8uo.onrender.com/api/v1/feedback",
                        json={
                            "feedback": "dislike",
                            "message": st.session_state.messages[i]["text"],
                            "history": [m["text"] for m in st.session_state.messages[:i] if m["sender"] == "user"]
                        },
                        timeout=10
                    )

# Input box
if user_input := st.chat_input("Type your message..."):
    # Add user message to history
    st.session_state.messages.append({"text": user_input, "sender": "user"})

    # Prepare payload for FastAPI backend
    payload = {
        "message": user_input,
        "history": [m["text"] for m in st.session_state.messages if m["sender"] == "user"],
        "persona": st.session_state.persona
    }
    try:
        with st.spinner("Thinking..."):
            response = requests.post(
                "https://therapy-bot-o8uo.onrender.com/api/v1/chat",
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
    
    st.rerun()

# New session button
if st.button("New Session"):
    st.session_state.messages = []
    st.session_state.persona = "professional"
    st.rerun()
