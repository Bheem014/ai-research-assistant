from app.services.search_service import SearchService


def main():

    service = SearchService()

    results = service.search(
        "latest artificial intelligence trends",
        limit=5,
    )

    print("\nSEARCH RESULTS\n")

    for index, result in enumerate(results, start=1):

        print(f"{index}. {result['title']}")
        print(f"   URL: {result['url']}")
        print(f"   Score: {result['score']}")
        print(
            f"   Content: "
            f"{result['content'][:200]}..."
        )
        print()


if __name__ == "__main__":
    main()