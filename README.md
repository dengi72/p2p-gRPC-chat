# p2p-gRPC-chat
### Установка
Помимо зависимостей, указанных в `requiremnets.txt`, которые можно установить с помощью:
```
pip3 install -r requirements.txt
```
понадобится библиотека `python3-tk`, которую можно установить с помощью менеджера пакетов.
Затем необходимо сгенерировать код из proto-схемы:
```
./generate.sh
```

### Запуск
В режиме клиента:
```
python3 src/main.py --type=client
```

В режиме сервера:
```
python3 src/main.py --type=server [--address=*IPv4 address* --port=*port number*]
```

### Архитектура
- main -- точка входа приложения: разбор аргументов командной строки, выбор, в каком режиме (клиент/сервер) запуститься.
- server -- класс-заглушка, созданный для общения с выбранным фреймворком по его интерфейсу.
- client -- интерфейс пользователя, реализованный через библиотеку tkinter.
- chat_pb2_grpc -- основная логика сервера.
- chat_pb2 -- proto-сообщение, сгенерированное из chat.proto.