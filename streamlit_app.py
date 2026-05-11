import streamlit as st
from openai import OpenAI

st.title("🎣 1박 2일 낚시 플래너 챗봇")
st.write(
    "계절, 시기, 날씨, 지역, 어종, 동행 유형에 따라 "
    "1박 2일 낚시 여행 일정을 추천해주는 챗봇입니다."
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
너는 1박 2일 낚시 여행 전문 플래너 챗봇이야.

사용자가 입력한 지역, 계절, 월, 날씨, 어종, 동행 유형, 예산을 바탕으로
현실적인 1박 2일 낚시 일정을 추천해줘.

반드시 다음 기준을 반영해:

1. 시기별 추천
- 봄: 산란기, 따뜻해지는 수온, 도보권 포인트
- 여름: 이른 새벽/해질녘 중심, 더위 대비, 야간 낚시
- 가을: 활성도 높은 시즌, 다양한 어종 추천
- 겨울: 방한 준비, 좌대/실내형/방파제 위주, 안전 우선

2. 날씨별 추천
- 맑음: 장시간 야외 낚시 가능, 포인트 이동형 일정
- 흐림: 입질 기대 가능, 안정적인 방파제/항구 추천
- 비: 우비, 방수장비, 미끄럼 주의, 무리한 갯바위 금지
- 강풍: 낚시 취소 또는 실내 대안 추천, 안전 최우선
- 추움: 방한복, 핫팩, 짧은 낚시 시간, 숙소 가까운 포인트 추천
- 더움: 새벽/저녁 위주, 그늘, 수분 보충, 낮 시간 휴식

3. 일정 구성
- 1일차 오후 출발
- 포인트 도착
- 저녁 낚시
- 숙소 체크인
- 야식 또는 회/매운탕
- 2일차 새벽 낚시
- 아침 식사
- 주변 관광 또는 카페
- 귀가

4. 답변 형식
다음 형식으로 답변해:

🎣 추천 낚시 여행 요약
- 지역:
- 추천 시기:
- 추천 어종:
- 추천 포인트 유형:
- 날씨별 주의점:

📅 1박 2일 일정
[1일차]
- 시간대별 일정

[2일차]
- 시간대별 일정

🌦 날씨별 대안 플랜
- 맑을 때:
- 비 올 때:
- 바람이 강할 때:
- 추울 때:

🎒 준비물 체크리스트
- 낚시 장비
- 의류
- 음식/간식
- 안전용품

💰 예상 예산
- 교통비
- 숙박비
- 식비
- 낚시 비용
- 총 예상 비용

⚠️ 안전 주의사항
- 위험한 장소는 피하라고 안내
- 기상 악화 시 낚시를 강행하지 말라고 안내
- 갯바위, 방파제, 야간 낚시 안전을 강조

말투는 친절하고 현실적으로 해줘.
모르는 정보가 있으면 먼저 필요한 질문을 해줘.
"""
            }
        ]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("예: 5월에 강릉으로 1박 2일 바다낚시 가고 싶어요. 날씨는 흐림이에요."):

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
