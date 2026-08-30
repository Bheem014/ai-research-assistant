from app.agents.analysis_agent import AnalysisAgent


def main():

    agent = AnalysisAgent()

    sources = [
        {
            "title": "AI Trends 2026",
            "url": "https://example.com/ai-trends",
            "content": """
            Artificial intelligence is increasingly being used
            for automation, software development, data analysis,
            and multi-agent systems.
            """
        },
        {
            "title": "Future of AI",
            "url": "https://example.com/future-ai",
            "content": """
            Multi-agent systems are becoming increasingly important
            because multiple specialized AI agents can collaborate
            on complex tasks.
            """
        }
    ]

    result = agent.analyze(
        query="What are the important AI trends in 2026?",
        sources=sources,
    )

    print("\n===== ANALYSIS RESULT =====\n")
    print(result)


if __name__ == "__main__":
    main()