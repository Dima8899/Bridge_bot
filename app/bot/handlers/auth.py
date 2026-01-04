from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from app.bot.states import AuthStates
from app.auth.telegram_auth import send_code, verify_code

router = Router()

# временное хранилище пользователей
USERS = {}


@router.callback_query(F.data == "connect_tg")
async def connect_tg(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "📱 Введите номер телефона в формате:\n"
        "+380631234567"
    )
    await state.set_state(AuthStates.waiting_for_phone)
    await callback.answer()


@router.message(AuthStates.waiting_for_phone)
async def phone_input(message: Message, state: FSMContext):
    phone = message.text.strip()
    user_id = message.from_user.id
    session_name = f"user_{user_id}"

    await send_code(phone=phone, session_name=session_name)

    USERS[user_id] = {
        "phone": phone,
        "session_name": session_name,
        "authorized": False,
    }

    await message.answer("📩 Код отправлен. Введите код из Telegram:")
    await state.set_state(AuthStates.waiting_for_code)


@router.message(AuthStates.waiting_for_code)
async def code_input(message: Message, state: FSMContext):
    code = message.text.strip()
    user_id = message.from_user.id

    user = USERS.get(user_id)
    if not user:
        await message.answer("❌ Ошибка. Начните заново /start")
        await state.clear()
        return

    await verify_code(phone=user["phone"], code=code)

    user["authorized"] = True

    await message.answer("✅ Telegram успешно подключён!")
    await state.clear()
