import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL")
    ES_HOST = os.getenv("ES_HOST")
    ES_USER = os.getenv("ES_USER")
    ES_PASSWORD = os.getenv("ES_PASSWORD")
    SITE_URL=os.getenv("SITE_URL")
    SITE_NAME=os.getenv("SITE_NAME")