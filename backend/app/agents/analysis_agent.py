from app.services.llm_service import LLMService


class AnalysisAgent:

    def __init__(self):
        self.llm = LLMService()

    def analyze(self, query: str, sources: list) -> str:

        source_text = ""

        for i, source in enumerate(sources, start=1):
            title = source.get("title", "")
            url = source.get("url", "")
            content = source.get("content", "")

            source_text += f"""
SOURCE {i}
Title: {title}
URL: {url}
Content:
{content}

--------------------------------
"""

        system_prompt = """
You are an AI research analysis agent.

Your job is to analyze information from web sources
and produce evidence-based research findings.

Rules:
1. Use only information provided in the sources.
2. Do not invent facts.
3. Identify the most important findings.
4. Compare information when sources disagree.
5. Mention uncertainty when evidence is weak.
6. Keep the answer clear and structured.
"""

        user_prompt = f"""
Research question:
{query}

Web sources:
{source_text}

Analyze these sources and provide:

1. Research Summary
2. Key Findings
3. Important Evidence
4. Contradictions or Uncertainty
5. Overall Conclusion
"""

        return self.llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )