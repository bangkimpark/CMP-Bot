import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    LLM_HOST = os.environ.get('LLM_HOST')
    LLM_API_KEY = os.environ.get('LLM_API_KEY')
    ES_HOST = os.getenv("ES_HOST")
    ES_USER = os.getenv("ES_USER")
    ES_PASSWORD = os.getenv("ES_PASSWORD")
    SITE_URL=os.getenv("SITE_URL")
    SITE_NAME=os.getenv("SITE_NAME")

