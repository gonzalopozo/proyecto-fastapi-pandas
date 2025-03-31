from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DRIVER: str
    DSN: str
    HOST: str
    DB: str
    UID: str
    PWD: str
    PORT: str