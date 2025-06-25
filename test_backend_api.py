import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.main import app

client = TestClient(app)

class TestBackendAPI:
    """Test cases for Backend API structure"""
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
    
    def test_chat_endpoint_exists(self):
        """Test chat endpoint exists and accepts POST requests"""
        response = client.post("/api/chat", json={"message": "test"})
        # Should return 422 for incomplete request or 200 for valid response
        assert response.status_code in [200, 422]
    
    def test_config_loaded(self):
        """Test that configuration is properly loaded"""
        from backend.app.config import settings
        assert settings is not None
        assert hasattr(settings, 'google_api_key')
        assert hasattr(settings, 'langsmith_api_key') 