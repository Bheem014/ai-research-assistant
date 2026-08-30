from urllib.parse import urlparse
from typing import List, Dict, Any


class SourceProcessor:

    def process(
        self,
        sources: List[Dict[str, Any]],
        max_sources: int = 5,
        max_chars_per_source: int = 1000,
    ) -> List[Dict[str, Any]]:
        """
        Clean, validate, deduplicate, rank, and truncate research sources.
        """
        processed = []
        seen_urls = set()

        for source in sources:
            title = source.get("title", "").strip()
            url = source.get("url", "").strip()
            content = source.get("content", "").strip()
            score = source.get("score", 0)

            # Skip incomplete sources
            if not title or not url or not content:
                continue

            # Validate URL
            parsed_url = urlparse(url)
            if parsed_url.scheme not in {"http", "https"}:
                continue

            # Remove duplicate URLs
            normalized_url = url.rstrip("/")
            if normalized_url in seen_urls:
                continue

            seen_urls.add(normalized_url)

            # Clean excessive whitespace and truncate to preserve memory/tokens
            cleaned_content = " ".join(content.split())
            truncated_content = cleaned_content[:max_chars_per_source].strip()

            processed.append(
                {
                    "title": title,
                    "url": normalized_url,
                    "content": truncated_content,
                    "score": float(score or 0),
                    "domain": parsed_url.netloc,
                }
            )

        # Highest relevance first
        processed.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        return processed[:max_sources]