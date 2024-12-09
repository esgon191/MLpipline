from queries.orm import AsyncORM
import asyncio, io, json
import numpy as np
from PIL import Image

from aiokafka import  AIOKafkaProducer

KAFKA_TOPICS_BOOTSTRAP_SERVERS = ['localhost:29092', 'localhost:29093', 'localhost:29094']
OUTPUT_TOPIC = "a_topic"

test_photos = [f'street_{i}.png' for i in range(1, 11)]

async def main():
    await AsyncORM.create_tables()
    for photo_name in test_photos:
        await AsyncORM.first_insert_photo(way_to_photo=f"../data/testdata/streets/{photo_name}", way_to_metadata='../data/testdata/streets/metadata.json')

    
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_TOPICS_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        #max_request_size=60000000
    )

    await producer.start()

    for i in range(1, len(test_photos)+1):
        response, obj = await AsyncORM.get_photo(bucket_name='bucket', object_name=str(i))
        #json_image = image_to_json(image)

        output_data = {
            "image" : obj
        }

        await producer.send_and_wait(OUTPUT_TOPIC, output_data)
        print('сообщение отправлено')

    await producer.stop()
    

asyncio.run(main())