# test_models.py

import pytest
from app.models import RAGPipeline, ConversationHistory
from langchain.docstore.document import Document
from unittest.mock import MagicMock
import os


@pytest.fixture
def mock_documents():
    # 테스트용 문서 생성
    return [
        Document(page_content="This is a test document about MyData."),
        Document(page_content="This document contains information about APIs."),
        Document(page_content="Here is some text about token management.")
    ]


@pytest.fixture
def rag_pipeline(mock_documents):
    # RAGPipeline 객체 생성 (OpenAI API 및 Chroma를 Mock으로 대체)
    mock_embeddings = MagicMock()
    mock_vectorstore = MagicMock()
    mock_llm = MagicMock()

    # 검색 시 Mock 문서 반환
    mock_vectorstore.similarity_search.return_value = mock_documents

    # LLM 호출 시 Mock 응답 반환
    mock_llm.return_value = MagicMock(content="This is a mock answer.")

    # RAGPipeline 초기화
    pipeline = RAGPipeline(documents=mock_documents)
    pipeline.embeddings = mock_embeddings
    pipeline.vectorstore = mock_vectorstore
    pipeline.llm = mock_llm

    return pipeline


def test_rag_pipeline_search_documents(rag_pipeline):
    query = "What is MyData?"
    results = rag_pipeline.search_documents(query)

    assert len(results) == 3  # Mock 문서가 3개 반환되는지 확인
    assert "MyData" in results[0].page_content  # 첫 번째 문서에 'MyData' 텍스트 포함 확인


def test_rag_pipeline_answer(rag_pipeline):
    query = "Tell me about token management."
    answer = rag_pipeline.answer(query)

    assert answer == "This is a mock answer."  # LLM이 Mock 응답을 반환하는지 확인


def test_conversation_history():
    history = ConversationHistory()

    # 대화 추가
    history.add_turn("What is MyData?", "MyData is a concept...")
    history.add_turn("Tell me about APIs.", "APIs are...")

    context = history.get_context()

    # 히스토리에 대화 내용이 올바르게 추가되었는지 확인
    assert "User: What is MyData?" in context
    assert "AI: MyData is a concept..." in context
    assert "User: Tell me about APIs." in context
    assert "AI: APIs are..." in context
