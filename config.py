import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    LLM_HOST = os.environ.get('LLM_HOST')
    LLM_API_KEY = os.environ.get('LLM_API_KEY')
    ES_HOST = os.environ.get('ES_HOST')
    ES_API_KEY = os.environ.get('ES_API_KEY')
