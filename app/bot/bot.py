import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.bot.handlers import start, auth

load_dotenv()


async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(auth.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
