# PLANNING.md - Therapeutic Chatbot Project

> **AI ASSISTANT INSTRUCTIONS**: Always reference this document before providing code suggestions, architectural advice, or making technical decisions. Follow the constraints and patterns defined here.

## Project Vision

### Core Purpose
Build a therapeutic chatbot that provides genuine emotional support through three distinct personas, utilizing CBT (Cognitive Behavioral Therapy) techniques while maintaining absolute safety standards.

### Key Principles
- **Safety First**: Crisis detection and intervention is non-negotiable
- **Authentic Personas**: Each persona must feel genuinely different and helpful
- **CBT Integration**: Subtle but effective therapeutic techniques embedded naturally
- **User Experience**: Intuitive, welcoming, and genuinely supportive interface
- **Vibe Coding**: Prioritize what "feels right" over technical perfection

---

## AI CODING ASSISTANT RULES

### Code Generation Guidelines
- **Language**: Python 3.9+ for backend, React 18+ for frontend
- **Style**: Follow PEP 8 for Python, ESLint standards for JavaScript
- **Comments**: Include docstrings and inline comments for complex logic
- **Error Handling**: Always include try-catch blocks for external API calls
- **Security**: Never hardcode API keys, always use environment variables

### Architecture Constraints
- **Single Responsibility**: Each file should have one clear purpose
- **Dependency Injection**: Use FastAPI's dependency system
- **Type Hints**: Use Python type hints for all functions
- **Async/Await**: Use async patterns for all I/O operations
- **Testing**: Generate tests alongside main code

### Code Patterns to Follow
```python
# API Endpoint Pattern
@app.post("/chat/{persona}")
async def chat_endpoint(
    persona: PersonaType,
    message: ChatMessage,
    session: SessionDep,
    crisis_detector: CrisisDetectorDep
) -> ChatResponse:
    """Handle chat requests with proper error handling."""
    try:
        # Implementation here
        pass
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

### Prohibited Patterns
- ❌ No global variables
- ❌ No hardcoded strings for prompts (use config files)
- ❌ No direct database calls in API endpoints
- ❌ No synchronous I/O operations
- ❌ No missing error handling

---

## Architecture Overview

### System Components
```
Frontend (React) 
    ↓
Backend API (FastAPI)
    ↓
AI Engine (Gemini 2.5 Flash-Lite)
    ↓
Memory System (Pinecone Vector DB)
    ↓
Safety Layer (Crisis Detection)
```

### Core Modules
1. **Chat Handler** - Main conversation logic
2. **Persona Manager** - Switches between therapeutic personalities
3. **Memory System** - Conversation history and context retention
4. **Crisis Detector** - Multi-layered safety monitoring
5. **CBT Engine** - Therapeutic technique integration
6. **Response Generator** - Orchestrates all components

---

## Technical Stack

### Backend
- **Framework**: FastAPI (Python)
- **AI Model**: Google Gemini 2.5 Flash-Lite Preview 06-17
- **Vector DB**: Pinecone (for RAG and memory)
- **Environment**: Python 3.9+
- **Deployment**: Docker + Cloud service (TBD)

### Frontend
- **Framework**: React 18+
- **Styling**: Tailwind CSS
- **State Management**: React hooks (useState, useContext)
- **HTTP Client**: Axios
- **Build Tool**: Vite

### Development Tools
- **IDE**: AI-assisted IDE (Cursor, Windsurf, etc.)
- **Version Control**: Git with conventional commits
- **Environment**: Virtual environments (venv)
- **Testing**: Pytest for backend, Jest for frontend
- **Monitoring**: Structured logging with Python logging module
- **Code Quality**: Black formatter, isort, flake8

---

## Persona Definitions

### 1. Professional Therapist
- **Tone**: Warm, professional, evidence-based
- **Approach**: Structured CBT techniques, reflective listening
- **Use Case**: Users seeking formal therapeutic support
- **Example**: "I understand you're experiencing sadness. This feeling is valid and common. Let's explore what might be contributing to these emotions."

### 2. Companion & Friendly Therapist
- **Tone**: Caring, supportive, informal but knowledgeable
- **Approach**: Empathetic friend + subtle CBT integration
- **Use Case**: Users wanting supportive conversation
- **Example**: "Oh, I'm so sorry you're feeling that way... that sadness can feel so heavy sometimes, huh?"

### 3. Yap (Gen-Z Friend)
- **Tone**: Trendy, casual, validating with appropriate slang
- **Approach**: Peer support with CBT principles disguised as casual advice
- **Use Case**: Younger users or those preferring informal support
- **Example**: "Ah, ok bestie, I hear you—you're feeling kinda down, huh? That's totally valid, no cap."

---

## Safety & Crisis Management

### Crisis Detection Layers
1. **Keyword Detection**: Immediate flagging of crisis terms
2. **Sentiment Analysis**: Emotional intensity monitoring
3. **Pattern Recognition**: Conversation flow analysis
4. **Context Awareness**: Historical conversation patterns

### Crisis Response Protocol
1. **Immediate Support**: Acknowledge crisis, provide validation
2. **Resource Provision**: Share appropriate helpline numbers
3. **Escalation**: Encourage professional help when needed
4. **Documentation**: Log crisis interactions for improvement

### Emergency Resources
- **US**: National Suicide Prevention Lifeline: 988
- **Crisis Text**: Text HOME to 741741
- **Emergency**: 911
- **Additional**: Local resources based on user location

---

## Development Constraints

### Budget Considerations
- **API Costs**: Monitor Gemini API usage carefully
- **Infrastructure**: Start with free tiers (Pinecone, cloud hosting)
- **Scaling**: Design for gradual cost increase as users grow

### Time Constraints
- **Timeline**: 6-week development cycle
- **Approach**: Iterative development with weekly milestones
- **Scope**: MVP first, then feature expansion

### Technical Limitations
- **Experience Level**: Beginner-friendly approach required
- **Complexity**: Avoid over-engineering, focus on core functionality
- **Dependencies**: Minimize external dependencies

---

## Core Features (MVP)

### Essential Features
- [ ] Three distinct personas with consistent personalities
- [ ] Conversation memory and context retention
- [ ] Crisis detection and appropriate responses
- [ ] Basic CBT technique integration
- [ ] Clean, intuitive chat interface
- [ ] Secure API endpoints

### Nice-to-Have Features
- [ ] Mood tracking over time
- [ ] Personalized CBT exercise recommendations
- [ ] Multi-language support
- [ ] Voice chat capabilities
- [ ] Integration with external therapy resources

---

## Success Metrics

### Technical Metrics
- **Response Time**: < 3 seconds per message
- **Uptime**: 99%+ availability
- **Crisis Detection**: 95%+ accuracy
- **Memory Retention**: Context maintained across sessions

### User Experience Metrics
- **Persona Consistency**: Responses stay in character
- **Engagement**: Average session length > 10 minutes
- **Safety**: Zero harmful responses in testing
- **Satisfaction**: Positive user feedback on helpfulness

### Therapeutic Effectiveness
- **CBT Integration**: Natural technique application
- **User Progress**: Self-reported mood improvements
- **Crisis Handling**: Appropriate escalation and support

---

## File Structure

> **AI ASSISTANT**: When generating files, follow this exact structure and naming convention.

```
therapeutic-chatbot/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI application entry point
│   │   ├── models/                 # Pydantic models
│   │   │   ├── __init__.py
│   │   │   ├── chat.py            # Chat-related models
│   │   │   ├── persona.py         # Persona models
│   │   │   └── crisis.py          # Crisis detection models
│   │   ├── services/              # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── chat_service.py    # Main conversation logic
│   │   │   ├── persona_service.py # Persona management
│   │   │   ├── memory_service.py  # Pinecone integration
│   │   │   ├── crisis_service.py  # Safety monitoring
│   │   │   └── gemini_service.py  # Gemini API integration
│   │   ├── api/                   # API routes
│   │   │   ├── __init__.py
│   │   │   ├── chat.py           # Chat endpoints
│   │   │   └── health.py         # Health check endpoints
│   │   ├── core/                  # Core configuration
│   │   │   ├── __init__.py
│   │   │   ├── config.py         # Settings management
│   │   │   ├── security.py       # Security utilities
│   │   │   └── logging.py        # Logging configuration
│   │   └── utils/                 # Utility functions
│   │       ├── __init__.py
│   │       ├── prompts.py        # Prompt templates
│   │       └── validators.py     # Input validation
│   ├── tests/                     # Test files
│   │   ├── __init__.py
│   │   ├── test_chat.py
│   │   ├── test_personas.py
│   │   └── test_crisis.py
│   ├── requirements.txt           # Python dependencies
│   ├── requirements-dev.txt       # Development dependencies
│   └── pytest.ini               # Pytest configuration
├── frontend/
│   ├── src/
│   │   ├── components/           # React components
│   │   │   ├── Chat/
│   │   │   │   ├── ChatInterface.jsx
│   │   │   │   ├── MessageBubble.jsx
│   │   │   │   └── TypingIndicator.jsx
│   │   │   ├── Persona/
│   │   │   │   ├── PersonaSelector.jsx
│   │   │   │   └── PersonaCard.jsx
│   │   │   └── Common/
│   │   │       ├── Header.jsx
│   │   │       └── ErrorBoundary.jsx
│   │   ├── hooks/               # Custom React hooks
│   │   │   ├── useChat.js
│   │   │   ├── usePersona.js
│   │   │   └── useWebSocket.js
│   │   ├── services/            # API client services
│   │   │   ├── api.js
│   │   │   └── chatService.js
│   │   ├── utils/               # Utility functions
│   │   │   ├── constants.js
│   │   │   └── helpers.js
│   │   ├── styles/              # Global styles
│   │   │   └── globals.css
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── public/                  # Static assets
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── docs/
│   ├── PLANNING.md              # This file
│   ├── TASK.md                  # Task tracking
│   ├── API.md                   # API documentation
│   └── DEPLOYMENT.md            # Deployment guide
├── .env.example                 # Environment variables template
├── .gitignore
├── docker-compose.yml           # Local development setup
├── Dockerfile                   # Production container
└── README.md                    # Project overview
```

---

## Risk Assessment

### High-Risk Areas
1. **Crisis Handling**: Failure could be life-threatening
2. **Persona Consistency**: Poor implementation reduces effectiveness
3. **Memory System**: Privacy and data security concerns
4. **API Costs**: Unexpected usage spikes

### Mitigation Strategies
1. **Extensive Safety Testing**: Multiple layers of crisis detection
2. **Persona Validation**: Continuous testing and refinement
3. **Data Security**: Encrypt sensitive conversation data
4. **Cost Monitoring**: Implement usage alerts and rate limiting

---

## Development Philosophy

### Vibe Coding Principles
1. **Feel-First Development**: If it doesn't feel right, it's not right
2. **Incremental Progress**: Small, testable improvements
3. **User Empathy**: Constantly consider the user's emotional state
4. **Authentic Interaction**: Prioritize natural conversation flow
5. **Safety Paranoia**: Always err on the side of caution

### AI Assistant Development Rules
- **Generate complete, working code** - no placeholders or TODOs
- **Include proper error handling** in all API interactions
- **Add logging statements** for debugging and monitoring
- **Write self-documenting code** with clear variable names
- **Follow the established patterns** defined in this document
- **Test code before suggesting** - ensure it's syntactically correct

### Quality Standards
- **Conversation Quality**: Would you use this bot yourself?
- **Safety Standards**: Could this bot help someone in crisis?
- **Technical Reliability**: Does it work consistently?
- **User Experience**: Is it genuinely helpful and supportive?

---

## References for Development

### Technical Resources
- FastAPI Documentation: https://fastapi.tiangolo.com/
- Gemini API Documentation: https://ai.google.dev/docs
- Pinecone Documentation: https://docs.pinecone.io/
- React Documentation: https://react.dev/

### Therapeutic Resources
- CBT Techniques: Beck Institute resources
- Crisis Intervention: National Suicide Prevention Lifeline guidelines
- Mental Health First Aid: Evidence-based response protocols

### Design Inspiration
- Therapeutic chatbots: Woebot, Wysa research
- Conversational AI: Best practices for empathetic responses
- Safety in AI: Responsible AI development guidelines

---

## Update Instructions

This document should be updated when:
- Core architecture changes
- New technical decisions are made
- Scope significantly changes
- New constraints are discovered

**Last Updated**: [Current Date]
**Next Review**: Weekly during development
