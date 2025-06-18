from  config.settings import config
from jose import jwt
from jose.jwt import JWTError
from datetime import timedelta, timezone, datetime
import bcrypt

def encode_jwt(
    payload: dict,
    privet_key: str = config.jwt.secret_key.read_text(),
    alghorithm: str = config.jwt.alghorithm,
    access_token_expire: int = config.jwt.access_token_expire_minute,
    expire_time_delta: timedelta | None = None
) -> str:
    expire: datetime
    if not expire_timedelta:
        expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    else:
        expire = datetime.now(timezone.utc) + expire_timedelta

    to_encode = payload.copy()
    to_encode.update(exp=expire)
    return jwt.encode(
        claims=to_encode,
        key=privet_key,
        algorithm=alghorithm
    )

def decode_jwt(
    token: str,
    public_key: str = config.jwt.public_key.read_text(),
    alghorithm: str = config.jwt.alghorithm,
) -> dict:
    return jwt.decode(
        token=token,
        key=public_key,
        algorithms=[alghorithm]
    )

def hash_password(
    payload_password: str
) -> str:
    salt  = bcrypt.gensalt()
    return bcrypt.hashpw(
        password=payload_password,
        salt=salt
    )

def verefy_passowrd(
    payload_password: str,
    hash_password: str
) -> bool:
    return bcrypt.checkpw(
        password=payload_password,
        hashed_password=hash_password
    )
        
