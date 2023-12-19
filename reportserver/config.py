from pydantic_settings import BaseSettings, SettingsConfigDict

from .reportgen.config import GenerationSettings


class Settings(BaseSettings):
    report: GenerationSettings

    model_config = SettingsConfigDict(
        secrets_dir="secrets/",
        env_prefix="REPORT_SERVER_",
        env_file=".env",
    )
