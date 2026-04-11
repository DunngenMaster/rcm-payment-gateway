class OAuthPayload:
    def __init__(self, client_id: str, client_secret: str, code: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.code = code
        self.redirect_uri = redirect_uri

    def to_dict(self) -> dict:
        return {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": self.code,
            "redirect_uri": self.redirect_uri
        }
