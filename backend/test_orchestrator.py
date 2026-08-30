import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.orchestrator.research_orchestrator import ResearchOrchestrator


async def main():
    orchestrator = ResearchOrchestrator()
    query = "Latest developments in AI multi-agent workflows"

    print(f"Executing complete pipeline for: '{query}'...\n")
    result = await orchestrator.research(query=query)

    print("===== SOURCES =====")
    for idx, s in enumerate(result["sources"], 1):
        print(f"[{idx}] {s['title']} ({s['url']})")

    print("\n===== FINAL SYNTHESIZED REPORT =====\n")
    print(result["report"])


if __name__ == "__main__":
    asyncio.run(main())