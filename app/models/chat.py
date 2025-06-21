from pydantic import BaseModel, Field
from typing import Literal

class ChatMessage(BaseModel):
    """
    Represents a single chat message from the user.
    """
    message: str = Field(..., min_length=1)
    history: list[str] = []
    persona: Literal["professional", "companion", "yap"] = Field(..., description="Persona to use for this session.")


class ChatResponse(BaseModel):
    """
    Represents a response from the chatbot.
    """
    response: str