import asyncio, json, requests, aiohttp, time
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from config import *

# Kafka Топики
INPUT_TOPIC = "a_topic"

# Постоянная часть запроса к tensorflow 
url = "http://localhost:8501/v1/models/lighttestmodel:predict"
headers = {"Content-Type": "application/json"}


async def process_data():
    # Создание Kafka Consumer для input_topic
    consumer = AIOKafkaConsumer(
        INPUT_TOPIC,
        bootstrap_servers=KAFKA_TOPICS_BOOTSTRAP_SERVERS,
        group_id="tensorflow_serving_group",
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        max_poll_interval_ms=10000,
        auto_offset_reset='earliest',  # Начать чтение с самого начала, если нет смещений
        fetch_max_bytes=60000000
    )

    await consumer.start()

    message_counter = 0

    try:
        async for message in consumer:
            input_data = message.value

            message_counter += 1

            data = {"instances" : input_data['image']}

            # Открытие сессии
            async with aiohttp.ClientSession() as session:
                # Запрос 
                async with session.post(url=url, headers=headers, json=data) as response:
                    # Получение ответа
                    response_data = await response.text()
                    print(f"Статус: {response.status}")
                    print(f"Тело: {response_data}")

    finally:
        await consumer.stop()

# Запуск обработки данных
asyncio.run(process_data())
