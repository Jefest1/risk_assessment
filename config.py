from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    HF_TOKEN: str
    MODEL_ID: str
    OPENAI_API_KEY: str
    GPT_MODEL: str
    PHI_MODEL: str
    META_MODEL: str
    CLAUDE: str
    CLAUDE_API_KEY: str

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
