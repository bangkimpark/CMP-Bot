from elasticsearch import Elasticsearch
from config import Config
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ESService:
    def __init__(self):
        self.es = Elasticsearch(
            Config.ES_HOST,
            basic_auth=(Config.ES_USER, Config.ES_PASSWORD),
            verify_certs=False
        )

    def search(self, index_pattern, query_dict):
        return self.es.search(index=index_pattern, body=query_dict)