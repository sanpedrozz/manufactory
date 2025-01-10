import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from shared.config.config import settings

# Настройка логгера SQLAlchemy
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

# Создание асинхронного подключения
async_engine = create_async_engine(
    str(settings.manufactory_db_url_async),
    future=True,
    echo=False,
)
AsyncSessionFactory = async_sessionmaker(
    async_engine,
    autoflush=False,
    expire_on_commit=False,
)

# Создание синхронного подключения
sync_engine = create_engine(
    str(settings.manufactory_db_url_sync),
    future=True,
    echo=False,
)
SyncSessionFactory = sessionmaker(
    sync_engine,
    autoflush=False,
    expire_on_commit=False,
)


# Асинхронная зависимость для базы данных
async def get_async_db():
    """
    Асинхронная зависимость для работы с базой данных.
    :yield: Асинхронная сессия SQLAlchemy
    """
    async with AsyncSessionFactory() as session:
        yield session


# Синхронная зависимость для базы данных
def get_sync_db():
    """
    Синхронная зависимость для работы с базой данных.
    :yield: Синхронная сессия SQLAlchemy
    """
    with SyncSessionFactory() as session:
        yield session
