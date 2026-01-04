from pyrogram import filters
from pyrogram.errors import PeerIdInvalid

from app.parsing.signal_parser import parse_signal
from app.trading.executor import execute_trade


def register_listeners(app, user_context, binance_client):

    @app.on_message(filters.chat(user_context.channel_ids))
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

            await execute_trade(
                binance_client=binance_client,
                symbol=symbol,
                side="BUY" if action == "buy" else "SELL",
                settings=user_context.trading,
            )

        except PeerIdInvalid:
            # ⚠️ Известная проблема Pyrogram, безопасно игнорируем
            return

        except Exception as e:
            print(f"[LISTENER ERROR] {e}")
