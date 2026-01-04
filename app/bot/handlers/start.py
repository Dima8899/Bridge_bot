from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from app.bot.keyboards import main_menu

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "Привет 👋\n\n"
        "Я помогу подключить твой Telegram и настроить автотрейдинг.\n\n"
        "Начнём с подключения аккаунта.",
        reply_markup=main_menu(),
    )
