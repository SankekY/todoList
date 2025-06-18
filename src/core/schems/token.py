from pydantic import BaseModel
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"

class TokenData(BaseModel):
    sub: int | None = None
    username: str | None = None
    expire: datetime | None = None
    active: bool | None = None