# MyDataAgent
Python을 사용하여 MyData 기술 가이드라인 및 표준 API 규격에 대한 질의응답을 지원하는 AI 에이전트입니다.
이 프로젝트는 FastAPI와 Streamlit을 기반으로 하며, LLM(Chatgpt-4)과 PDF 파일을 사용하여 한국어로 질문에 대해 정확하고 친절하게 답변하고자 합니다.

# 환경 
python 3.10 이상

FastAPI: 0.95.1

Streamlit: 1.37.1

PyMuPDF: 1.19.0

LangChain: 0.57.0

OpenAI API: gpt-4


# 프로젝트 아키텍처


<img width="1030" alt="project architecture_capture" src="https://github.com/user-attachments/assets/75a39e57-4bb3-4cda-bd60-95e0937770be">



# mydata-agent 프로젝트 구조 

📦app                                                           # 애플리케이션의 주요 비즈니스 로직과 관련된 모듈을 포함한 폴더 
 ┣ 📜__init__.py                                                # app 모듈을 초기화하는 파일
 ┣ 📜config.py                                                  # 환경 설정과 관련된 설정값을 관리 (OpenAI API 키 설정)
 ┣ 📜conversation_manager.py                                    # 대화 관리, 질문 처리, 추가 질문 생성 로직을 관리
 ┣ 📜db_utils.py                                                # 데이터베이스와의 상호작용을 관리 (대화 이력 저장 및 조회 기능이 포함)
 ┣ 📜main.py                                                    # FastAPI 서버의 진입점으로, API 엔드포인트를 정의하고 서버를 실행
 ┣ 📜models.py                                                  # RAGPipeline 및 AI 모델 호출을 위한 로직을 포함
 ┣ 📜pdf_processor.py                                           # PDF 파일에서 텍스트를 추출하고 이를 청크로 나누는 처리 로직 관리 
 ┣ 📜qa_chain_setup.py                                          # 질의응답 체인 설정과 관련된 로직 관리 (임베딩 및 벡터 저장소 초기화가 포함)
 ┗ 📜utils.py                                                   # 기타 유틸리티 함수들을 포함
  📦data                                                        # PDF 파일이 저장되는 디렉토리
 ┣ 📜(221115 수정배포) (2022.10) 금융분야 마이데이터 기술 가이드라인.pdf    
 ┣ 📜(수정게시) 금융분야 마이데이터 표준 API 규격 v1.pdf
 📦frontend                                                     # 프론트엔드 관련 파일을 포함
 ┗ 📜streamlit_app.py                                           # Streamlit 기반의 사용자 인터페이스를 정의
 📦tests                                                        # 각 모듈의 기능을 검증 밑 테스트 코드 폴더
 ┣ 📜test_conversation_manager.py                               # conversation_manager 모듈의 테스트
 ┣ 📜test_import.py                                             # 다양한 모듈 임포트에 대한 테스트
 ┣ 📜test_main.py                                               # main.py의 API 엔드포인트에 대한 테스트
 ┣ 📜test_models.py                                             # models.py에서 정의된 로직에 대한 테스트
 ┣ 📜test_pdf_processor.py                                      # pdf_processor.py 모듈의 텍스트 추출 및 청크 처리 로직에 대한 테스트
 ┣ 📜test_qa_chain_setup.py                                     # qa_chain_setup.py의 질의응답 체인 설정 로직에 대한 테스트
 ┗ 📜test_transformers.py                                       # Transformers 라이브러리와 관련된 테스트
 📦asset                                                        # 테스트용 샘플 파일들을 포함
 ┣ 📜image_test.png                                             # 이미지 입력 테스트를 위한 샘플 이미지 파일
 ┣ 📜금융마이데이터.mp3                                             # 음성 입력 테스트를 위한 샘플 MP3 파일
 ┗ 📜마이데이터 질문.mp3   
   
 📜.gitignore                                                   # Git에 포함시키지 않을 파일 및 디렉토리를 정의
 📜requirements.txt                                             # 프로젝트에 필요한 파이썬 패키지와 버전을 명시
                       



## 주요 기능

### 1. **PDF 기반 RAG (Retrieval-Augmented Generation)**
마이데이터 관련 PDF 문서를 기반으로 질문에 답변합니다.

#### 1.1 PDF 문서 처리
- **`extract_text_from_pdfs` 함수**: PyMuPDF를 사용하여 PDF 파일에서 텍스트를 추출합니다.
- **`chunk_text` 함수**: 긴 텍스트를 일정한 크기의 청크로 분할하여 모델이 효율적으로 처리할 수 있도록 합니다. 이 과정에서 `CharacterTextSplitter` 클래스를 사용하며, 각 청크는 지정된 크기(`chunk_size`)와 중첩(`chunk_overlap`)을 가집니다.

#### 1.2 임베딩 및 벡터 저장소
- **텍스트 임베딩**: `OpenAIEmbeddings`를 사용하여 텍스트 청크를 임베딩(숫자 벡터)으로 변환합니다. 이를 통해 PDF 검색 시 유사한 의미를 가진 문장을 찾을 수 있습니다.
- **벡터 저장소**: `Chroma`를 사용하여 임베딩된 텍스트 청크를 벡터 저장소에 저장합니다. 이를 통해 효율적인 유사도 검색이 가능해집니다.

### 2. **불용어 처리 및 텍스트 전처리**
질문에 대한 주요 단어를 추출하고, 다양한 형태의 질문을 구성하여 더 나은 검색 결과를 얻을 수 있습니다.

- **`nltk` 라이브러리 사용**: 한국어 텍스트를 전처리하여 불필요한 조사나 어미를 제거합니다.
- **`word_tokenize` 함수**: 질문을 단어 단위로 분리하여 분석합니다.
- **불용어 필터링**: 외부 한국어 불용어 리스트를 사용하여 검색의 정확도를 높입니다. 추가적인 불용어도 설정 가능합니다.

### 3. **질문 처리**
사용자의 질문을 처리하여 단어 조합을 생성하고, 명확한 답변이 없을 경우 추가 질문을 자동으로 생성합니다.

- **`process_question` 함수**: 질문을 처리하여 핵심 단어를 추출하고 가능한 모든 단어 조합을 생성합니다.
- **`generate_clarification_question` 함수**: 사용자가 입력한 질문을 바탕으로 추가 정보를 얻기 위한 구체적인 질문을 생성합니다.

### 4. **질의응답 체인**
사용자가 입력한 질문에 대해 관련 정보를 검색하고, LLM(ChatGPT-4)을 통해 답변을 생성합니다.

- **`initialize_qa_chain` 함수**: PDF에서 추출한 텍스트를 바탕으로 질의응답 체인을 초기화합니다. 이 체인은 검색과 응답 생성 작업을 수행합니다.
- **`RAGPipeline` 클래스**: `ChatOpenAI`와 같은 API를 사용하여 응답을 생성하며, 정의된 프롬프트 템플릿에 부합하는 답변을 제공합니다.

### 5. **멀티턴 대화 관리**
사용자의 질문과 AI의 응답을 히스토리로 관리합니다.

- **지속적인 대화 관리**:
    - `ConversationHistory` 클래스는 사용자가 AI와 나눈 대화를 히스토리로 관리합니다. 대화의 각 턴(사용자의 질문과 AI의 응답)을 기록하여 이후 대화에서 참고할 수 있도록 합니다.
    -  대화의 각 턴(사용자의 질문과 AI의 응답)을 기록하여 이후 대화에서 참고할 수 있도록 SQLite 데이터베이스에 저장합니다.
    - `add_turn` 메서드를 통해 사용자의 입력과 AI의 응답을 저장하며, `get_context` 메서드를 통해 대화의 전체 맥락을 쉽게 참조할 수 있습니다.
       이를 통해 AI는 대화의 흐름을 이해하고, 사용자가 이전에 했던 질문이나 AI의 답변을 바탕으로 적절한 응답을 생성할 수 있습니다.
    - 데이터베이스에 저장된 대화 이력은 재시작 시에도 유지되며, 지속적인 대화가 가능합니다.

- **명확한 추가 질문 생성**:
    - 사용자가 입력한 질문에 대해 명확한 답변을 얻지 못한 경우, `generate_clarification_question` 함수를 통해 추가적인 정보를 요청하는 구체적인 질문을 자동으로 생성합니다. 이 기능은 대화를 이어가며, AI가 사용자의 의도를 더 잘 이해할 수 있도록 도와줍니다.

### 6. **멀티모달 입력 지원**
텍스트, 이미지, 음성 입력을 지원합니다.

- **텍스트 입력**:
    - `streamlit_app.py`에서 텍스트 입력을 받아 AI와 상호작용할 수 있습니다. 사용자는 텍스트 입력을 통해 질문을 입력하고, AI로부터 즉각적인 답변을 받을 수 있습니다.

- **이미지 입력**:
    - 이미지 입력 기능은 `pytesseract`를 사용하여 이미지에서 텍스트를 추출합니다. 사용자가 업로드한 이미지 파일에서 텍스트를 추출하여, AI가 이 텍스트를 분석하고 적절한 답변을 제공합니다. 예를 들어, 이미지에 포함된 문서나 스크린샷에서 텍스트를 추출해 질문할 수 있습니다.

- **음성 입력**:
    - 음성 입력은 `SpeechRecognition`과 `pydub` 라이브러리를 사용하여 처리됩니다. 사용자가 음성 파일(MP3)을 업로드하거나 마이크를 통해 직접 질문할 수 있으며, 이 음성은 텍스트로 변환되어 AI가 이를 분석하고 응답을 생성합니다.
    - 이 기능은 다양한 입력 방법을 지원하여 사용자가 더 편리하게 AI와 상호작용할 수 있도록 돕습니다.

## 테스트용 파일

이 프로젝트에서는 다양한 입력 형태를 테스트하기 위해 `asset` 폴더에 샘플 이미지와 MP3 파일을 포함하고 있습니다. 이 파일들은 멀티모달 입력 기능의 테스트에 사용됩니다.


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

streamlit run frontend/streamlit_app.py --server.enableXsrfProtection false

streamlit 앱에서 파일 업로드 시에 --server.enableXsrfProtection false 안하면 403 에러 발생함


# 테스트 실행 방법

pytest

(예시) pytest tests/test_models.py






