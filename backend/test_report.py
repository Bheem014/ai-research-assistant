import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.agents.report_agent import ReportAgent


def main():
    print("Initializing ReportAgent...")
    report_agent = ReportAgent()

    query = "Applications of Multi-Agent AI Systems"
    sources = [
        {
            "title": "Autonomous Systems 2026",
            "url": "https://example.com/autonomous-2026",
        }
    ]
    sample_analysis = "Multi-agent systems divide complex tasks across specialized agents for higher accuracy."
    sample_critique = "Reliability 8/10. Claim is well-grounded in reference text."

    print("Generating final research report...\n")
    report = report_agent.generate_report(
        query=query,
        sources=sources,
        analysis_text=sample_analysis,
        critique_text=sample_critique,
    )

    print("===== FINAL REPORT =====")
    print(report)


if __name__ == "__main__":
    main()