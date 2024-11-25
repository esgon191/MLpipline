import asyncio
from aiokafka import AIOKafkaConsumer

async def consume():
    # Конфигурация консюмера
    consumer = AIOKafkaConsumer(
        'a_topic',  # Название топика
        bootstrap_servers='localhost:29092',  # Адрес bootstrap сервера
        group_id='test',  # Уникальный идентификатор группы консюмеров
        auto_offset_reset='earliest'  # Начать чтение с самого начала, если нет смещений
    )

    # Запуск консюмера
    await consumer.start()
    try:
        print(f'Консюмер подписан на топик "my_topic". Ожидание сообщений...')
        # Основной цикл получения сообщений
        async for msg in consumer:
            print(f"Получено сообщение: {msg.value.decode('utf-8')} от топика {msg.topic} [{msg.partition}] offset {msg.offset}")
    except KeyboardInterrupt:
        print('\nКонсюмер остановлен пользователем.')
    finally:
        # Закрываем консюмер для корректного завершения работы
        await consumer.stop()

# Запуск асинхронного консюмера
loop = asyncio.get_event_loop()
loop.run_until_complete(consume())