import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        self.CLOVER_CLIENT_ID = os.getenv("CLOVER_CLIENT_ID", "")
        self.CLOVER_CLIENT_SECRET = os.getenv("CLOVER_CLIENT_SECRET", "")
        self.CLOVER_REDIRECT_URI = os.getenv("CLOVER_REDIRECT_URI", "")
        self.CLOVER_AUTH_BASE_URL = os.getenv("CLOVER_AUTH_BASE_URL", "https://sandbox.dev.clover.com")
        self.CLOVER_API_BASE_URL = os.getenv("CLOVER_API_BASE_URL", "https://apisandbox.dev.clover.com")
        self.CLOVER_TEST_API_TOKEN = os.getenv("CLOVER_TEST_API_TOKEN", "")  # For development
        self.CLOVER_TEST_MERCHANT_ID = os.getenv("CLOVER_TEST_MERCHANT_ID", "")  # For development
        self.FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

settings = Settings()