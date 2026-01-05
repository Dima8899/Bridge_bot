import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.bot.handlers.auth import USERS
from app.bot.keyboards import main_menu
from app.bot.runtime import UserRuntime

from app.telegram.client import create_client
from app.telegram.listener import register_listeners

# TODO: binance_client пока один общий/заглушка — позже сделаем на пользователя
#from binance.client import Client as BinanceClient
#from app.config import BINANCE_API_KEY, BINANCE_API_SECRET


router = Router()

# user_id -> runtime
RUNTIMES: dict[int, UserRuntime] = {}


#def _get_binance_client():
    #return BinanceClient(api_key=BINANCE_API_KEY, api_secret=BINANCE_API_SECRET)


@router.callback_query(F.data == "toggle_dry_run")
async def toggle_dry_run(callback: CallbackQuery):
    user = USERS.get(callback.from_user.id)
    if not user:
        await callback.answer("Сначала /start")
        return

    user["dry_run"] = not user.get("dry_run", True)

    await callback.message.edit_reply_markup(
        reply_markup=main_menu(dry_run=user["dry_run"])
    )
    await callback.answer("Dry-run переключён")


@router.callback_query(F.data == "start_core")
async def start_core(callback: CallbackQuery):
    user_id = callback.from_user.id
    user = USERS.get(user_id)

    if not user or not user.get("authorized"):
        await callback.answer("❌ Сначала подключи Telegram", show_alert=True)
        return

    if not user.get("channel_id"):
        await callback.answer("❌ Сначала укажи канал", show_alert=True)
        return

    # не создаём второй runtime
    if user_id in RUNTIMES and RUNTIMES[user_id].task and not RUNTIMES[user_id].task.done():
        await callback.answer("⚠️ Уже запущено")
        return

    # дефолтные настройки трейдинга (пока)
    user.setdefault("dry_run", True)
    user.setdefault("trading", {
        "leverage": 10,
        "notional_usd": 200.0,
        "sl_percent": 2.0,
        "tp_percent": 3.0,
        "auto_close_minutes": 1,
        "dry_run": user.get("dry_run", True),
    })
    # синхронизируем dry_run в trading
    user["trading"]["dry_run"] = user.get("dry_run", True)

    tg_client = create_client(session_name=user["session_name"])
    binance_client = None
    register_listeners(
        app=tg_client,
        channel_id=user["channel_id"],
        user_settings=user,      # тут лежит dry_run и trading
        binance_client=None,
    )

    runtime = UserRuntime(client=tg_client, stop_event=asyncio.Event())
    task = asyncio.create_task(runtime.run())

    runtime.task = task
    RUNTIMES[user_id] = runtime

    user["running"] = True

    await callback.answer("▶️ Core запущен")


@router.callback_query(F.data == "stop_core")
async def stop_core(callback: CallbackQuery):
    user_id = callback.from_user.id
    user = USERS.get(user_id)

    runtime = RUNTIMES.get(user_id)
    if not runtime:
        await callback.answer("ℹ️ Не запущено")
        return

    # корректная остановка
    await runtime.stop()

    # чистим runtime
    RUNTIMES.pop(user_id, None)
    if user:
        user["running"] = False

    await callback.answer("⏹ Core остановлен")
