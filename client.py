import asyncio
import httpx
from faker import Faker
from random import choice
import time

fake = Faker("ru_RU")  # Инициализация объекта для получения вспомогательных данных


async def send_message(client):
    URLs = [
        "http://localhost:1234/message",
        "http://localhost:4321/message",
    ]
    URL = choice(URLs)

    names = list([fake.first_name() for _ in range(10)])
    name = choice(names)

    text = fake.text()  # Генерация случайного текста
    payload = {
        "name": name,
        "text": text,
    }

    try:
        response = await client.post(URL, json=payload)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e}")
        return None
    except httpx.RequestError as e:
        print(f"Request error: {e}")
        return None


async def worker(client, num_requests):
    """Функция обработчик запросов"""
    for _ in range(num_requests):
        await send_message(client)


async def main():
    COROUTINES_QUANTITY = 50
    REQUESTS_PER_COROUTINE = 100
    total_requests = COROUTINES_QUANTITY * REQUESTS_PER_COROUTINE

    start_time = time.perf_counter()  # Запуск таймера

    async with httpx.AsyncClient() as client:

        tasks = [
            asyncio.create_task(worker(client, REQUESTS_PER_COROUTINE))
            for _ in range(COROUTINES_QUANTITY)
        ]
        await asyncio.gather(*tasks)

    end_time = time.perf_counter()  # Остановка таймера

    total_time = end_time - start_time  # Общее время работы
    single_request_time = total_time / total_requests  # Время работы одного запроса
    throughput_time = total_requests / total_time  # Общая пропускная способность

    print(f"Время за которое было выполнено {total_requests:.2f} запросов: {total_time} секунд")
    print(f"Время работы одного запроса: {single_request_time:.2f} секунд")
    print(f"Общая пропускная способность серверов: {throughput_time:.2f} запросов/секунду")


asyncio.run(main())
