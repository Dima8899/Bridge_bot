import asyncio
from binance.client import Client as BinanceClient
from app.trading.sl_tp import set_stop_loss_and_take_profit


async def execute_trade(
    binance_client: BinanceClient,
    symbol: str,
    side: str,
    settings,
):
    """
    Открывает сделку или выполняет dry-run.
    """

    # =========================
    # DRY-RUN MODE (ВАЖНО)
    # =========================
    if settings.dry_run:
        print(
            f"[DRY-RUN] {side} {symbol} | "
            f"notional={settings.notional_usd}, "
            f"leverage={settings.leverage}, "
            f"SL={settings.sl_percent}, "
            f"TP={settings.tp_percent}, "
            f"auto_close={settings.auto_close_minutes}"
        )
        return

    # =========================
    # REAL TRADING MODE
    # =========================

    # Устанавливаем плечо
    await asyncio.to_thread(
        binance_client.futures_change_leverage,
        symbol=symbol,
        leverage=settings.leverage,
    )

    # Получаем текущую цену
    ticker = await asyncio.to_thread(
        binance_client.futures_symbol_ticker,
        symbol=symbol,
    )
    price = float(ticker["price"])

    # Рассчитываем количество
    quantity = settings.notional_usd / price

    # Открываем сделку
    await asyncio.to_thread(
        binance_client.futures_create_order,
        symbol=symbol,
        side=side,
        type="MARKET",
        quantity=quantity,
    )

    print(f"[TRADE] Opened {side} {symbol} qty={quantity}")

    # Устанавливаем SL / TP
    if settings.sl_percent and settings.tp_percent:
        await set_stop_loss_and_take_profit(
            binance_client,
            symbol,
            side,
            price,
            settings.sl_percent,
            settings.tp_percent,
        )

    # Автозакрытие сделки
    if settings.auto_close_minutes:
        asyncio.create_task(
            auto_close(
                binance_client,
                symbol,
                side,
                settings.auto_close_minutes,
            )
        )


async def auto_close(
    binance_client: BinanceClient,
    symbol: str,
    side: str,
    minutes: int,
):
    """
    Закрывает сделку через N минут.
    """
    await asyncio.sleep(minutes * 60)

    opposite_side = "SELL" if side == "BUY" else "BUY"

    await asyncio.to_thread(
        binance_client.futures_create_order,
        symbol=symbol,
        side=opposite_side,
        type="MARKET",
        quantity=1,  # TODO: заменить на реальное количество позиции
    )

    print(f"[AUTO-CLOSE] Closed {symbol} after {minutes} minutes")
