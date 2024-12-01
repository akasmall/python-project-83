import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    # DATABASE_URL = os.getenv('DATABASE_URL')
    DATABASE_URL = os.environ.get("DATABASE_URL")

    def __init__(self):
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY не найден в переменных окружения")
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL не найден в переменных окружения")


config = Config()
