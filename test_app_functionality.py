import pytest
from fastapi.testclient import TestClient
import sys
import os

# FastAPI 앱 테스트
sys.path.append("backend")
from app.main import app

client = TestClient(app)


def test_fastapi_root_endpoint():
    """FastAPI 루트 엔드포인트가 올바르게 작동하는지 테스트"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Vibe Coding Chat API"}


def test_fastapi_app_title():
    """FastAPI 앱의 타이틀이 올바르게 설정되었는지 테스트"""
    assert app.title == "Vibe Coding Chat API"
    assert app.version == "1.0.0"


def test_fastapi_health_endpoint():
    """FastAPI 헬스체크 엔드포인트가 올바르게 작동하는지 테스트"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "debug" in data
    assert "log_level" in data
    assert data["status"] == "healthy"


def test_streamlit_app_file_exists():
    """Streamlit 앱 파일이 존재하는지 테스트"""
    assert os.path.exists("frontend/app.py"), "frontend/app.py 파일이 존재해야 합니다"


def test_env_variables_template():
    """환경 변수 템플릿 파일의 내용이 올바른지 테스트"""
    with open(".env.example", "r") as f:
        content = f.read()
        assert "GOOGLE_API_KEY" in content
        assert "LANGSMITH_API_KEY" in content
        assert "API_HOST" in content
        assert "STREAMLIT_SERVER_PORT" in content 