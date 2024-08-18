import os
import fitz  # PyMuPDF
#from langchain.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
#from langchain_chroma import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
#from sentence_transformers import SentenceTransformer
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document
from chromadb.config import Settings
from app.config import OPENAI_API_KEY
from app.pdf_processor import extract_text_from_pdfs, chunk_text

openai_api_key = OPENAI_API_KEY
if not openai_api_key:
    raise ValueError("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")



# 멀티턴 대화를 위한 클래스 정의
class ConversationHistory:
    def __init__(self):
        self.history = []

    def add_turn(self, user_input, ai_response):
        self.history.append({"user": user_input, "ai": ai_response})

    def get_context(self):
        return " ".join([f"User: {turn['user']} AI: {turn['ai']}" for turn in self.history])

# RAGPipeline 정의
class RAGPipeline:
    def __init__(self, documents):
        self.documents = documents
        self.embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        client_settings = Settings()  # 기본 설정 사용
        self.vectorstore = Chroma.from_documents(documents, self.embeddings, client_settings=client_settings)

        self.llm = ChatOpenAI(openai_api_key=openai_api_key, model_name="gpt-4o")

        
    def search_documents(self, query):
        print(f"Calling similarity_search with query: {query}")
        try:
            #results = self.vectorstore.similarity_search(query, n_results=5)
            results = self.vectorstore.similarity_search(query, k=5)
            return [Document(page_content=result.page_content) for result in results]
        except TypeError as e:
            print(f"TypeError in similarity_search: {e}")  # Check for errors related to argument passing
            raise e
            
    def answer(self, query: str, model="gpt-4") -> str:
        try:
            relevant_docs = self.search_documents(query)
            combined_text = " ".join([doc.page_content for doc in relevant_docs])
            #response = self.llm.completions.create(
            response = self.llm(
                #model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful agent."},
                    {"role": "user", "content": f"Based on the following text extracted from the PDF, answer the question friendly and precisely from this text: {query}"}
                ]
                #,max_tokens=4008,
            )
            #return response.choices[0].message.content
            return response.content
        except Exception as e:
            print(f"Error: {str(e)}")  # 오류 메시지 출력
            raise e  # 예외 재발생 시켜 FastAPI가 처리하도록 함