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

### 환경 변수 설정
- .env 생성 및 변수 설정

### 실행 방법
- ```streamlit run [ui파일명].py```


### 브랜치 전략
- feature/* 브랜치 생성 후 작업
- 작업 완료 및 테스트 후 PR 생성