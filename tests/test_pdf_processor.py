import pytest
from app.pdf_processor import extract_text_from_pdfs, chunk_text

def preprocess_text(text):
    # 텍스트를 전처리하여 더 쉽게 청크로 나눌 수 있도록 합니다.
    # 예를 들어, 각 문장 뒤에 구분자 추가
    return text.replace("\n", " ").replace(".", ".\n")

def test_extract_text_from_pdfs():
    # 예시 PDF 파일 경로
    pdf_paths = ["data/(221115 수정배포) (2022.10) 금융분야 마이데이터 기술 가이드라인.pdf", "data/(수정게시) 금융분야 마이데이터 표준 API 규격 v1.pdf"]  # 테스트용 샘플 PDF
    extracted_text = extract_text_from_pdfs(pdf_paths)
    assert len(extracted_text) > 0, "PDF에서 텍스트가 추출되지 않았습니다."  # 텍스트가 추출되는지 확인

def test_chunk_text():
    pdf_paths = ["data/(221115 수정배포) (2022.10) 금융분야 마이데이터 기술 가이드라인.pdf", "data/(수정게시) 금융분야 마이데이터 표준 API 규격 v1.pdf"]  # 테스트용 샘플 PDF
    extracted_text = extract_text_from_pdfs(pdf_paths)
    # 전처리된 텍스트로 청크 분할
    preprocessed_text = preprocess_text(extracted_text)
    chunks = chunk_text(extracted_text, chunk_size=20, chunk_overlap=5)
    