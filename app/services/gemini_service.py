from typing import List, Optional
from google.generativeai import GenerativeModel, configure
import logging
from app.prompts.personas import PERSONA_PROMPTS


def _format_history(prompt: str, history: List[str]) -> list:
    """
    Format the chat history for Gemini API. The first message is the persona prompt as a 'user' message.
    All history items are treated as user messages for simplicity.
    """
    formatted = []
    # Add persona prompt as the first user message
    formatted.append({"role": "user", "parts": [prompt]})
    # Add each history message as a user message
    for msg in history:
        formatted.append({"role": "user", "parts": [msg]})
    return formatted

class GeminiService:
    def __init__(self, api_key: str):
        configure(api_key=api_key)
        self.model = GenerativeModel('gemini-2.5-flash')

    async def generate_response(self, message: str, history: List[str], persona: str) -> str:
        try:
            prompt = PERSONA_PROMPTS.get(persona, PERSONA_PROMPTS["professional"])
            formatted_history = _format_history(prompt, history)
            chat = self.model.start_chat(history=formatted_history)
            response = await chat.send_message_async({"role": "user", "parts": [message]})
            # Extract text from Gemini response
            if hasattr(response, 'text'):
                return response.text
            elif hasattr(response, 'candidates') and response.candidates:
                return response.candidates[0].text
            else:
                return "Sorry, I couldn't generate a response."
        except Exception as e:
            logging.error(f"GeminiService error: {e}")
            print("GeminiService error:", e)
            return "Sorry, there was an error processing your request."


from app.core.config import settings

def get_gemini_service():
    """
    Dependency injector for the GeminiService.
    """
    return GeminiService(api_key=settings.GEMINI_API_KEY)