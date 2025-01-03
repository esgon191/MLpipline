class Settings:
    DB_HOST = "localhost"
    DB_PORT = 5432
    DB_USER = "user" 
    DB_PASS = "password"
    DB_NAME = "db0"
    
    MINIO_HOST = "127.0.0.1"
    MINIO_PORT = 9000 
    MINIO_NAME = "user"
    MINIO_PASSWORD = "password"

    @property
    def DATABASE_URL_asyncpg(self):
        # postgresql+asyncpg://postgres:postgres@localhost:5432/sa
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_psycopg(self):
        # DSN
        # postgresql+psycopg://postgres:postgres@localhost:5432/sa
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    

settings = Settings()