def get_query_generation_prompt(curr_date, metadata, user_question):
    return f"""
    당신은 Elasticsearch 전문가입니다. 
    제공된 인덱스 정보를 바탕으로 사용자의 질문에 답하는 **순수한 JSON 형식의 Query DSL**만 생성하세요.

    [제약 사항 - 반드시 지킬 것]
    1. 답변에 '설명', '인사', 'GET 인덱스명' 같은 텍스트를 절대 포함하지 마세요.
    2. 마크다운 코드 블록(```json)도 사용하지 말고 오직 {{ }} 로 시작하는 JSON 데이터만 출력하세요.
    3. 결과는 반드시 하나의 JSON 오브젝트여야 합니다.
    
    오늘 날짜: {curr_date}
    인덱스 정보: {metadata}
    질문: {user_question}
    """