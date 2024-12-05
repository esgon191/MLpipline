from queries.orm import AsyncORM
import asyncio, io
from PIL import Image
# SyncORM.check_connection()

# asyncio.run(AsyncORM.create_tables())
# asyncio.run(AsyncORM.test_insert())

async def main():
    #await AsyncORM.create_tables()
    #print(await AsyncORM.first_insert_photo(way_to_photo='../data/testdata/photo.jpg', way_to_metadata='../data/testdata/metadata.json'))
    response, image = await AsyncORM.get_photo(bucket_name='bucket', object_name='1')
    print(response)
    image.show()

asyncio.run(main())