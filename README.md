<h2>DummyMessenger</h2>


<b>DummyMessenger</b> - проект по тестированию скорости асинхронной отправки сообщений на сервер.<br>

<div>:heavy_minus_sign:Сервер:heavy_minus_sign:<br>
Сервер получает сообщения от клиента, занося содержимое каждого (name & text) в базу данных.<br>
Ответ сервера представляет собой отформатированный JSON файл с последними 10 сообщениями от данного пользователя. (инициализация пользователей идёт по атрибуту name). 
</div><br>

<div>:heavy_minus_sign:Клиент:heavy_minus_sign:<br>
Клиент отправляет запросы асинхронно из 50 одновременно запущенных корутин.<br> 
Каждая корутина последовательно отправляет 100 запросов и завершает работу.
</div>
<div><br>
Итогом работы станет:
<ul>
    <li>Подсчёт затраченного времени на обработку 5000 запросов</li>
    <li>Вычисление времени работы одного запроса</li>
    <li>Определение общей пропускной способности сервера(-ов)</li>
</ul>
</div><br>
<hr>
<h3>Локальное развёртывание проекта на ОС Windows</h3>

<h5><i>Понадобятся два окна терминала</i></h5>
<div>
<h6>Первое окно терминала</h6>

```cmd
    git clone https://github.com/735Andrew/DummyMessenger 
    cd DummyMessenger
    python -m venv venv 
    venv\Scripts\activate
    (venv) pip install -r requirements.txt
    
    (venv) python server.py
```
</div><br>
<div>
<h6>Второе окно терминала</h6>

```cmd
    cd DummyMessenger 
    venv\Scripts\activate
    
    (venv) python client.py
```
</div>
<hr>
<h3>Полученные метрики</h3>

<h6><i>Характеристики сервера(-ов)</i></h6>
<div>

```cmd
    Время за которое было выполнено 5000 запросов: 62.15 секунд
    Время работы одного запроса: 0.01243049931526184 секунд
    Общая пропускная способность серверов: 80.45 запросов/секунду
```
</div><br>
<div>
<h6>Ответ сервера на запрос</h6>

```cmd
    (venv) C:\...\DummyMessenger>http localhost:1234/message name="Andrew" text="Goodbye!"
    HTTP/1.1 200 OK
    content-length: 121
    content-type: application/json
    date: Sun, 04 May 2025 12:41:17 GMT
    server: uvicorn

    [
        [
            "Andrew",
            "Goodbye!",
            "2025-05-04 12:41:18.581163+00:00",
            2,
            2
        ],
        [
            "Andrew",
            "Hello!",
            "2025-05-04 12:41:07.772966+00:00",
            1,
            1
        ]
    ]
```
</div>

