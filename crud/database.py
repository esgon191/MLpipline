import aiobotocore.session
import asyncio, minio, logging, aiobotocore
from typing import Annotated

from sqlalchemy import String, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from logger import LoggerFactory
from config import settings

# Асинхронная сессия реляционной бд
async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
)

# Фабрика асинхронных клиентов реляционной бд
async_session_factory = async_sessionmaker(async_engine)

# Фабрика асинхронных клиентов S3
session = aiobotocore.session.get_session()


# Конфиг
config = aiobotocore.config.AioConfig(connect_timeout=5, read_timeout=15)
def create_minio_client():
    return session.create_client(
        's3',
        endpoint_url = f'http://{settings.MINIO_HOST}:{settings.MINIO_PORT}',
        aws_access_key_id = settings.MINIO_NAME,
        aws_secret_access_key = settings.MINIO_PASSWORD,
        config=config
    )

# Синхронный клиент подключения к S3
minio_client = minio.Minio(
    f'{settings.MINIO_HOST}:{settings.MINIO_PORT}',
    access_key = settings.MINIO_NAME,
    secret_key = settings.MINIO_PASSWORD,
    secure=False
    )
# Логгер для ORM
orm_logger = LoggerFactory.create_logger("orm", "logs/orm.log", level=logging.DEBUG)

str_256 = Annotated[str, 256]
class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)
    }

    repr_cols_num = 3
    repr_cols = tuple()
    
    def __repr__(self):
        """Relationships не используются в repr(), т.к. могут вести к неожиданным подгрузкам"""
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"