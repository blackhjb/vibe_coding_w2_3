import pytest
from fastapi.testclient import TestClient
import sys
import os
from unittest.mock import Mock, patch

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.main import app

client = TestClient(app)

class TestAPIEndpoints:
    """Test cases for API endpoints with agent integration"""
    
    @patch('backend.app.main.get_chat_agent')
    def test_chat_endpoint_with_agent_integration(self, mock_get_agent):
        """Test chat endpoint properly integrates with ChatAgent"""
        # Mock agent response
        mock_agent_instance = Mock()
        mock_agent_instance.invoke.return_value = {
            "messages": [
                {"role": "assistant", "content": "Hello! How can I help you?"}
            ]
        }
        mock_get_agent.return_value = mock_agent_instance
        
        response = client.post("/api/chat", json={
            "message": "Hello",
            "conversation_id": "test-123"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "conversation_id" in data
        assert data["conversation_id"] == "test-123"
    
    @patch('backend.app.main.get_chat_agent')
    def test_chat_endpoint_handles_agent_errors(self, mock_get_agent):
        """Test chat endpoint handles agent errors gracefully"""
        # Mock agent to raise an error during invoke
        mock_agent_instance = Mock()
        mock_agent_instance.invoke.side_effect = Exception("Agent error")
        mock_get_agent.return_value = mock_agent_instance
        
        response = client.post("/api/chat", json={
            "message": "Hello"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        # Should contain error message
        assert "error" in data["response"].lower()
    
    @patch('backend.app.main.get_chat_agent')
    def test_chat_endpoint_handles_agent_unavailable(self, mock_get_agent):
        """Test chat endpoint handles unavailable agent gracefully"""
        # Mock get_chat_agent to return None (agent initialization failed)
        mock_get_agent.return_value = None
        
        response = client.post("/api/chat", json={
            "message": "Hello"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        # Should contain fallback message
        assert "unable to process" in data["response"].lower()
    
    def test_chat_endpoint_validation(self):
        """Test chat endpoint validates input properly"""
        # Test with missing message
        response = client.post("/api/chat", json={})
        assert response.status_code == 422
        
        # Test with empty message
        response = client.post("/api/chat", json={"message": ""})
        assert response.status_code == 422
    
    @patch('backend.app.main.get_chat_agent')
    def test_chat_endpoint_generates_conversation_id(self, mock_get_agent):
        """Test chat endpoint generates conversation_id when not provided"""
        # Mock agent response
        mock_agent_instance = Mock()
        mock_agent_instance.invoke.return_value = {
            "messages": [
                {"role": "assistant", "content": "Response"}
            ]
        }
        mock_get_agent.return_value = mock_agent_instance
        
        response = client.post("/api/chat", json={"message": "Hello"})
        
        assert response.status_code == 200
        data = response.json()
        assert "conversation_id" in data
        assert data["conversation_id"] is not None
        assert len(data["conversation_id"]) > 0 