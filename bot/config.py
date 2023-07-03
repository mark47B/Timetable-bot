from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    EXCEL_PATH: str
    SERVICE_ACCOUNT_CREDENTIALS_PATH: str
    SPREADSHEET_ID: str


    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'


config = Settings()
