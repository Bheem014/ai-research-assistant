from app.services.llm_service import LLMService


def main():

    llm = LLMService()

    response = llm.generate(
        system_prompt=(
            "You are an AI research assistant. "
            "Give concise and factual answers."
        ),
        user_prompt=(
            "Explain what a research assistant "
            "does in 3 sentences."
        ),
    )

    print("\nLLM RESPONSE\n")
    print(response)


if __name__ == "__main__":
    main()