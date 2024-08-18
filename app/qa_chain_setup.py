from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from app.pdf_processor import extract_text_from_pdfs, chunk_text


# PDF 텍스트 추출 및 청크 분할
def initialize_qa_chain(pdf_paths):
    from app.pdf_processor import extract_text_from_pdfs, chunk_text

    # 텍스트 추출 및 청크 분할
    extracted_text = extract_text_from_pdfs(pdf_paths)
    text_chunks = chunk_text(extracted_text)

    # 인덱싱
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_texts(text_chunks, embeddings)

    # LLM 모델 설정
    model = ChatOpenAI(model_name="gpt-4", temperature=0)

    # 프롬프트 템플릿 정의
    prompt = PromptTemplate(
        input_variables=['context', 'question'],
        template="""You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question.
        If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
        Question: {question}
        Context: {context}
        Answer:"""
    )

    # RetrievalQA 체인 생성
    qa_chain = RetrievalQA.from_chain_type(
        llm=model,
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs={"prompt": prompt}
    )

    return qa_chain
