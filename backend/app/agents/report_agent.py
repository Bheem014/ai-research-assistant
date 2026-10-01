from typing import List, Dict, Any
from app.services.llm_service import LLMService


class ReportAgent:

    def __init__(self):
        self.llm_service = LLMService()

    def generate_report(
        self,
        query: str,
        sources: List[Dict[str, Any]],
        analysis_text: str,
        critique_text: str,
    ) -> str:
        """
        Synthesizes the draft analysis and critic feedback into a cohesive,
        well-structured final research report.
        """
        system_prompt = (
            "You are a Senior Research Report Writer. Your role is to produce a "
            "comprehensive, polished, and objective research report based on provided "
            "source evidence, analytical findings, and academic critique notes. "
            "Use clear headings, structured bullet points, and maintain an authoritative tone."
        )

        source_references = "\n".join(
            [f"- [{i+1}] {s.get('title', 'Source')} ({s.get('url', 'N/A')})" for i, s in enumerate(sources)]
        )

        user_prompt = f"""Topic: {query}

Reference Sources:
{source_references}

Analysis Notes:
{analysis_text}

Critic Feedback & Validation:
{critique_text}

Please generate the final research report structured with the following sections:
# Executive Summary
# Key Findings & Evidence
# Limitations & Identified Gaps
# Strategic Recommendations
# References
"""

        response = self.llm_service.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        if isinstance(response, dict):
            return response.get("response", "") or response.get("content", "") or str(response)

        return response if response else "No report generated."