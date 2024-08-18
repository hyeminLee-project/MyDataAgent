# MyDataAgent
Python을 사용하여 MyData 기술 가이드라인 및 표준 API 규격에 대한 질의응답을 지원하는 AI 에이전트입니다.
이 프로젝트는 FastAPI와 Streamlit을 기반으로 하며, LLM과 PDF 파일을 사용하여 한국어로 질문에 대해 정확하고 친절하게 답변하고자 합니다.

# 환경 
python 3.10 이상

FastAPI: 0.95.1

Streamlit: 1.37.1

PyMuPDF: 1.19.0

LangChain: 0.57.0

OpenAI API: gpt-4

## 주요 기능
- **PDF 기반 RAG(Retrieval-Augmented Generation)**: 마이데이터 관련 PDF 문서를 기반으로 질문에 답변합니다.
- **멀티턴 대화 관리**: 사용자의 질문과 AI의 응답을 히스토리로 관리합니다.
- **멀티모달 입력 지원**: 텍스트, 이미지, 음성 입력을 지원합니다.


# 가상환경 생성 (예: myenv라는 이름의 가상환경)
python3 -m venv myenv

# 가상환경 활성화 (macOS/Linux)
source myenv/bin/activate

# 가상환경 활성화 (Windows)
myenv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# FastAPI 서버 실행 방법

uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload

# Streamlit 앱 실행 방법 

streamlit run app/frontend/streamlit_app.py

# 테스트 실행 방법

pytest

(예시) pytest tests/test_models.py

# 프로젝트 구조 





