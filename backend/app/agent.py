import os
from typing import List, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import BaseTool

from .config import settings

class ChatAgent:
    """LangGraph React Agent with DuckDuckGo search capability"""
    
    def __init__(self):
        """Initialize the chat agent"""
        self.model = self._initialize_model()
        self.tools = self._initialize_tools()
        self.agent = self._create_agent()
    
    def _initialize_model(self) -> ChatGoogleGenerativeAI:
        """Initialize Gemini model"""
        if not settings.google_api_key:
            raise ValueError("Google API key is required")
        
        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key=settings.google_api_key,
            temperature=0.1
        )
    
    def _initialize_tools(self) -> List[BaseTool]:
        """Initialize DuckDuckGo search tool"""
        search_tool = DuckDuckGoSearchRun(
            name="duckduckgo_search",
            description="Search the web for current information using DuckDuckGo"
        )
        
        return [search_tool]
    
    def _create_agent(self):
        """Create the LangGraph React Agent"""
        return create_react_agent(
            model=self.model,
            tools=self.tools,
            prompt="You are a helpful assistant that can search the web for information. "
                   "Use the search tool when you need to find current information."
        )
    
    def invoke(self, message: str, conversation_id: str = None) -> Dict[str, Any]:
        """Invoke the agent with a message"""
        try:
            # Prepare input for the agent
            input_data = {
                "messages": [{"role": "user", "content": message}]
            }
            
            # Configure LangSmith if available
            config = {}
            if settings.langsmith_api_key:
                config = {
                    "configurable": {
                        "session_id": conversation_id or "default"
                    }
                }
            
            # Invoke the agent
            result = self.agent.invoke(input_data, config=config)
            
            return result
            
        except Exception as e:
            # Fallback response on error
            return {
                "messages": [
                    {
                        "role": "assistant", 
                        "content": f"I apologize, but I encountered an error: {str(e)}"
                    }
                ]
            } 