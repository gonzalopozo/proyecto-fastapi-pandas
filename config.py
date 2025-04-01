from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DRIVER: str
    DSN: str
    HOST: str
    DB: str
    UID: str
    PWD2: str
    PORT: str