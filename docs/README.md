# HotBot — Telegram → Trading Bridge

HotBot — сервис для автоматического трейдинга по сигналам из Telegram-каналов.

## Ключевая идея
Каждый пользователь:
- подключает СВОЙ Telegram-аккаунт
- выбирает ОДИН канал
- настраивает автотрейдинг
- бот читает канал от имени пользователя и исполняет сигналы

❗ Боты Telegram не используются для чтения каналов.
Используется Pyrogram (user sessions).

---

## Текущий статус проекта (Stage: MVP Core)

✅ Telegram Bot (UI, aiogram 3.x)  
✅ Авторизация Telegram аккаунта пользователя (send_code / verify_code)  
✅ Pyrogram user sessions (.session файлы)  
✅ Подключение закрытых Telegram-каналов  
✅ Парсинг торговых сигналов  
✅ Runtime Start / Stop без гонок  
✅ Dry-run режим (без реальных сделок)  

❌ Persist storage (БД) — В ПРОЦЕССЕ  
❌ Реальная торговля Binance — В ПРОЦЕССЕ  
❌ Подписки / лимиты — ПЛАНИРУЕТСЯ  

---

Где хранятся сессии Telegram?
/sessions/*.session
Файлы сохраняются автоматически Pyrogram
и позволяют не вводить код повторно.

## Как запускать проект

```bash
python -m app.bot.bot
