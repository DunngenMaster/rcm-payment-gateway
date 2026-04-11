import json
import os
from app.core.constants import (
    OAUTH_PARAM_MERCHANT_ID,
    TOKEN_FILE_PATH,
    FILE_MODE_READ,
    FILE_MODE_WRITE,
    TOKEN_JSON_KEY_ACCESS_TOKEN,
)

class TokenStore:
    def __init__(self, file_path=TOKEN_FILE_PATH):
        self.file_path = file_path

    def save_token(self, token_data: dict):
        with open(self.file_path, FILE_MODE_WRITE) as file:
            json.dump(token_data, file, indent=2)

    def load_token(self):
        if not os.path.exists(self.file_path):
            return None
        with open(self.file_path, FILE_MODE_READ) as file:
            return json.load(file)

    def get_access_token(self):
        token_data = self.load_token()
        if not token_data:
            return None
        return token_data.get(TOKEN_JSON_KEY_ACCESS_TOKEN)
    
    def get_merchant_id(self):
        token_data = self.load_token()
        if not token_data:
            return None
        return token_data.get(OAUTH_PARAM_MERCHANT_ID)

token_store = TokenStore()