
---

# 🧠 `docs/ARCHITECTURE.md`
**(как всё устроено технически)**

```md
# Архитектура HotBot

## Общая схема

Telegram Bot (aiogram)
        |
        v
User UI / Buttons
        |
        v
User State (USERS)
        |
        v
Runtime (1 per user)
        |
        v
Pyrogram Client (user session)
        |
        v
Telegram Channel
        |
        v
Signal Parser
        |
        v
Trading Executor (dry-run / real)

---

## Основные принципы

- Один пользователь = один Telegram аккаунт
- Один пользователь = один канал (на текущем этапе)
- Один пользователь = один runtime
- Pyrogram клиент живёт до нажатия "Stop"
- Нет глобальных listeners
- Нет shared state между пользователями

---

## Основные модули

### `app/bot/`
Telegram-бот (UI)

- `bot.py` — entrypoint бота
- `handlers/` — обработчики команд и кнопок
- `keyboards.py` — inline-кнопки
- `states.py` — FSM состояния
- `runtime.py` — управление жизненным циклом Pyrogram клиента

---

### `app/auth/`
Авторизация Telegram аккаунта пользователя

- `telegram_auth.py`
  - send_code()
  - verify_code()
  - создаёт `.session` файл

---

### `app/telegram/`
Работа с Pyrogram

- `client.py` — создание Pyrogram клиента
- `listener.py` — подписка на канал и обработка сообщений

---

### `app/parsing/`
Парсинг сигналов

- `signal_parser.py` — извлечение ticker / action из текста

---

### `app/trading/`
Трейдинг логика

- `executor.py` — выполнение сделки
- `sl_tp.py` — SL / TP
- Сейчас используется только dry-run

---

### `sessions/`
Хранилище Pyrogram session-файлов

---

## User State (runtime)

Сейчас хранится в памяти:

```python
USERS[user_id] = {
    "authorized": bool,
    "session_name": str,
    "channel_id": int | None,
    "dry_run": bool,
    "running": bool,
}
