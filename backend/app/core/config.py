from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Research Assistant"
    environment: str = "development"

    tavily_api_key: str

    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "llama3.2:1b"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()