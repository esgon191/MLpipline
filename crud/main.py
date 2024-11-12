from queries.orm import AsyncORM
import asyncio
# SyncORM.check_connection()

asyncio.run(AsyncORM.create_tables())
print(asyncio.run(AsyncORM.first_insert_photo(
    way_to_photo='../data/testdata/photo.jpg',
    way_to_metadata='../data/testdata/metadata.json'
)))