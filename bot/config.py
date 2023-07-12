from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    EXCEL_PATH: str
    SERVICE_ACCOUNT_CREDENTIALS_PATH: str
    SPREADSHEET_ID: str

    POSTGRES_DB_NAME: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_USER: str

    REDIS_HOSTS: str
    REDIS_PORT: str
    REDIS_PASSWORD: SecretStr

    REDIS_COMMANDER_PORT: str

    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'


config = Settings()
