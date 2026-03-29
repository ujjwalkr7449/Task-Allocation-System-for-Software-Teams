from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Task Allocation System"
    api_prefix: str = "/api/v1"
    secret_key: str = "change-this-secret-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24
    database_url: str = "sqlite:///./task_allocation.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
