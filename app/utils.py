# utils.py 파일에 정의
import time
#from PyPDF2 import PdfReader
#from langchain.schema import Document

#def load_documents(filepaths):
#    documents = []
#    for filepath in filepaths:
#        reader = PdfReader(filepath)
#        text = ""
#        for page in reader.pages:
#            text += page.extract_text()
#        documents.append(Document(page_content=text, metadata={"source": filepath}))
#    return documents


def rate_limited_request(llm, query):
    time.sleep(1)  # 각 요청 사이에 1초의 딜레이를 추가
    return llm(
        messages=[
            {"role": "system", "content": "You are a helpful agent."},
            {"role": "user", "content": query}
        ]
    )
