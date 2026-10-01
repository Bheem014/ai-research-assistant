from typing import List, Dict, Any
from app.services.llm_service import LLMService


class CriticAgent:

    def __init__(self):
        self.llm_service = LLMService()

    def evaluate(self, query: str, sources: List[Dict[str, Any]], analysis_text: str) -> str:
        """
        Reviews and compares analysis points against the retrieved sources.
        """
        system_prompt = (
            "You are an academic review assistant. Your role is to cross-reference "
            "draft notes against reference source text. Summarize which points are "
            "directly covered in the references, which points are missing reference backing, "
            "and suggest improvements."
        )

        source_text = "\n\n".join(
            [f"Reference [{i+1}] ({s.get('title', 'Source')}):\n{s.get('content', '')}" for i, s in enumerate(sources)]
        )

        user_prompt = f"""Topic: {query}

Reference Sources:
{source_text}

Draft Notes to Review:
{analysis_text}

Provide an academic review with:
- Supported points from references
- Points not mentioned in references
- Reliability assessment (1-10)"""

        response = self.llm_service.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        if isinstance(response, dict):
            return response.get("response", "") or response.get("content", "") or str(response)

        return response if response else "No critique generated."