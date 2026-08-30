import ollama
from app.core.config import settings


class LLMService:

    def __init__(self):
        self.client = ollama.Client(host=settings.ollama_host)
        self.model = settings.ollama_model

    def generate(self, system_prompt: str, user_prompt: str, max_tokens: int = 250) -> str:
        """
        Sends chat messages to Ollama with constrained token limits
        and tuned CPU threading for 8GB RAM / i5-8250U.
        """
        try:
            response = self.client.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                options={
                    "num_predict": max_tokens, # Caps response length to prevent long generation loops
                    "num_ctx": 2048,           # Lowers RAM usage
                    "num_thread": 4,           # Matches physical CPU cores
                    "temperature": 0.2,
                },
            )
            return response["message"]["content"]
        except Exception as e:
            return f"LLM Generation Error: {str(e)}"