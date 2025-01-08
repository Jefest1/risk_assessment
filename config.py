from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    HF_TOKEN: str
    MODEL_ID: str
    OPENAI_API_KEY: str
    GPT_MODEL: str

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
