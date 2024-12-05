from queries.orm import AsyncORM
import asyncio, io, json
import numpy as np
from PIL import Image

from aiokafka import  AIOKafkaProducer

KAFKA_TOPICS_BOOTSTRAP_SERVERS = ['localhost:29092', 'localhost:29093', 'localhost:29094']
OUTPUT_TOPIC = "a_topic"


def image_to_json(image): 
    """
    Принимает на вход объект image, отдает json-строку
    """

    image_data = np.array(np.expand_dims(np.array(image), axis=0))
    #image_data = json.dumps(image_data.tolist())
    image_data = image_data.tolist()


    return image_data

async def main():
    await AsyncORM.create_tables()
    await AsyncORM.first_insert_photo(way_to_photo='../data/testdata/photo.jpg', way_to_metadata='../data/testdata/metadata.json')

    response, image = await AsyncORM.get_photo(bucket_name='bucket', object_name='1')
    json_image = image_to_json(image)

    output_data = {
        "image" : json_image
    }

    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_TOPICS_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        max_request_size=31457280
    )

    await producer.start()

    await producer.send_and_wait(OUTPUT_TOPIC, json_image)
    print('сообщение отправлено')

    await producer.stop()
    

asyncio.run(main())