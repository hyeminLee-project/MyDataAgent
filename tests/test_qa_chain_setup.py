import pytest
from app.qa_chain_setup import initialize_qa_chain
from app.config import pdf_paths

def test_initialize_qa_chain():
#    pdf_paths = ["(221115 수정배포) (2022.10) 금융분야 마이데이터 기술 가이드라인", "(수정게시) 금융분야 마이데이터 표준 API 규격 v1.pdf"] 
    qa_chain = initialize_qa_chain(pdf_paths)
    
    assert qa_chain is not None  # QA 체인이 생성되는지 확인
    assert hasattr(qa_chain, "run")  # QA 체인에 run 메서드가 있는지 확인
