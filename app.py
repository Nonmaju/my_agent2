import streamlit as st
import requests
from dotenv import load_dotenv
from langchain.tools import tool
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent

load_dotenv()

@tool
def get_usd_krw_rate() -> str:
    """Gets the current exchange rate for USD to KRW (dollar to won) from Frankfurter API."""
    url = "https://api.frankfurter.dev/v1/latest?base=USD&symbols=KRW"
    response = requests.get(url)
    data = response.json()
    rate = data["rates"]["KRW"]
    date = data["date"]
    return f"기준일자 {date}의 1 USD당 KRW 환율은 {rate}원입니다."

model = init_chat_model("gpt-5.4-mini")
agent = create_agent(model, [get_usd_krw_rate])

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("실시간 환율 챗봇")

prompt = st.chat_input("환율이나 환산한 금액을 자연어로 질문해 보세요.")
if prompt:
    response = agent.invoke({"messages": {"role": "user", "content": prompt}})
    st.session_state.messages.append({'role': "user", 'content': prompt})
    st.session_state.messages.append({'role': "ai", 'content': response['messages'][-1].content})

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message['content'])
