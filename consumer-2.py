import asyncio
from config import *
from consumer import process_data

# Kafka Топики
INPUT_TOPIC = "a_topic"

# Постоянная часть запроса к tensorflow 
url = "http://localhost:8503/v1/models/lighttestmodel:predict"
headers = {"Content-Type": "application/json"}

asyncio.run(process_data(url=url))