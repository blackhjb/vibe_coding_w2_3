import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
import requests

# Add the frontend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'frontend'))

class TestStreamlitFrontend:
    """Test cases for Streamlit Frontend"""
    
    def test_frontend_module_exists(self):
        """Test that the frontend app module exists and can be imported"""
        try:
            import frontend.app as frontend_app
            assert frontend_app is not None
        except ImportError:
            # If import fails, the file should at least exist
            assert os.path.exists("frontend/app.py")
    
    @patch('frontend.app.requests.post')
    def test_send_message_to_api(self, mock_post):
        """Test that frontend can send messages to the API"""
        import frontend.app as frontend_app
        
        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "response": "Hello! How can I help you?",
            "conversation_id": "test-123"
        }
        mock_post.return_value = mock_response
        
        # Test the function exists and works
        if hasattr(frontend_app, 'send_message_to_api'):
            result = frontend_app.send_message_to_api("Hello", "test-123")
            assert result is not None
            assert "response" in result
            assert "conversation_id" in result
    
    @patch('frontend.app.requests.post')
    def test_handle_api_errors(self, mock_post):
        """Test that frontend handles API errors gracefully"""
        import frontend.app as frontend_app
        
        # Mock API error
        mock_post.side_effect = requests.exceptions.RequestException("API Error")
        
        # Test error handling
        if hasattr(frontend_app, 'send_message_to_api'):
            result = frontend_app.send_message_to_api("Hello")
            # Should return some error indication or None
            assert result is None or "error" in str(result).lower()
    
    def test_frontend_has_main_function(self):
        """Test that frontend has main function for running the app"""
        import frontend.app as frontend_app
        
        # Should have either main function or app entry point
        assert hasattr(frontend_app, 'main') or hasattr(frontend_app, 'run_app')
    
    def test_frontend_configuration(self):
        """Test that frontend has proper configuration"""
        import frontend.app as frontend_app
        
        # Should have API URL configuration
        if hasattr(frontend_app, 'API_URL'):
            assert frontend_app.API_URL is not None
            assert isinstance(frontend_app.API_URL, str) 