from database import async_engine, async_session_factory, minio_client, orm_logger, S3Client
from models import Base, Photo, RoadSign, Defect, DetectedDefect, DetectedSign
from config import settings
import json, aiofiles

class AsyncORM:
    default_bucket="bucket"

    s3client = S3Client(
        access_key=settings.MINIO_NAME,
        secret_key=settings.MINIO_PASSWORD,
        endpoint_url=f"http://{settings.MINIO_HOST}:{settings.MINIO_PORT}",
        bucket_name=default_bucket
    )

    @classmethod
    async def create_tables(cls, bucket : str = None):
        if bucket is None:
            bucket = cls.default_bucket

        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

            orm_logger.debug("PSQL tables created")

            if not minio_client.bucket_exists(bucket):
                orm_logger.info(f"MinIO {bucket} does not exist")
                minio_client.make_bucket(bucket)
                orm_logger.info(f"MinIO {bucket} created")

            else:
                orm_logger.debug(f"MinIO {bucket} exists")
            
            await conn.commit()

    @classmethod
    async def async_file_reader(cls, file_path):
        """
        Асинхронный чтец файлов из файловой системы
        """
        async with aiofiles.open(file_path, mode='rb') as file_data:
            data = await file_data.read()  
            orm_logger.debug(f"read {file_path}")
            
        return data

    @classmethod
    async def first_insert_photo(cls, way_to_photo : str, way_to_metadata : str, bucket : str = None) -> int:
        """
        Первое добавление поступившей фотографии в бд: 
            1) сохранение метаданных (json) в реляционной бд
            2) получение присвоенного первичного ключа
            3) сохранение самой фотографии в MinIO
            4) коммит

        Ремарки
            1) Пока нет фронта, загрузка метаданных будет происходить через файл
        """
        metadata = await cls.async_file_reader(way_to_metadata)
        metadata = json.loads(metadata)
        photo = Photo(is_processed=False, **metadata)

        photo_obj = await cls.async_file_reader(way_to_photo)

        if bucket is None:
            bucket = cls.default_bucket

        async with async_session_factory() as session:
            # Добавление метаданных в клиент реляционной бд
            session.add(photo) 
            await session.flush()
            # Получение присвоенного в реляционной бд первичного ключа
            photo_id = photo.id

            orm_logger.debug(f"photo {photo_id} added to session")

            # Добавление объекта фото в S3 
            await cls.s3client.upload_file(
                photo_obj,
                str(photo_id)
            )
            orm_logger.info(f"obj {photo_id} uploaded to {bucket}")
            
            # Коммит клиента реляционной бд после успешного 
            # сохранения изображения в S3
            await session.commit()
            orm_logger.info(f"photo {photo_id} commited to table")
            
        return 200

    @classmethod
    async def test_insert(cls):
        async with async_session_factory() as session:
            photo = Photo(
                latitude=1,
                longitude=1,
                is_processed=False
            )
            session.add(photo)
            await session.commit()

    @staticmethod
    async def process_photo():
        pass

    @classmethod
    async def get_photo(cls, object_name, bucket_name=None):
        response = await cls.s3client.get_object(
            object_name=object_name,
            bucket_name=bucket_name
        )
        return response
