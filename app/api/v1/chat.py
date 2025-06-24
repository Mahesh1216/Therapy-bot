from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Optional
from app.models.chat import ChatMessage, ChatResponse
from app.services.gemini_service import GeminiService, get_gemini_service
from app.services.rag_service import RAGService
from app.core.config import Settings
import logging
import sqlite3
from datetime import datetime

router = APIRouter()
settings = Settings()
rag_service = RAGService(settings)

# Ensure feedback table exists
conn = sqlite3.connect('feedback.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    feedback TEXT,
    message TEXT,
    history TEXT
)''')
conn.commit()
conn.close()

@router.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat_with_bot(
    message: ChatMessage,
    gemini_service: GeminiService = Depends(get_gemini_service),
) -> ChatResponse:
    """
    Main chat endpoint to interact with the chatbot.

    Args:
        message (ChatMessage): The user's message.
        gemini_service (GeminiService): The Gemini service dependency.


    Returns:
        ChatResponse: The chatbot's response.
    """
    try:
        # 1. Query RAG for context
        context_chunks = rag_service.query(message.message, top_k=5)
        context_text = ""
        for i, chunk in enumerate(context_chunks, 1):
            title = chunk.get('source', '')
            context_text += f"[{i}] {chunk['text']} (Source: {title})\n"
        # 2. Compose the message for Gemini
        if context_text:
            gemini_input = (
                f"Context from therapy guides:\n{context_text}\n"
                "Use the above context to answer the user's question. "
                "If the context is not relevant, answer from your own knowledge.\n\n"
                f"User: {message.message}"
            )
        else:
            gemini_input = message.message
        # 3. Call Gemini
        response_text = await gemini_service.generate_response(
            message=gemini_input,
            history=message.history,
            persona=message.persona
        )
        return ChatResponse(response=response_text)
    except Exception as e:
        logging.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred.")

@router.post("/feedback", tags=["Feedback"])
async def feedback_endpoint(request: Request):
    data = await request.json()
    feedback = data.get("feedback")
    message = data.get("message")
    history = data.get("history", [])
    # Persist feedback to SQLite DB
    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    c.execute(
        "INSERT INTO feedback (timestamp, feedback, message, history) VALUES (?, ?, ?, ?)",
        (datetime.utcnow().isoformat(), feedback, message, str(history))
    )
    conn.commit()
    conn.close()
    logging.info(f"User feedback: {feedback} | Message: {message} | History: {history}")
    return {"status": "ok"}