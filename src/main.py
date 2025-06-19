from fastapi import FastAPI
from api.routes import main_router
from config.settings import config
from contextlib import asynccontextmanager
from repository.database.base import BaseRepository
import uvicorn

app = FastAPI(
    lifespan=lifespan
)
app.include_router(main_router)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Data Table is Create")
    yield 
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        print("Data Table is drop")

if __name__=="__main__":
    uvicorn.run(
        app="main:app",
        host=config.server.host,
        port=config.server.port,
        reload=True
    )