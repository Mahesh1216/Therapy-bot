from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import chat

app = FastAPI(
    title="Therapeutic Chatbot API",
    description="An API for providing therapeutic support through AI personas.",
    version="0.1.0",
)

# CORS configuration
origins = [
    "http://localhost:8501",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/v1")

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to ensure the server is running.

    Returns:
        dict: A dictionary with the status of the server.
    """
    return {"status": "ok"}