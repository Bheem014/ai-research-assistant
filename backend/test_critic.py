import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.agents.critic_agent import CriticAgent


def main():
    print("Initializing CriticAgent...")
    critic = CriticAgent()

    query = "AI multi-agent applications"
    sources = [
        {
            "title": "Multi-Agent Trends",
            "content": "Multi-agent systems improve efficiency through parallel task division and specialized role assignments.",
        }
    ]
    sample_analysis = (
        "Multi-agent systems improve efficiency by dividing tasks across specialized agents. "
        "They also reduce server hosting costs to zero."
    )

    print("Sending evaluation request to local LLM...\n")
    evaluation = critic.evaluate(
        query=query,
        sources=sources,
        analysis_text=sample_analysis,
    )

    print("===== CRITIQUE RESULT =====")
    print(evaluation)


if __name__ == "__main__":
    main()