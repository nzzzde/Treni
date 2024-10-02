import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self):
        load_dotenv()
        self.TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
        self.DB_NAME = os.getenv("DB_NAME")
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD")
        self.DB_HOST = os.getenv("DB_HOST", "localhost")
        self.DB_PORT = os.getenv("DB_PORT", "5432")


config = Config()
