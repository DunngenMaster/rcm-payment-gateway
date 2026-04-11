import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        self.CLOVER_CLIENT_ID = os.getenv("CLOVER_CLIENT_ID")
        self.CLOVER_CLIENT_SECRET = os.getenv("CLOVER_CLIENT_SECRET")
        self.CLOVER_REDIRECT_URI = os.getenv("CLOVER_REDIRECT_URI")
        self.CLOVER_AUTH_BASE_URL = os.getenv("CLOVER_AUTH_BASE_URL")
        self.CLOVER_API_BASE_URL = os.getenv("CLOVER_API_BASE_URL")
        self.CLOVER_ECOMMERCE_BASE_URL = os.getenv("CLOVER_ECOMMERCE_BASE_URL")
        self.CLOVER_ECOMMERCE_PUBLIC_TOKEN = os.getenv("CLOVER_ECOMMERCE_PUBLIC_TOKEN")
        self.CLOVER_ECOMMERCE_PRIVATE_TOKEN = os.getenv("CLOVER_ECOMMERCE_PRIVATE_TOKEN")
        self.CLOVER_TOKEN_BASE_URL = os.getenv("CLOVER_TOKEN_BASE_URL")
        self.CLOVER_TEST_API_TOKEN = os.getenv("CLOVER_TEST_API_TOKEN")
        self.CLOVER_TEST_MERCHANT_ID = os.getenv("CLOVER_TEST_MERCHANT_ID")
        self.FRONTEND_URL = os.getenv("FRONTEND_URL")
        self.TOKEN_ENCRYPTION_KEY = os.getenv("TOKEN_ENCRYPTION_KEY")

settings = Settings()