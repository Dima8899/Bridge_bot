from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.bot.states import AuthStates
from app.bot.handlers.auth import USERS

router = Router()  # 🔴 ОБЯЗАТЕЛЬНО


@router.callback_query(F.data == "set_channel")
async def ask_channel(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "📡 Укажи канал одним из способов:\n\n"
        "1️⃣ Перешли любое сообщение из канала\n"
        "2️⃣ Или вставь ID канала (пример: -1001234567890)"
    )
    await state.set_state(AuthStates.waiting_for_channel)
    await callback.answer()


@router.message(AuthStates.waiting_for_channel)
async def receive_channel(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user = USERS.get(user_id)

    if not user or not user.get("authorized"):
        await message.answer("❌ Сначала подключи Telegram аккаунт")
        await state.clear()
        return

    channel_id = None

    # 1️⃣ Если переслано сообщение
    if message.forward_from_chat:
        channel_id = message.forward_from_chat.id

    # 2️⃣ Если введён ID вручную
    elif message.text and message.text.startswith("-100"):
        try:
            channel_id = int(message.text.strip())
        except ValueError:
            pass

    if not channel_id:
        await message.answer("❌ Не удалось определить канал. Попробуй ещё раз.")
        return

    user["channel_id"] = channel_id

    from app.storage.sqlite import save_user

    save_user(user_id, USERS[user_id])

    await message.answer(f"✅ Канал сохранён:\n`{channel_id}`")
    await state.clear()
