from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from app.models import RAGPipeline, extract_text_from_pdfs, chunk_text, ConversationHistory
from app.conversation_manager import initialize_qa_chain
from app.config import pdf_paths
from app.db_utils import init_db, save_conversation_to_db  # db_utils에서 함수 가져오기
from langchain.docstore.document import Document
import uvicorn
import asyncio
from fastapi.middleware.cors import CORSMiddleware
import logging

# 로그 설정
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처에 대해 허용 (특정 출처만 허용하려면 ["http://example.com"] 식으로 명시)
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용 (GET, POST, PUT 등)
    allow_headers=["*"],  # 모든 헤더 허용
)

# 애플리케이션 시작 시 DB 초기화
@app.on_event("startup")
def startup():
    init_db()

# PDF에서 텍스트를 추출 및 청크로 나누기
extracted_text = extract_text_from_pdfs(pdf_paths)
chunks = chunk_text(extracted_text)

# 문서를 Document 객체 리스트로 변환
documents = [Document(page_content=chunk) for chunk in chunks]

# RAGPipeline 초기화
rag_pipeline = RAGPipeline(documents)

# 멀티턴 대화 히스토리 객체 생성
conversation_history = ConversationHistory()

class QuestionRequest(BaseModel):
    query: str
        
@app.middleware("http")
async def log_request(request: Request, call_next):
    logging.info(f"Request body: {await request.body()}")
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logging.error(f"Error during request: {e}")
        raise e        

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    question = request.query
    print(f"Received question: {question}")  # 요청된 질문 출력
    context = conversation_history.get_context()
    full_question = f"{context} {question}"
    
    try:
        #비동기적으로 RAGPipeline의 answer 메서드 호출
        answer = await asyncio.to_thread(rag_pipeline.answer, full_question)
        #answer = rag_pipeline.answer(full_question)
        conversation_history.add_turn(question, answer)
        return {"question": question, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/")
async def read_root():
    return {"message": "Welcome to MyData Agent API! Use the /ask endpoint to ask questions."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, log_level="info")
