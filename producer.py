import asyncio, json, time
from aiokafka import  AIOKafkaProducer
from config import *

# Kafka Топики
OUTPUT_TOPIC = "a_topic"

async def process_data():
    # Создание Kafka Producer для output_topic
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_TOPICS_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    await producer.start()

    

    await producer.send_and_wait(OUTPUT_TOPIC, output_data)
        #print(f"Результат отправлен в Kafka: {output_data['message']}")

    await producer.stop()

# Запуск обработки данных
asyncio.run(process_data())
