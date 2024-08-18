import logging
import streamlit as st
import requests
from PIL import Image
import pytesseract
import speech_recognition as sr
from pydub import AudioSegment
import os

# 로그 설정
logging.basicConfig(level=logging.INFO)

# Streamlit 애플리케이션 설정
st.title("MyData Agent AI Chatbot")

# 질문과 답변 히스토리 저장을 위한 리스트 초기화
if 'history' not in st.session_state:
    st.session_state.history = []

# 입력 상태를 위한 변수 초기화
if 'user_query' not in st.session_state:
    st.session_state.user_query = ""
if 'option' not in st.session_state:
    st.session_state.option = "텍스트 입력"
if 'additional_text' not in st.session_state:
    st.session_state.additional_text = ""
if 'previous_option' not in st.session_state:
    st.session_state.previous_option = st.session_state.option

# 질문 유형 선택
st.session_state.option = st.selectbox(
    "질문 유형을 선택하세요:",
    ("텍스트 입력", "이미지 업로드", "MP3 업로드", "마이크 입력"),
)

# 질문 유형이 변경되었을 때 입력창 초기화
if st.session_state.option != st.session_state.previous_option:
    st.session_state.user_query = ""
    st.session_state.additional_text = ""
    st.session_state.previous_option = st.session_state.option

# 히스토리 출력 (오래된 질문과 답변이 위로, 최신 질문과 답변이 아래로 가도록)
st.header("Conversation History")
for i, (q, a) in enumerate(st.session_state.history):
    st.write(f"**Q{i+1}:** {q}")
    st.write(f"**A{i+1}:** {a}")
    st.write("---")  # 구분선 추가

# 텍스트 입력
if st.session_state.option == "텍스트 입력":
    st.session_state.user_query = st.text_input("Enter your question here:", st.session_state.user_query)

# 이미지 업로드 및 텍스트 추출
elif st.session_state.option == "이미지 업로드":
    uploaded_image = st.file_uploader("이미지를 업로드하세요:", type=["png", "jpg", "jpeg"])
    st.session_state.additional_text = st.text_input("추가적으로 입력할 텍스트를 여기에 입력하세요:", st.session_state.additional_text)
    if uploaded_image is not None:
        try:
            image = Image.open(uploaded_image)
            extracted_text = pytesseract.image_to_string(image, lang='kor')
            st.session_state.user_query = f"{extracted_text}\n{st.session_state.additional_text}" if st.session_state.additional_text else extracted_text
            st.write(f"추출된 텍스트: {st.session_state.user_query}")
        except Exception as e:
            logging.error(f"이미지 처리 중 오류 발생: {e}")
            st.error(f"이미지 처리 중 오류가 발생했습니다: {e}")

# MP3 업로드 및 음성 텍스트 변환
elif st.session_state.option == "MP3 업로드":
    uploaded_audio = st.file_uploader("MP3 파일을 업로드하세요:", type=["mp3"])
    if uploaded_audio is not None:
        recognizer = sr.Recognizer()
        audio = AudioSegment.from_file(uploaded_audio, format="mp3")
        audio.export("temp.wav", format="wav")

        with sr.AudioFile("temp.wav") as source:
            audio_data = recognizer.record(source)
        os.remove("temp.wav")

        try:
            transcribed_text = recognizer.recognize_google(audio_data, language="ko-KR")
            st.session_state.user_query = transcribed_text
            st.write(f"인식된 질문: {st.session_state.user_query}")
        except sr.UnknownValueError:
            st.error("음성을 인식할 수 없습니다.")
        except sr.RequestError as e:
            st.error(f"STT 서비스에 접근할 수 없습니다: {e}")

# 마이크 입력을 통한 음성 인식
elif st.session_state.option == "마이크 입력":
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("마이크가 활성화되었습니다. 말씀하세요...")
        try:
            audio_data = recognizer.listen(source, timeout=5)
            transcribed_text = recognizer.recognize_google(audio_data, language="ko-KR")
            st.session_state.user_query = transcribed_text
            st.write(f"인식된 질문: {st.session_state.user_query}")
            print(transcribed_text)
        except sr.UnknownValueError:
            st.error("음성을 인식할 수 없습니다.")
        except sr.RequestError as e:
            st.error(f"STT 서비스에 접근할 수 없습니다: {e}")
        except Exception as e:
            st.error(f"마이크 입력 중 오류가 발생했습니다: {e}")

# 질문을 제출하는 함수
def submit_question():
    if st.session_state.user_query:
        try:
            response = requests.post(
                "http://127.0.0.1:8001/ask",
                json={"query": st.session_state.user_query},
            )
            if response.status_code == 200:
                result = response.json()
                st.session_state.history.append((result['question'], result['answer']))
                # 입력창 및 추출된 내용 초기화
                st.session_state.user_query = ""
                st.session_state.additional_text = ""
                st.rerun()  # Trigger a rerun to update the interface
            else:
                st.error(f"Error: {response.status_code}")
        except Exception as e:
            st.error(f"Failed to connect to the server: {e}")
    else:
        st.error("Please enter or upload a question.")

# 질문을 제출하는 버튼
if st.button("Submit"):
    submit_question()

# Clear Session State 버튼 추가하여 세션 상태 초기화
if st.button("Clear Session State"):
    # 세션 상태 초기화
    extracted_text = ""
    transcribed_text = ""
    st.session_state.clear()  # 세션 상태 전체 초기화
    st.session_state.user_query = ""
    st.session_state.additional_text = ""


# Clear History 버튼 추가하여 히스토리 초기화 가능
if st.button("Clear History"):
    extracted_text = ""
    transcribed_text =""
    st.session_state.history.clear()
    st.session_state.user_query = ""
    st.session_state.additional_text = ""
    st.rerun()  # 페이지 새로고침
