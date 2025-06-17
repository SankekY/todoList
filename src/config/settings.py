from pydantic_settings import BaseSettings
from pydantic import BaseModel


class JWTConfig(BaseModel):
    pass

class DataBaseConfig(BaseModel):
    pass

class ServerConfig(BaseModel):
    pass

class Settings(BaseSettings):
    jwt: JWTConfig = JWTConfig()
    db: DataBaseConfig = DataBaseConfig()
    server: ServerConfig = ServerConfig()

config = Settings()