import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter

# PDF에서 텍스트를 추출하는 함수
def extract_text_from_pdfs(pdf_paths):
    combined_text = ""
    for pdf_path in pdf_paths:
        doc = fitz.open(pdf_path)
        for page in doc:
            combined_text += page.get_text()
    return combined_text

# 텍스트를 작은 청크로 나누는 함수
def chunk_text(text, chunk_size=500, chunk_overlap=100):#1000
    from langchain.text_splitter import CharacterTextSplitter
    text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_text(text)
    return chunks
