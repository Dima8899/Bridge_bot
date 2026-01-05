from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu(dry_run: bool = True):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔗 Подключить Telegram", callback_data="connect_tg")],
            [InlineKeyboardButton(text="📡 Указать канал", callback_data="set_channel")],
            [InlineKeyboardButton(text=f"🧪 Dry-run: {'ON' if dry_run else 'OFF'}", callback_data="toggle_dry_run")],
            [
                InlineKeyboardButton(text="▶️ Старт", callback_data="start_core"),
                InlineKeyboardButton(text="⏹ Стоп", callback_data="stop_core"),
            ],
        ]
    )
