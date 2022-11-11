# Бот помощник

Бот ведет диалог с пользователями с помощью [DialogFlow](https://developers.google.com/learn/pathways/chatbots-dialogflow)

## Как установить

Доступны два модуля реализации бота:

- Для VK
- Для telegram

### Настройка переменных окружения:

- Для хранения переменных окружения создаем файл .env:

```
touch .env
```

1. Токен telegram бота, получаем после регистрации [бота](https://habr.com/ru/post/262247/)

```
echo "TG_TOKEN"=<токен бота>" >> .env
```

2. ID вашего чата, можно получить в коде с помощью `bot.get_updates()[0].message.chat_id`

```
echo "GG_DF_SESSION_ID"=<ID телеграм чата>" >> .env
```

3. ID проекта в google cloud, создаем проект и получаем ID по [инструкции](https://cloud.google.com/dialogflow/es/docs/quick/setup)

```
echo "GG_DF_ID"=<ID вашего проекта>" >> .env
```

4. Переменная окружения с путем к json файлу настроек аутентификации, смотрим инструкцию [тут](https://cloud.google.com/docs/authentication/client-libraries)

```
echo "GOOGLE_APPLICATION_CREDENTIALS"=<ID вашего проекта>" >> .env
```

5. Ключ доступа к API VK, как получить читаем [тут](https://cloud.google.com/docs/authentication/client-libraries)

```
echo "VK_API_KEY"=<ключ API VK>" >> .env
```

### Установка с помощью docker:

1. Скачать образ python:

```bash
docker pull python:3.10
```

2. Упаковать контейнер:

```bash
docker build -t bot-helper .
```

3. Запустить контейнер:

```bash
docker run -d -t bot-helper
```

4. Проверить что контейнер запустился:

```bash
docker ps
```

### Установка обычным путем:

- Необходимо установить интерпретатор python версии 3.10
- Cкопировать содержимое проекта к себе в рабочую директорию
- Активировать внутри рабочей директории виртуальное окружение:

```
python -m venv [название окружения]
```

- Установить зависимости(необходимые библиотеки):

```
pip install -r requirements.txt
```

### Как пользоваться:

- Запускаем vk бота:

```
python vk_bot.py
```

- Запускаем telegram бота:

```
python tg_bot.py
```
