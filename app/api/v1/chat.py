from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from app.models.chat import ChatMessage, ChatResponse
from app.services.gemini_service import GeminiService, get_gemini_service
import logging

router = APIRouter()

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
        response_text = await gemini_service.generate_response(
            message=message.message,
            history=message.history,
            persona=message.persona
        )
        return ChatResponse(response=response_text)
    except Exception as e:
        logging.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred.")