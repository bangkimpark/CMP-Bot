import streamlit as st 
import markdown 
import io 
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer 
from reportlab.lib.styles import getSampleStyleSheet 
from reportlab.lib.pagesizes import A4 
from reportlab.pdfbase import pdfmetrics 
from reportlab.pdfbase.ttfonts import TTFont 
from reportlab.lib.styles import ParagraphStyle
from services.llm_service import LLMService
# ---------------------- # 설정 # ---------------------- 
# 
def setup_page(): 
    st.set_page_config(page_title="NHN Chat UI", page_icon="🤖") 
    st.title("🤖 NHN CHAT BOT") 

#---------------------- # 세션 상태 초기화 # ---------------------- 
def init_session_state(): 
    if "selected_mode" not in st.session_state: 
        st.session_state.selected_mode = None 

    if "messages" not in st.session_state: 
        st.session_state.messages = { "mode_a": [], "mode_b": [] } 
                
# ---------------------- # 상단 버튼 영역 # ---------------------- 
def render_mode_selector(): 
    col1, col2 = st.columns(2) 
    with col1: 
        if st.button("ES 쿼리 생성"): 
            st.session_state.selected_mode = "mode_a" 
    with col2: 
        if st.button("리소스 보고서 생성"): 
            st.session_state.selected_mode = "mode_b" 
    st.divider() 

def get_initial_message(mode: str) -> str: 
    if mode == "mode_a": 
        return ( 
            "안녕하세요 👋\n" "Elasticsearch 쿼리 생성 봇입니다.\n\n" "- 자연어로 원하는 조건을 입력해 주세요\n" "- 예: 최근 10분간 메모리 가용량이 1GB 미만인 vm 조회" ) 
    elif mode == "mode_b": return ( "안녕하세요 👋\n" "리소스/운영 보고서 생성 봇입니다.\n\n" "- 보고서 목적과 범위를 입력해 주세요\n" "- 예: 운영 리소스 모니터링 현황 보고서" ) 
    return "" 

def markdown_to_pdf(markdown_text: str) -> bytes: 
    pdfmetrics.registerFont( TTFont("NotoSansKR", "fonts/NotoSansKR-Regular.ttf") ) 
    
    buffer = io.BytesIO() 
    
    doc = SimpleDocTemplate( buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40, ) 
    styles = getSampleStyleSheet() 
    
    # 한글 폰트 스타일 정의 
    styles.add( ParagraphStyle( name="Korean", fontName="NotoSansKR", fontSize=10, leading=14, ) ) 
    story = [] 
    # Markdown → HTML 
    html = markdown.markdown(markdown_text) 
    # HTML을 단락 단위로 분리 
    for line in html.split("\n"): 
        if line.strip(): 
            story.append(Paragraph(line, styles["Korean"])) 
            story.append(Spacer(1, 12)) 
    doc.build(story) 
    buffer.seek(0) 
    return buffer.read() 

# ---------------------- # 응답 생성 로직 (나중에 LLM 연결 지점) # ---------------------- 
def generate_response(mode: str, prompt: str) -> str: 
    if mode == "mode_a": # 답변 샘플 (추후 llm 답변으로 변경) 
        query = """ 
        # ```json
        # GET nhn-monitoring_api-realtime-*/_search
        # {
        #     "size": 0,
        #     "query": {
        #         "bool": {
        #             "filter": [
        #                 { "term": { "workload_type": "vm" } },
        #                 { "term": { "data_name": "memory_available" } },
        #                 {
        #                     "range": {
        #                         "@timestamp": {
        #                             "gte": "now-10m",
        #                             "lte": "now"
        #                         }
        #                     }
        #                 },
        #                 {
        #                     "range": {
        #                         "data_value": {
        #                             "lt": 1073741824
        #                         }
        #                     }
        #                 }
        #             ]
        #         }
        #     },
        #     "aggs": {
        #         "by_vm": {
        #             "terms": {
        #                 "field": "vm_id",
        #                 "size": 100
        #             },
        #             "aggs": {
        #                 "latest": {
        #                     "top_hits": {
        #                         "size": 1,
        #                         "sort": [
        #                             { "@timestamp": { "order": "desc" } }
        #                         ],
        #                         "_source": {
        #                             "includes": [
        #                                 "vm_name",
        #                                 "instance_ip",
        #                                 "cluster_id",
        #                                 "data_value",
        #                                 "@timestamp"
        #                             ]
        #                         }
        #                     }
        #                 }
        #             }
        #         }
        #     }
        # }       
        # """
        answer=LLMService()
        return f"{answer.test_ask(query)}"
    elif mode == "mode_b":
        # 답변 샘플 (추후 llm 답변으로 변경)
        answer = """
            # 운영 리소스 모니터링 현황 보고서

            ## 1. 개요
            본 보고서는 모니터링 API를 통해 수집된 VM 리소스 지표를 기반으로
            운영 환경의 안정성을 점검하기 위해 작성되었습니다.

            본 보고서는 실시간 메모리 가용량 데이터를 중심으로
            리소스 임계 상태 여부를 분석합니다.

            ---

            ## 2. 모니터링 대상 및 기준

            - 대상 리소스: 가상머신(VM)
            - 데이터 출처: nhn-monitoring API (realtime)
            - 주요 지표: 메모리 가용량 (`memory_available`)
            - 측정 단위: Byte
            - 점검 기준:
            - 정상: 1GB 이상
            - 주의: 512MB ~ 1GB
            - 위험: 512MB 미만

            ---

            ## 3. VM 메모리 가용량 현황 요약

            | VM 이름 | VM ID | IP 주소 | 클러스터 | 메모리 가용량(GB) | 상태 |
            |-------|------|--------|---------|------------------|------|
            | inje_instance2 | 0001e0d8-a0d2-473b-8b19-21e66a517586 | 10.1.59.162 | v002 | 3.23 | 정상 |
            | example_vm01 | xxxx | 10.1.59.163 | v002 | 0.78 | 주의 |
            | example_vm02 | yyyy | 10.1.59.164 | v003 | 0.42 | 위험 |

            ---

            ## 4. 이상 징후 및 분석

            - 일부 VM에서 메모리 가용량이 지속적으로 감소하는 경향이 확인됨
            - 메모리 사용량 증가 시점과 특정 애플리케이션 배포 이력 간 상관 가능성 존재
            - 위험 상태 VM은 단기 내 장애 발생 가능성 존재

            ---

            ## 5. 조치 및 권고 사항

            - 위험 상태 VM:
            - 프로세스 점검 및 메모리 사용량 상위 프로세스 확인
            - 필요 시 VM 재기동 또는 스케일 업 검토
            - 주의 상태 VM:
            - 24시간 모니터링 강화
            - 임계치 하향 여부 검토

            ---

            ## 6. 결론
            모니터링 API 기반 실시간 리소스 수집은
            운영 안정성 확보에 중요한 지표로 활용 가능하며,
            지속적인 임계치 관리와 선제적 대응이 필요합니다.

            ---
            작성일: 2026-01-28

            """
        return f"{answer}"
    return "지원하지 않는 모드입니다."


# ----------------------
# 채팅 UI
# ----------------------
def render_chat(mode: str):
    # 최초 진입 시 assistant 안내 메시지
    if len(st.session_state.messages[mode]) == 0:
        initial_msg = get_initial_message(mode)
        st.session_state.messages[mode].append({
            "role": "assistant",
            "content": initial_msg
        })
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
    with st.chat_message("assistant"):
        with st.spinner("🤖 답변을 생성 중입니다..."):
            response = generate_response(mode, prompt)
            st.markdown(response)

    st.session_state.messages[mode].append({
        "role": "assistant",
        "content": response
    })


    # 보고서 모드일 경우 PDF 다운로드 버튼
    if mode == "mode_b":
        last_msg = st.session_state.messages[mode][-1]

        if last_msg["role"] == "assistant":
            pdf_bytes = markdown_to_pdf(last_msg["content"])

            st.download_button(
                label="📄 보고서 PDF 다운로드",
                data=pdf_bytes,
                file_name="siem_report.pdf",
                mime="application/pdf"
            )


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