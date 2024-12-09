import asyncio, json, requests, aiohttp, time, io, base64
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from PIL import Image
from config import *
from utils.image_converter import image_to_json

# Kafka Топики
INPUT_TOPIC = "a_topic"


async def process_data(consumer_id: (str | None) = None, url: (str | None) = None, headers: (str | None) = None):
    if url is None:
        url = DEFAULT_URL
    if headers is None:
        headers = DEFAULT_HEADERS

    # Создание Kafka Consumer
    consumer = AIOKafkaConsumer(
        INPUT_TOPIC,
        bootstrap_servers=KAFKA_TOPICS_BOOTSTRAP_SERVERS,
        group_id="tensorflow_serving_group",
        group_instance_id=consumer_id,
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        auto_offset_reset='earliest',  # Начать чтение с самого начала, если нет смещений
        fetch_max_bytes=10000000 # 10мб
    )

    await consumer.start()

    message_counter = 0

    try:
        async for message in consumer:
            input_data = message.value
            message_counter += 1
            print(f"Получено сообщение {input_data['image_id']}")
            print(f"Всего получено сообщений {message_counter}")
            

            obj = base64.b64decode(input_data['image']) # Бинарник
            image = Image.open(io.BytesIO(obj)) # Изображение 
            image = image.convert('RGB') # Преобразование в 3 канала (на случай наличия альфа-канала)
            json_image = image_to_json(image) # json (список shape=(1, None, None, 3))

            data = {'instances' : json_image}

            # Открытие сессии
            async with aiohttp.ClientSession() as session:
                # Запрос 
                async with session.post(url=url, headers=headers, json=data) as response:
                    # Получение ответа
                    response_data = await response.text()
                    print(f"Статус: {response.status}")
                    #print(f"Тело: {response_data}")

    finally:
        await consumer.stop()

# Запуск обработки данных
if __name__ == "__main__":
    asyncio.run(process_data())
