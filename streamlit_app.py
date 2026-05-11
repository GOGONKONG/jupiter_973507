import streamlit as st
from openai import OpenAI

st.title("✈️ 여행 플래너 챗봇")
st.write(
    "이 챗봇은 여행지 추천, 일정 계획, 맛집 추천, 준비물 체크리스트, "
    "예산 계획 등을 도와주는 여행용 AI 챗봇입니다."
)

openai_api_key = st.text_input("OpenAI API 키", type="password")

if not openai_api_key:
    st.info("계속하려면 OpenAI API 키를 입력해주세요.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": """
너는 친절하고 센스 있는 여행 플래너 챗봇이야.
사용자의 여행 목적, 일정, 예산, 취향을 바탕으로 여행 계획을 추천해줘.

답변할 때는 다음을 고려해:
- 여행지 추천
- 날짜별 일정
- 맛집/카페 추천
- 교통 동선
- 예상 예산
- 준비물
- 비 오는 날 대안 일정
- 혼자/커플/친구/가족 여행 여부

답변은 보기 쉽게 정리하고, 너무 딱딱하지 않게 친절한 말투로 말해줘.
"""
            }
        ]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("어디로 여행 가고 싶으신가요?"):

        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            stream=True,
        )

        with st.chat_message("assistant"):
            response = st.write_stream(stream)

        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )
