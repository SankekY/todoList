from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config.settings import config

engine = create_async_engine(
    url=config.db.url,
    echo=config.db.echo,
    max_overflow=config.db.max_overflow,
)

session_factory = sessionmaker(
    bind=engine,
    autoflush=False,
    class_=AsyncSession,
)

async def get_session() -> AsyncSession:
    async with session_factory() as session:
        yield session

