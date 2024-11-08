from queries.orm import SyncORM, AsyncORM
import asyncio
# SyncORM.check_connection()

asyncio.run(AsyncORM.create_tables())