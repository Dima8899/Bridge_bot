from binance.client import Client as BinanceClient

from app.telegram.client import create_telegram_client
from app.telegram.listener import register_listeners
from app.models.user_context import UserContext, TradingSettings


def main():
    """
    Entry point for HotBot core (single-user MVP).
    """

    # =========================
    # USER CONTEXT (MVP)
    # =========================
    user = UserContext(
        user_id=1,
        telegram_session_name="user_1",   # имя session-файла
        channel_ids=[-1002328007504],     # ОДИН канал (пока)
        binance_api_key="PUT_KEY_HERE",
        binance_api_secret="PUT_SECRET_HERE",
        trading=TradingSettings(
            leverage=10,
            notional_usd=200.0,
            sl_percent=2.0,
            tp_percent=3.0,
            auto_close_minutes=1,
            dry_run=True,
        ),
    )

    tg_client = create_telegram_client(user.telegram_session_name)


    binance_client = BinanceClient(
        api_key=user.binance_api_key,
        api_secret=user.binance_api_secret,
    )


    register_listeners(
        app=tg_client,
        user_context=user,
        binance_client=binance_client,
    )


    print("[START] HotBot core started (DRY-RUN mode)")
    tg_client.run()


if __name__ == "__main__":
    main()
