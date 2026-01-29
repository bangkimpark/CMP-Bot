from openai import OpenAI
from config import Config
from datetime import datetime
from prompts.templates import get_query_generation_prompt

class LLMService:
    def __init__(self):
        self.client = OpenAI(
            base_url=Config.OPENROUTER_BASE_URL,
            api_key=Config.OPENROUTER_API_KEY
        )

    def ask_to_llm(self, user_question, index_metadata):
        curr_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        prompt = get_query_generation_prompt(curr_date, index_metadata, user_question)

        response = self.client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            extra_headers={
                "HTTP-Referer": Config.SITE_URL,
                "X-Title": Config.SITE_NAME,
            }
        )
        return response.choices[0].message.content.strip()