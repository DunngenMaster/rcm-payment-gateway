import json
from pathlib import Path
from cryptography.fernet import Fernet
from app.core.config import settings
from app.core.constants import OAUTH_PARAM_MERCHANT_ID, TOKEN_FILE_PATH, TOKEN_JSON_KEY_ACCESS_TOKEN

class TokenStore:
    def __init__(self, file_path=TOKEN_FILE_PATH):
        self.file_path = file_path
        if not settings.TOKEN_ENCRYPTION_KEY:
            raise ValueError("TOKEN_ENCRYPTION_KEY not set in environment variables")
        self.cipher = Fernet(settings.TOKEN_ENCRYPTION_KEY.encode())

    def save_token(self, token_data: dict):
        json_str = json.dumps(token_data)
        encrypted = self.cipher.encrypt(json_str.encode()).decode()
        with open(self.file_path, "w") as f:
            f.write(encrypted)

    def load_token(self):
        file_path = Path(self.file_path)
        if not file_path.exists():
            return None
        try:
            with open(self.file_path, "r") as f:
                encrypted = f.read()
            decrypted = self.cipher.decrypt(encrypted.encode()).decode()
            return json.loads(decrypted)
        except Exception:
            return None

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

token_store = TokenStore()