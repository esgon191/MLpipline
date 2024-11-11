from database import async_engine, async_session_factory, sync_engine, minio_client, orm_logger
from logger import LoggerFactory
from models import Base
from sqlalchemy import text

class SyncORM:
    @staticmethod
    def create_tables():
        sync_engine.echo = True
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)
        sync_engine.echo = True

    @staticmethod
    def check_connection():
        sync_engine.echo = True
        with sync_engine.connect() as connection:
            try:
                connection.execute(text("""
                        CREATE TABLE IF NOT EXISTS test_table (
                            id SERIAL PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        value INTEGER NOT NULL
                    )
                """))
                connection.commit()
                print("SUCCES")
            except Exception as e:
                print("FAIL")
                print(e)

class AsyncORM:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            await conn.commit()

        orm_logger.debug("PSQL tables created")
        bucket_name = "bucket"

        if not minio_client.bucket_exists(bucket_name):
            orm_logger.info(f"MinIO {bucket_name} does not exist")
            minio_client.make_bucket(bucket_name)
            orm_logger.info(f"MinIO {bucket_name} created")

        else:
            orm_logger.debug(f"MinIO {bucket_name} exists")

    @staticmethod
    async def process_photo():
        pass