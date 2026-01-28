### 가상환경 설정
- Mac/Linux
```
python3 -m venv venv
source venv/bin/activate
```
- Windows
```
python -m venv venv
venv\Scripts\activate
```

### 라이브러리 설치
- 라이브러리 설치
  - ```pip install -r requirements.txt```
- 추가 라이브러리 설치 후 requirements 파일에 추가
  - ```pip freeze > requirements.txt```

### 디렉터리 구조
```
chatbot-pilot/
├── .env                # API 키, ES 접속 비번 등 민감 정보
├── chat_ui.py          # Streamlit 실행 파일
├── config.py           # 환경 변수 로드 및 전역 설정
├── requirements.txt    # 설치 필요한 라이브러리 목록
│
├── services/           # 비즈니스 로직
│   ├── __init__.py     # 패키지 인식용
│   ├── llm_service.py  # LLM 통신 및 쿼리 생성 로직
│   ├── es_service.py   # ES 쿼리 실행 및 매핑 정보 조회
│   └── controller.py   # ui는 이 파일만 보도록
│
├── prompts/            # 프롬프트 관리
│   ├── __init__.py
│   └── templates.py    # 프롬프트를 변수/클래스로 관리
│
└── utils/              # 기타 공통 기능
    └── logger.py       # 디버깅용 로그 설정
```

### 환경 변수 설정
- .env 생성 및 변수 설정

### 실행 방법
- ```streamlit run [ui파일명].py```


### 브랜치 전략
- feature/* 브랜치 생성 후 작업
- 작업 완료 및 테스트 후 PR 생성