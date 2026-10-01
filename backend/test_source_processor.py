from app.services.source_processor import SourceProcessor


def main():
    processor = SourceProcessor()

    mock_sources = [
        {
            "title": "Duplicate Link",
            "url": "https://example.com/ai-trends/",
            "content": "Multi-agent systems are evolving rapidly.   Lots   of   spaces.",
            "score": 0.82,
        },
        {
            "title": "Duplicate Link Without Slash",
            "url": "https://example.com/ai-trends",
            "content": "Same link duplicate should be skipped.",
            "score": 0.90,
        },
        {
            "title": "Invalid URL Scheme",
            "url": "ftp://example.com/invalid",
            "content": "This should be discarded by urlparse.",
            "score": 0.99,
        },
        {
            "title": "High Quality Source",
            "url": "https://techresearch.org/agents-2026",
            "content": "Autonomous agents will handle complex decomposition tasks.",
            "score": 0.95,
        },
        {
            "title": "Missing Content",
            "url": "https://example.com/empty",
            "content": "",
            "score": 0.50,
        },
    ]

    results = processor.process(mock_sources, max_sources=3)

    print(f"Total processed sources: {len(results)}\n")
    for idx, item in enumerate(results, 1):
        print(f"[{idx}] Score: {item['score']} | Domain: {item['domain']}")
        print(f"    Title: {item['title']}")
        print(f"    URL: {item['url']}")
        print(f"    Content: {item['content']}\n")


if __name__ == "__main__":
    main()