from pydantic import BaseModel


class CodeExchangeRequest(BaseModel):
    code: str
    merchant_id: str | None = None
