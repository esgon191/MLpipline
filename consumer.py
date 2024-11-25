import asyncio
import json
import requests
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import time 
from config import *

# Kafka Топики
INPUT_TOPIC = "a_topic"

async def process_data():
    # Создание Kafka Consumer для input_topic
    consumer = AIOKafkaConsumer(
        INPUT_TOPIC,
        bootstrap_servers=KAFKA_TOPICS_BOOTSTRAP_SERVERS,
        group_id="tensorflow_serving_group",
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        max_poll_interval_ms=10000,
        auto_offset_reset='earliest'  # Начать чтение с самого начала, если нет смещений
    )

    await consumer.start()

    message_counter = 0

    try:
        async for message in consumer:
            input_data = message.value

            message_counter += 1

            print(f"Получены данные из Kafka: {input_data['message']}")
            print(f'Всего получено сообщений {message_counter}')


    finally:
        await consumer.stop()

# Запуск обработки данных
asyncio.run(process_data())
