from pydantic_settings import BaseSettings
from pydantic import BaseModel
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
# DB_PATH = BASE_DIR / "db.sqlite3"

class JWTConfig(BaseModel):
    public_key: Path = BASE_DIR / "secret" / "jwt-public.pem" 
    secret_key: Path = BASE_DIR / "secret" / "jwt-privet.pem"
    alghorithm: str = "RS256"
    access_token_expire_minute: int = 30

class DataBaseConfig(BaseModel):
    pass

class ServerConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000

class Settings(BaseSettings):
    jwt: JWTConfig = JWTConfig()
    db: DataBaseConfig = DataBaseConfig()
    server: ServerConfig = ServerConfig()

config = Settings()