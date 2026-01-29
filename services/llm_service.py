from openai import OpenAI
from config import Config
from datetime import datetime
from prompts.templates import get_query_generation_prompt


class LLMService:
    def __init__(self):
        self.client = OpenAI(
            base_url=Config.LLM_HOST,
            api_key=Config.LLM_API_KEY
        )
        self.model = "google/gemini-2.0-flash-001"


    def ask_to_llm(self, user_question, index_metadata):
        curr_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        prompt = get_query_generation_prompt(curr_date, index_metadata, user_question)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            extra_headers={
                "HTTP-Referer": Config.SITE_URL,
                "X-Title": Config.SITE_NAME,
            }
        )
        return response.choices[0].message.content.strip()


    def test_ask(self, query: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": query}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"에러 발생: {e}"


if __name__ == "__main__":
    llm = LLMService()
    print(llm.test_ask("자기소개 해봐"))
