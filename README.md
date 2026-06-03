# Historical Quiz Bot: Telegram & VK

## Обзор

Этот проект представляет собой ботов для мессенджеров Telegram и ВКонтакте, которые проводят викторину по историческим вопросам. Вопросы берутся из текстового файла (`quiz/1vs1200.txt`), содержащего блоки с вопросами и ответами. Боты используют Redis для хранения состояния пользователей (текущий вопрос и правильный ответ), поддерживают нормализацию ответов (удаление пояснений в скобках и после точки) и предоставляют удобную клавиатуру с кнопками «Новый вопрос» и «Сдаться».

## Ссылки на ботов

@quizhistorbot - Бот ТГ /n
[Бот ВК](https://vk.com/club239239733)

## Создание виртуального окружения
```
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Установка зависимостей

```
pip install -r requirements.txt
```

## Создайте .env
```
TG_TOKEN=8877835706:A...
VK_TOKEN=vk1.a.2uTdeH9NHvhMrhAo...
REDIS_HOST=ordinary-friends-flexib...
REDIS_PORT=198...
REDIS_PASSWORD=w1GQC...
```

## Запуск ботов локально

```
python bot_telegram.py
```

```
python bot_vk.py
```

