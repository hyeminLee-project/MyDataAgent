import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to MyData Agent API! Use the /ask endpoint to ask questions."}

def test_ask_question(mocker):
    # QA 체인의 mock을 생성하여 특정 질문에 대한 답변을 설정
    mocker.patch("app.main.rag_pipeline.answer", return_value="Mocked Answer")

    response = client.post("/ask", json={"query": "테스트 질문"})
    assert response.status_code == 200
    assert response.json() == {"question": "테스트 질문", "answer": "Mocked Answer"}
