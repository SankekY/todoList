from pydantic import BaseModel, validator
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"

class TokenData(BaseModel):
    sub: int | None = None
    email: str | None = None
    username: str | None = None
    exp: datetime | None = None
    active: bool | None = None

    @validator('sub', pre=True)
    def convert_sub_to_int(cls, v):
        if v is None:
            return None
        try:
            return int(v)
        except (TypeError, ValueError):
            return None