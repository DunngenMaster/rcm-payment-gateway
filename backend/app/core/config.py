import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        self.CLOVER_CLIENT_ID = os.getenv("CLOVER_CLIENT_ID", "")
        self.CLOVER_CLIENT_SECRET = os.getenv("CLOVER_CLIENT_SECRET", "")
        self.CLOVER_REDIRECT_URI = os.getenv("CLOVER_REDIRECT_URI", "")
        self.CLOVER_BASE_URL = os.getenv("CLOVER_BASE_URL", "")
        self.FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

settings = Settings()