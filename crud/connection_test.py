from sqlalchemy import create_engine

# Подключаемся к базе данных (в данном случае PostgreSQL)
DATABASE_URL = "postgresql://user:password@localhost:5432/db0" 
engine = create_engine(DATABASE_URL, echo=True)

# Проверка доступности базы данных
try:
    with engine.connect() as connection:
        print("Database is available.")
except Exception as e:
    print(f"Database is not available: {e}")

