from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import os
import uuid

from .config import settings
from .agent import ChatAgent

app = FastAPI(
    title="Vibe Coding Chatbot API",
    description="API for AI-powered chatbot with web search capabilities",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ChatAgent
chat_agent = None

def get_chat_agent():
    """Get or initialize the chat agent"""
    global chat_agent
    if chat_agent is None:
        try:
            chat_agent = ChatAgent()
        except Exception as e:
            print(f"Warning: Could not initialize ChatAgent: {e}")
            # Return None to indicate initialization failed
            return None
    return chat_agent

# Pydantic models
class ChatMessage(BaseModel):
    message: str = Field(..., min_length=1, description="The user message")
    conversation_id: Optional[str] = Field(None, description="Optional conversation ID")

class ChatResponse(BaseModel):
    response: str
    conversation_id: str

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# Chat endpoint with agent integration
@app.post("/api/chat", response_model=ChatResponse)
async def chat(chat_message: ChatMessage):
    """Chat endpoint for processing user messages with agent"""
    # Get or create conversation ID
    conversation_id = chat_message.conversation_id or str(uuid.uuid4())
    
    try:
        # Get the chat agent
        agent = get_chat_agent()
        
        if agent is None:
            # Fallback if agent is not available
            return ChatResponse(
                response=f"I received your message: '{chat_message.message}', but I'm currently unable to process it with full capabilities.",
                conversation_id=conversation_id
            )
        
        # Invoke the agent
        result = agent.invoke(chat_message.message, conversation_id)
        
        # Extract response from agent result
        if "messages" in result and len(result["messages"]) > 0:
            # Get the last assistant message
            assistant_messages = [
                msg for msg in result["messages"] 
                if msg.get("role") == "assistant" or hasattr(msg, "content")
            ]
            
            if assistant_messages:
                last_message = assistant_messages[-1]
                # Handle different message formats
                if hasattr(last_message, "content"):
                    response_text = last_message.content
                elif isinstance(last_message, dict) and "content" in last_message:
                    response_text = last_message["content"]
                else:
                    response_text = str(last_message)
            else:
                response_text = "I'm here to help! How can I assist you today?"
        else:
            response_text = "I'm here to help! How can I assist you today?"
        
        return ChatResponse(
            response=response_text,
            conversation_id=conversation_id
        )
        
    except Exception as e:
        # Error handling - return error message in response
        return ChatResponse(
            response=f"I apologize, but I encountered an error while processing your request: {str(e)}",
            conversation_id=conversation_id
        )

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Vibe Coding Chatbot API is running"}

# PR Test endpoint
@app.get("/api/pr-test")
async def pr_test():
    """PR 테스트용 엔드포인트"""
    return {
        "message": "PR 테스트 성공!",
        "branch": "pr_test",
        "status": "active",
        "features": [
            "새로운 API 엔드포인트 추가",
            "README.md 업데이트",
            "브랜치 기반 개발 테스트"
        ]
    } 