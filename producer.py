import asyncio
import json
import requests
from aiokafka import  AIOKafkaProducer

# Kafka Топики
OUTPUT_TOPIC = "a_topic"

async def process_data():
    # Создание Kafka Producer для output_topic
    producer = AIOKafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    await producer.start()

    # Публикуем результат обратно в Kafka в output_topic
    output_data = {
        "message" : "MESSAGE"
    }
    await producer.send_and_wait(OUTPUT_TOPIC, output_data)
    print(f"Результат отправлен в Kafka: {output_data}")

    await producer.stop()

# Запуск обработки данных
asyncio.run(process_data())
