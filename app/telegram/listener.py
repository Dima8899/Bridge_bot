from pyrogram import filters
from pyrogram.errors import PeerIdInvalid

from app.parsing.signal_parser import parse_signal
from app.trading.executor import execute_trade


def register_listeners(app, channel_id: int, user_settings: dict, binance_client):

    @app.on_message(filters.chat(channel_id))
    async def handle_message(_, message):
        try:
            content = message.text or message.caption
            if not content:
                return

            parsed = parse_signal(content)
            if not parsed:
                return

            ticker, action = parsed
            symbol = f"{ticker}USDT"

            # 🧪 DRY-RUN
            if user_settings.get("dry_run", True):
                print(f"[DRY-RUN] {action.upper()} {symbol}")
                return

            await execute_trade(
                binance_client=binance_client,
                symbol=symbol,
                side="BUY" if action == "buy" else "SELL",
                settings=user_settings["trading"],
            )

        except PeerIdInvalid:
            return
        except Exception as e:
            print(f"[LISTENER ERROR] {e}")
