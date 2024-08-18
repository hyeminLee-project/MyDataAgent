import sys
import os
import pytest
from app.conversation_manager import process_question, ask_question_with_fallback
from langchain.chat_models import ChatOpenAI
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))



@pytest.fixture
def qa_chain_mock():
    # qa_chain을 mocking 할 수 있는 fixture 생성
    class MockQAChain:
        def __call__(self, query):
            if "test" in query["query"]:
                return {"result": "Test answer"}
            return {"result": ""}

    return MockQAChain()


def generate_clarification_question(query, model):
    prompt = f"사용자가 '{query}'에 대해 질문하였습니다. 이 질문과 관련하여 추가 정보를 요청할 수 있는 구체적인 질문을 생성해 주세요."
    clarification_result = model.invoke([MagicMock(content="Test answer")])  # Mock된 결과 반환
    return clarification_result[0].content  # 리스트의 첫 번째 요소의 content 반환"

#def test_process_question():
#    question = "정보 전송 요구 연장은 언제 가능한가요?"
#    stop_words = ['이', '가', '을', '를', '에', '의']  # 예시 불용어 목록
#    #combinations = process_question(question)
#    
#    
#    #assert len(combinations) > 0  # 조합이 생성되는지 확인
#    # Mock LLM 모델
#    model = MagicMock()

def test_ask_question_with_fallback(qa_chain_mock):##qa_chain_mock
    pdf_paths = ["data/(221115 수정배포) (2022.10) 금융분야 마이데이터 기술 가이드라인.pdf", "data/(수정게시) 금융분야 마이데이터 표준 API 규격 v1.pdf"]
    query = "정보 전송 요구 연장은 언제 가능한가요?"
    #qa_chain = initialize_qa_chain(pdf_paths)
    stop_words = ['이', '가', '을', '를', '에', '의']  # 예시 불용어 목록
    
    
    # LLM 모델 인스턴스 생성
    #model = ChatOpenAI(model_name="gpt-4", temperature=0)
    model = MagicMock()
    model.invoke.return_value = [MagicMock(content="Test answer")]   # invoke가 호출되면 "Test answer" 반환

    # Mock generate_clarification_question 함수를 직접 처리
#    with MagicMock() as generate_clarification_question_mock:
#        generate_clarification_question_mock.return_value = "Test answer"
#        
        # ask_question_with_fallback 함수 호출 시 model 인자를 추가
    answer = ask_question_with_fallback(query, qa_chain_mock, stop_words, model)
    
    assert answer == "Test answer"

    # ask_question_with_fallback 함수 호출 시 model 인자를 추가
    #answer = ask_question_with_fallback(query, qa_chain_mock, stop_words, model)
    
    #assert answer == "Test answer"
