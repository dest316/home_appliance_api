from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER


# Строка подключения к базе данных
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
Base = declarative_base()


# Движок, используемый для создания асинхронных сессий для работы с базой данных
engine = create_async_engine(DATABASE_URL)

# Фабрика для создания асинхронных сессий с помощью движка engine
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Функция, возвращающая по мере требования асинхронную сессию для подключения к базе данных
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session