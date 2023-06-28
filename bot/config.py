from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    EXCEL_PATH: str

    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'


config = Settings()
