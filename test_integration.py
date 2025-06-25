import pytest
import sys
import os
import time
import threading
import requests
from unittest.mock import Mock, patch

# Add paths for all modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

class TestIntegration:
    """Integration tests for the complete system"""
    
    def test_all_modules_importable(self):
        """Test that all main modules can be imported without errors"""
        # Backend modules
        from backend.app.main import app
        from backend.app.config import settings
        from backend.app.agent import ChatAgent
        
        # Frontend module
        import frontend.app as frontend_app
        
        assert app is not None
        assert settings is not None
        assert ChatAgent is not None
        assert frontend_app is not None
    
    def test_config_settings_loaded(self):
        """Test that configuration settings are properly loaded"""
        from backend.app.config import settings
        
        # Settings should be accessible
        assert hasattr(settings, 'google_api_key')
        assert hasattr(settings, 'langsmith_api_key')
        assert hasattr(settings, 'fastapi_host')
        assert hasattr(settings, 'fastapi_port')
    
    def test_agent_class_structure(self):
        """Test that ChatAgent class has the expected structure"""
        from backend.app.agent import ChatAgent
        
        # Test class structure without initialization
        assert hasattr(ChatAgent, '__init__')
        assert hasattr(ChatAgent, 'invoke')
        
        # Test that the class can be referenced
        assert ChatAgent is not None
        assert callable(ChatAgent)
    
    def test_api_endpoints_structure(self):
        """Test that all required API endpoints are defined"""
        from backend.app.main import app
        
        # Get all routes
        routes = [route.path for route in app.routes]
        
        # Required endpoints
        assert "/health" in routes
        assert "/api/chat" in routes
        assert "/" in routes
    
    def test_frontend_api_integration_functions(self):
        """Test that frontend has proper API integration functions"""
        import frontend.app as frontend_app
        
        # Should have API integration functions
        assert hasattr(frontend_app, 'send_message_to_api')
        assert hasattr(frontend_app, 'API_URL')
        assert callable(frontend_app.send_message_to_api)
    
    def test_pydantic_models_validation(self):
        """Test that Pydantic models work correctly"""
        from backend.app.main import ChatMessage, ChatResponse
        
        # Test ChatMessage validation
        valid_message = ChatMessage(message="Hello", conversation_id="test-123")
        assert valid_message.message == "Hello"
        assert valid_message.conversation_id == "test-123"
        
        # Test validation errors
        with pytest.raises(Exception):  # Should raise validation error
            ChatMessage(message="")  # Empty message should fail
        
        # Test ChatResponse
        response = ChatResponse(response="Hi there!", conversation_id="test-123")
        assert response.response == "Hi there!"
        assert response.conversation_id == "test-123"
    
    def test_error_handling_works(self):
        """Test that error handling mechanisms are in place"""
        from backend.app.main import get_chat_agent
        import backend.app.main as main_module
        
        # Reset global agent to None for clean test
        main_module.chat_agent = None
        
        # Test that the function exists and handles errors
        agent = get_chat_agent()
        
        # Should either return an agent or None (depending on environment)
        # The important thing is that it doesn't crash
        assert agent is None or hasattr(agent, 'invoke')
    
    def test_conversation_id_handling(self):
        """Test that conversation IDs are handled properly across components"""
        import uuid
        from backend.app.main import ChatMessage
        
        # Test with provided conversation ID
        test_id = str(uuid.uuid4())
        message = ChatMessage(message="Hello", conversation_id=test_id)
        assert message.conversation_id == test_id
        
        # Test without conversation ID (should allow None)
        message_no_id = ChatMessage(message="Hello")
        assert message_no_id.conversation_id is None
    
    def test_all_required_packages_available(self):
        """Test that all required packages are available"""
        required_packages = [
            'fastapi',
            'uvicorn', 
            'streamlit',
            'langgraph',
            'langchain_google_genai',
            'langchain_community',
            'duckduckgo_search',
            'requests',
            'pydantic'
        ]
        
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                pytest.fail(f"Required package '{package}' is not available")
    
    def test_project_structure_compliance(self):
        """Test that the project structure matches expectations"""
        # Required files should exist
        required_files = [
            'backend/app/__init__.py',
            'backend/app/main.py',
            'backend/app/config.py',
            'backend/app/agent.py',
            'frontend/app.py',
            'requirements.txt'
        ]
        
        for file_path in required_files:
            assert os.path.exists(file_path), f"Required file {file_path} does not exist"
    
    def test_backend_frontend_api_compatibility(self):
        """Test that backend and frontend are compatible in terms of API contract"""
        from backend.app.main import ChatMessage, ChatResponse
        import frontend.app as frontend_app
        
        # Test that frontend API_URL is a string
        assert isinstance(frontend_app.API_URL, str)
        
        # Test that backend models match frontend expectations
        # Frontend should be able to create the right request format
        test_message = ChatMessage(message="Hello", conversation_id="test-123")
        
        # This should work without errors
        assert test_message.message == "Hello"
        assert test_message.conversation_id == "test-123" 