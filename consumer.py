import asyncio
import json
import requests
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import time 

# Kafka Топики
INPUT_TOPIC = "a_topic"

async def process_data():
    # Создание Kafka Consumer для input_topic
    consumer = AIOKafkaConsumer(
        INPUT_TOPIC,
        bootstrap_servers='localhost:9092',
        group_id="tensorflow_serving_group",
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    await consumer.start()

    try:
        async for message in consumer:
            input_data = message.value
            for i in range(5):
                print(i+1)
                time.sleep(1)

            print(f"Получены данные из Kafka: {input_data}")


    finally:
        await consumer.stop()

# Запуск обработки данных
asyncio.run(process_data())
