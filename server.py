from fastapi import FastAPI, Body
import uvicorn
import asyncio
import sqlite3
from datetime import datetime, timezone
import os

# Переменные настройки базы данных
basedir = os.path.abspath(os.path.dirname(__file__))
db_name = os.path.join(basedir, "messages.db")

connection = sqlite3.connect(db_name)
cursor = connection.cursor()


def init_db():
    with sqlite3.connect(db_name) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS Messages
            (
            MessageID INTEGER PRIMARY KEY,
            AuthorName TEXT NOT NULL,
            Text TEXT NOT NULL,
            Datetime TEXT NOT NULL,
            AuthorMessagesCounter INTEGER
            )
            """
        )


app = FastAPI()


@app.post("/message")
async def message(
    name: str = Body(embed=True),
    text: str = Body(embed=True),
):
    request_time = datetime.now(timezone.utc)  # Время получения запроса

    # Вычисление количества имеющихся у пользователя сообщений
    query1 = """SELECT COUNT(*) FROM Messages WHERE AuthorName=:AuthorName"""
    params1 = {"AuthorName": name}
    cursor.execute(query1, params1)
    messages_quantity = cursor.fetchone()[0]  # Из функции возвращается кортеж

    # Внесение нового сообщения в базу данных
    query2 = """INSERT INTO Messages (AuthorName, Text, Datetime, AuthorMessagesCounter)
            VALUES (?,?,?,?)"""
    params2 = (name, text, request_time, messages_quantity + 1)
    cursor.execute(query2, params2)
    connection.commit()

    # Возврат 10 последних сообщений пользователя, отсортированных по времени
    query3 = """
            SELECT AuthorName, Text, Datetime, MessageID, AuthorMessagesCounter
            FROM Messages 
            WHERE AuthorName=?
            ORDER BY Datetime DESC
            LIMIT 10 
    """
    cursor.execute(query3, (name,))
    total = cursor.fetchall()
    return total


async def run_server(port: int):
    """Функция запуска сервера"""
    config = uvicorn.Config(app, port=port)
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    init_db()
    task1 = asyncio.create_task(run_server(port=1234))
    task2 = asyncio.create_task(run_server(port=4321))

    try:
        await asyncio.gather(task1, task2)
    except asyncio.exceptions.CancelledError as e:
        print(f"Exception: {e}")


asyncio.run(main())
