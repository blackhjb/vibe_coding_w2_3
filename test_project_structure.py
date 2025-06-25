import os
import pytest


def test_backend_folder_structure():
    """백엔드 폴더 구조가 올바르게 생성되었는지 테스트"""
    assert os.path.exists("backend"), "backend 폴더가 존재해야 합니다"
    assert os.path.exists("backend/app"), "backend/app 폴더가 존재해야 합니다"
    assert os.path.exists("backend/app/__init__.py"), "backend/app/__init__.py 파일이 존재해야 합니다"
    assert os.path.exists("backend/app/main.py"), "backend/app/main.py 파일이 존재해야 합니다"
    assert os.path.exists("backend/app/routers"), "backend/app/routers 폴더가 존재해야 합니다"
    assert os.path.exists("backend/app/routers/__init__.py"), "backend/app/routers/__init__.py 파일이 존재해야 합니다"


def test_frontend_folder_structure():
    """프론트엔드 폴더 구조가 올바르게 생성되었는지 테스트"""
    assert os.path.exists("frontend"), "frontend 폴더가 존재해야 합니다"
    assert os.path.exists("frontend/app.py"), "frontend/app.py 파일이 존재해야 합니다"


def test_requirements_file():
    """requirements.txt 파일이 존재하는지 테스트"""
    assert os.path.exists("requirements.txt"), "requirements.txt 파일이 존재해야 합니다"


def test_env_files():
    """환경 변수 파일들이 존재하는지 테스트"""
    assert os.path.exists(".env.example"), ".env.example 파일이 존재해야 합니다" 