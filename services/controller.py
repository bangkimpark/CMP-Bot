import json
from .llm_service import LLMService
from .es_service import ESService
from .yaml_loader import YamlLoader

class ChatController:
    def __init__(self):
        self.llm = LLMService()
        self.es = ESService()
        # 파일을 동적으로 로드
        self.index_metadata = YamlLoader.load_metadata("monitoring_api.yaml")

    def execute_workflow(self, user_input):
        # 1. LLM 쿼리 생성
        generated_query = self.llm.ask_to_llm(user_input, self.index_metadata)
        clean_query = generated_query.replace("```json", "").replace("```", "").strip()
        query_dict = json.loads(clean_query)

        # 2. ES 검색
        res = self.es.search("nhn-monitoring_api-realtime-*", query_dict)
        
        return query_dict, res