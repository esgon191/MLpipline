from queries.orm import AsyncORM
import asyncio
# SyncORM.check_connection()

# asyncio.run(AsyncORM.create_tables())
# asyncio.run(AsyncORM.test_insert())

async def main():
    await AsyncORM.create_tables()
    print(await AsyncORM.first_insert_photo(way_to_photo='../data/testdata/photo.jpg', way_to_metadata='../data/testdata/metadata.json'))

asyncio.run(main())