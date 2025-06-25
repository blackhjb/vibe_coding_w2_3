import pytest
import sys
import os
from unittest.mock import Mock, patch

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

class TestLangGraphAgent:
    """Test cases for LangGraph React Agent"""
    
    def test_agent_initialization(self):
        """Test that the agent can be initialized properly"""
        from backend.app.agent import ChatAgent
        
        agent = ChatAgent()
        assert agent is not None
        assert hasattr(agent, 'invoke')
    
    def test_duckduckgo_tool_available(self):
        """Test that DuckDuckGo search tool is available"""
        from backend.app.agent import ChatAgent
        
        agent = ChatAgent()
        assert hasattr(agent, 'tools')
        
        # Check if DuckDuckGo tool is in the tools list
        tool_names = [tool.name for tool in agent.tools]
        assert 'duckduckgo_search' in tool_names
    
    @patch('backend.app.agent.ChatGoogleGenerativeAI')
    def test_gemini_model_integration(self, mock_gemini):
        """Test that Gemini model is properly integrated"""
        from backend.app.agent import ChatAgent
        
        mock_model = Mock()
        mock_gemini.return_value = mock_model
        
        agent = ChatAgent()
        assert agent.model is not None
    
    def test_agent_invoke_with_simple_query(self):
        """Test agent can handle simple queries"""
        from backend.app.agent import ChatAgent
        
        agent = ChatAgent()
        
        # Simple test query
        response = agent.invoke("Hello")
        assert response is not None
        assert isinstance(response, dict)
        assert 'messages' in response
    
    def test_agent_tools_length(self):
        """Test that the agent has the expected number of tools"""
        from backend.app.agent import ChatAgent
        
        agent = ChatAgent()
        
        # Should have at least 1 tool (DuckDuckGo search)
        assert len(agent.tools) >= 1 