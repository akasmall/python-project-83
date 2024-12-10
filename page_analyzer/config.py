import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    DATABASE_URL = os.environ.get("DATABASE_URL")

    def __init__(self):
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY not found in environment variables")
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL not found in environment variables")


config = Config()
