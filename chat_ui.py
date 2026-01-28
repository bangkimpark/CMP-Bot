import streamlit as st


# ----------------------
# 설정
# ----------------------
def setup_page():
    st.set_page_config(page_title="Multi Chat UI", page_icon="🤖")
    st.title("🤖 기능 선택형 챗봇")


# ----------------------
# 세션 상태 초기화
# ----------------------
def init_session_state():
    if "selected_mode" not in st.session_state:
        st.session_state.selected_mode = None

    if "messages" not in st.session_state:
        st.session_state.messages = {
            "mode_a": [],
            "mode_b": []
        }


# ----------------------
# 상단 버튼 영역
# ----------------------
def render_mode_selector():
    col1, col2 = st.columns(2)

    with col1:
        if st.button("ES 쿼리 생성"):
            st.session_state.selected_mode = "mode_a"

    with col2:
        if st.button("리소스 보고서 생성"):
            st.session_state.selected_mode = "mode_b"

    st.divider()


# ----------------------
# 응답 생성 로직 (나중에 LLM 연결 지점)
# ----------------------
def generate_response(mode: str, prompt: str) -> str:
    if mode == "mode_a":
        answer = "llm_a" # 추후 llm 답변으로 변경
        return f"쿼리 생성 봇 응답: {answer}"
    elif mode == "mode_b":
        answer = "llm_b" # 추후 llm 답변으로 변경
        return f"보고서 생성 봇 응답: {answer}"
    return "지원하지 않는 모드입니다."


# ----------------------
# 채팅 UI
# ----------------------
def render_chat(mode: str):
    for msg in st.session_state.messages[mode]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("메시지를 입력하세요")

    if not prompt:
        return

    # user message
    st.session_state.messages[mode].append({
        "role": "user",
        "content": prompt
    })
    with st.chat_message("user"):
        st.markdown(prompt)

    # assistant message
    response = generate_response(mode, prompt)
    st.session_state.messages[mode].append({
        "role": "assistant",
        "content": response
    })
    with st.chat_message("assistant"):
        st.markdown(response)


# ----------------------
# main
# ----------------------
def main():
    setup_page()
    init_session_state()
    render_mode_selector()

    if st.session_state.selected_mode:
        render_chat(st.session_state.selected_mode)
    else:
        st.info("⬆️ 위에서 기능을 선택하면 채팅이 시작됩니다.")


if __name__ == "__main__":
    main()
