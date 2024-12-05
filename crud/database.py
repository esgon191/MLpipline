import asyncio, minio, logging, aiobotocore
from typing import Annotated
from aiobotocore.session import get_session
from sqlalchemy import String, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from contextlib import asynccontextmanager

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

# Синхронный клиент подключения к S3
minio_client = minio.Minio(
    f'{settings.MINIO_HOST}:{settings.MINIO_PORT}',
    access_key = settings.MINIO_NAME,
    secret_key = settings.MINIO_PASSWORD,
    secure=False
    )
# Логгер для ORM
orm_logger = LoggerFactory.create_logger("orm", "logs/orm.log", level=logging.DEBUG)

# Класс асинхронного клиента S3
class S3Client:
    def __init__(
            self, 
            access_key: str, 
            secret_key: str, 
            endpoint_url: str,
            bucket_name: str
    ):
        self.config = {
            "aws_access_key_id" : access_key,
            "aws_secret_access_key" : secret_key,
            "endpoint_url" : endpoint_url,
        }
        self.bucket_name =  bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(
            self, 
            object_binary,
            object_name: str,
            bucket_name: str = None
    ):
        if bucket_name is None:
            bucket_name = self.bucket_name

        async with self.get_client() as client:
            await client.put_object(
                Bucket=bucket_name,
                Key=object_name,
                Body=object_binary
            )

    async def get_object(
            self, 
            object_name,
            bucket_name=None
    ):
        if bucket_name is None:
            bucket_name = self.bucket_name

        async with self.get_client() as client:
            response = await client.get_object(
                Bucket=bucket_name,
                Key=object_name
            )

            return response


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