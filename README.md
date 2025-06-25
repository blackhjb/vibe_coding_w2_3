# 🤖 Vibe Coding Chat Bot

LangGraph React Agent를 활용한 AI 챗봇 프로젝트입니다.

## 📁 프로젝트 구조

```
vibe_coding_w2-1/
├── backend/                 # FastAPI 백엔드
│   └── app/
│       ├── __init__.py
│       ├── config.py       # 환경 변수 설정
│       ├── main.py         # FastAPI 앱
│       └── routers/        # API 라우터
├── frontend/               # Streamlit 프론트엔드
│   └── app.py             # Streamlit 앱
├── requirements.txt       # Python 의존성
├── .env.example          # 환경 변수 템플릿
└── .env                  # 실제 환경 변수 (Git 제외)
```

## 🚀 시작하기

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env` 파일에서 다음 값들을 설정하세요:

```bash
# 필수: Google Gemini API 키
GOOGLE_API_KEY=your_google_api_key_here

# 선택사항: LangSmith 모니터링
LANGSMITH_API_KEY=your_langsmith_api_key_here
```

### 3. 백엔드 실행

```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

### 4. 프론트엔드 실행

```bash
streamlit run frontend/app.py --server.port 8501
```

## 🧪 테스트 실행

```bash
# 모든 테스트 실행
python -m pytest -v

# 특정 테스트 파일 실행
python -m pytest test_project_structure.py -v
python -m pytest test_app_functionality.py -v
python -m pytest test_env_config.py -v
```

## 🛠️ 기술 스택

### 백엔드
- **FastAPI**: 고성능 웹 프레임워크
- **uvicorn**: ASGI 서버
- **python-dotenv**: 환경 변수 관리

### 프론트엔드
- **Streamlit**: 웹 앱 프레임워크

### AI Agent
- **LangChain**: Agent 프레임워크
- **LangGraph**: React Agent 구현
- **Gemini-2.5-flash**: LLM 모델
- **DuckDuckGo Search**: 웹 검색 도구

### 개발 도구
- **pytest**: 테스트 프레임워크

## 📝 개발 원칙

이 프로젝트는 다음 원칙들을 따릅니다:

1. **SOLID 원칙** 준수
2. **Clean Architecture** 구조
3. **TDD (Test-Driven Development)** 방식
4. 파일과 함수의 **최소 단위** 분할

## 🔧 개발 모드

개발 모드에서는 다음 기능들이 활성화됩니다:

- FastAPI 자동 리로드
- Streamlit 사이드바에 개발 정보 표시
- 상세한 로그 출력

## 📊 API 엔드포인트

- `GET /`: API 루트 엔드포인트
- `GET /health`: 헬스체크 엔드포인트
- `GET /docs`: FastAPI 자동 문서화 (Swagger UI)

## 🌟 다음 단계

TASK-001 완료 후 다음 태스크들이 예정되어 있습니다:

- TASK-002: FastAPI 백엔드 기본 구조 구현
- TASK-003: LangGraph Agent 구현
- TASK-004: Streamlit 프론트엔드 구현 

커밋테스트야