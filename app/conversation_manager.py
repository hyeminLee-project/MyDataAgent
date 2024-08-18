import nltk
import re
from nltk.tokenize import word_tokenize
from itertools import combinations
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from app.config import pdf_paths
from app.qa_chain_setup import initialize_qa_chain
from langchain.schema import HumanMessage


# nltk 데이터 다운로드 (최초 실행 시 필요)
nltk.download('punkt')

# wget 명령어로 불용어 파일 다운로드
import os
import urllib.request

if not os.path.exists('korean_stopwords.txt'):
    urllib.request.urlretrieve(
        "https://raw.githubusercontent.com/byungjooyoo/Dataset/main/korean_stopwords.txt", 
        "korean_stopwords.txt"
    )

# 불용어 파일 읽어오기
with open('korean_stopwords.txt', 'r') as f:
    stop_words = f.read().split("\n")

# 추가 불용어
additional_stop_words = ['는', '은', '두']  # 필요한 경우 추가 불용어
stop_words = additional_stop_words + stop_words

#print("불용어 수:", len(stop_words))
#print("불용어 예시:", stop_words[:10])


# 불용어 제거 함수
def remove_postpositions(word, stop_words):
    pattern = '|'.join([f'{stop_word}$' for stop_word in stop_words])
    return re.sub(pattern, '', word)

# 질문을 처리하여 단어 조합을 생성하는 함수
def process_question(question):
    words = word_tokenize(question)
    filtered_words = [remove_postpositions(word, stop_words) for word in words if word.isalnum()]
    combinations_list = []
    for r in range(len(filtered_words), 1, -1):
        combinations_list.extend([' '.join(combo) for combo in combinations(filtered_words, r)])
    return combinations_list

# 추가 질문을 자동으로 생성하는 함수
def generate_clarification_question(query, model):
    prompt = f"사용자가 '{query}'에 대해 질문하였습니다. 이 질문과 관련하여 추가 정보를 요청할 수 있는 구체적인 질문을 생성해 주세요."
    
    # HumanMessage 객체를 생성하여 모델을 호출
    clarification_result = model.invoke([HumanMessage(content=prompt)])
    #return clarification_result[0].content
    
    # AIMessage 객체에서 content를 직접 반환
    return clarification_result.content

# qa_chain 초기화
qa_chain = initialize_qa_chain(pdf_paths)

# 질문을 처리하고 답변을 찾는 함수
def ask_question_with_fallback(query, qa_chain, stop_words, model):
    result = qa_chain({"query": query})
    
    # 첫 번째 시도에서 결과가 있는 경우 반환
    if 'result' in result and result['result'] and '관련된 내용이 없습니다' not in result['result']:
        return result['result']

    # 질문을 단어 조합으로 나누고 재질문
    queries = process_question(query)
    for sub_query in queries:
        result = qa_chain({"query": sub_query})
        if 'result' in result and result['result'] and '관련된 내용이 없습니다' not in result['result']:
            return result['result']
    
    # 모든 시도에서 답변을 찾지 못한 경우, 추가 질문을 자동으로 생성
    clarification_question = generate_clarification_question(query, model)
    return clarification_question

