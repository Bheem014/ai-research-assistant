from tavily import TavilyClient

from app.core.config import settings


class SearchService:

    def __init__(self):
        self.client = TavilyClient(
            api_key=settings.tavily_api_key
        )

    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[dict]:

        response = self.client.search(
            query=query,
            search_depth="advanced",
            max_results=limit,
            include_answer=False,
        )

        results = []

        for item in response.get("results", []):
            results.append(
                {
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "content": item.get("content", ""),
                    "score": item.get("score"),
                }
            )

        return results