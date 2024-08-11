import json
import os

import requests
import streamlit as st
from dotenv import load_dotenv
from streamlit_chat import message


class CompletionExecutor:
    def __init__(self):
        # .env 파일 로드 (API 키 준비)
        load_dotenv()

        self._clovastudio_api_key = os.getenv('CLOVASTUDIO_API_KEY')
        self._apigw_api_key = os.getenv('APIGW_API_KEY')

    def execute(self, request_data):
        headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': self._clovastudio_api_key,
            'X-NCP-APIGW-API-KEY': self._apigw_api_key,
            'Content-Type': 'application/json; charset=utf-8',
        }
        response = requests.post('https://clovastudio.stream.ntruss.com/testapp/v1/chat-completions/HCX-003',headers=headers, json=request_data, stream=False)
        json_data = json.loads(response.text)

        return json_data['result']['message']['content']

st.title("HyperCLOVA X 챗봇 만들기")

if 'assistant' not in st.session_state:
    st.session_state['assistant'] = []

if 'user' not in st.session_state:
    st.session_state['user'] = []

with st.form('form', clear_on_submit=True):
    user_input = st.text_area('입력: ', '', key='input',height=200)
    submitted = st.form_submit_button('전송')
    if submitted and user_input:
        with st.spinner("대기중..."):

            completion_executor = CompletionExecutor()

            preset_text = [{"role":"system","content":""},{"role":"user","content":user_input}]
            request_data = {
                'messages': preset_text,
                'topP': 0.8,
                'topK': 0,
                'maxTokens': 300,
                'temperature': 0.3,
                'repeatPenalty': 5.0,
                'stopBefore': [],
                'includeAiFilters': True,
                'seed': 0
            }

            response_text=completion_executor.execute(request_data)

            # 대화 기록 유지
            st.session_state.user.append(user_input)
            st.session_state.assistant.append(response_text)

if st.session_state['assistant']:
    for i in range(len(st.session_state['assistant'])-1, -1, -1):
        message(st.session_state['user'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["assistant"][i], key=str(i))