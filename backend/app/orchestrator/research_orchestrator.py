from app.services.search_service import SearchService
from app.services.source_processor import SourceProcessor
from app.agents.analysis_agent import AnalysisAgent
from app.agents.critic_agent import CriticAgent
from app.agents.report_agent import ReportAgent


class ResearchOrchestrator:

    def __init__(self):
        self.search_service = SearchService()
        self.source_processor = SourceProcessor()
        self.analysis_agent = AnalysisAgent()
        self.critic_agent = CriticAgent()
        self.report_agent = ReportAgent()

    async def research(self, query: str) -> dict:
        # Step 1: Tavily Search
        raw_sources = self.search_service.search(query=query, limit=5)

        # Step 2: Deduplicate, Clean, and Rank Sources
        processed_sources = self.source_processor.process(
            sources=raw_sources,
            max_sources=5,
            max_chars_per_source=1000,
        )

        if not processed_sources:
            return {
                "query": query,
                "source_count": 0,
                "sources": [],
                "analysis": "No relevant sources found.",
                "critique": "Skipped.",
                "report": "Unable to generate report without sources.",
            }

        # Step 3: Analysis Agent
        analysis_result = self.analysis_agent.analyze(
            query=query,
            sources=processed_sources,
        )

        # Step 4: Critic Agent Validation
        critique_result = self.critic_agent.evaluate(
            query=query,
            sources=processed_sources,
            analysis_text=analysis_result,
        )

        # Step 5: Report Agent Synthesis
        final_report = self.report_agent.generate_report(
            query=query,
            sources=processed_sources,
            analysis_text=analysis_result,
            critique_text=critique_result,
        )

        return {
            "query": query,
            "source_count": len(processed_sources),
            "sources": processed_sources,
            "analysis": analysis_result,
            "critique": critique_result,
            "report": final_report,
        }