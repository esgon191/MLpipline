import aiobotocore.config
import aiobotocore.session
from database import async_engine, async_session_factory, create_minio_client, minio_client, orm_logger
from models import Base, Photo, RoadSign, Defect, DetectedDefect, DetectedSign
import json, aiobotocore, aiofiles

class AsyncORM:
    default_bucket = 'bucket' 

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
    async def upload_to_minio(cls, bucket_name, object_name, data):
        # Создание клиента
        client = create_minio_client()
        orm_logger.debug("MinIO client created")

        async with client as client_obj:
            # Загружаем данные в MinIO
            orm_logger.debug("MinIO client context") 

            resp = await client_obj.put_object(
                Bucket=bucket_name, 
                Key=object_name, 
                Body=data
            )

            orm_logger.info(f"MinIO {resp}")

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

            photo_id = photo.id

            orm_logger.debug(f"photo {photo_id} added to session")

            # Добавление объекта фото в S3 
            await cls.upload_to_minio(
                bucket_name=bucket,
                object_name=str(photo_id), 
                data=photo_obj
            )

            orm_logger.info(f"obj {photo_id} uploaded to {bucket}")
            # Коммит клиента реляционной бд после успешного 
            # сохранения изображения в S3
            await session.commit()
            
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

