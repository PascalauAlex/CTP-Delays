from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    database_url: str
    tranzy_api_key: str
    tranzy_base_url: str = "https://api.tranzy.ai/v1/opendata"
    tranzy_agency_id: int = 2
    poll_interval_seconds: int = 30


settings = Settings()