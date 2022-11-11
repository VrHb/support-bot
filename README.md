# Бот помощник

Бот ведет диалог с пользователями с помощью [DialogFlow](https://developers.google.com/learn/pathways/chatbots-dialogflow)

## Как установить

Доступны два модуля реализации бота:

- Для VK
- Для telegram

Пример работы бота:  
![telegram bot gif](https://dvmn.org/media/filer_public/7a/08/7a087983-bddd-40a3-b927-a43fb0d2f906/demo_tg_bot.gif)

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

6. Токен бота для логов, получаем как в шаге № 1

```
echo "TG_LOGGER_TOKEN"=<токен бота>" >> .env
```

### Установка:

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
