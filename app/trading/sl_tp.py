import asyncio
from binance.exceptions import BinanceAPIException


async def set_stop_loss_and_take_profit(
    binance_client,
    symbol: str,
    side: str,
    entry_price: float,
    sl_percent: float,
    tp_percent: float,
):
    """
    Устанавливает Stop Loss и Take Profit ордера.
    """

    try:
        if side == "BUY":
            sl_price = entry_price * (1 - sl_percent / 100)
            tp_price = entry_price * (1 + tp_percent / 100)
            opposite_side = "SELL"
        else:
            sl_price = entry_price * (1 + sl_percent / 100)
            tp_price = entry_price * (1 - tp_percent / 100)
            opposite_side = "BUY"

        sl_price = round(sl_price, 2)
        tp_price = round(tp_price, 2)

        # Stop Loss
        await asyncio.to_thread(
            binance_client.futures_create_order,
            symbol=symbol,
            side=opposite_side,
            type="STOP_MARKET",
            stopPrice=sl_price,
            closePosition=True,
        )

        # Take Profit
        await asyncio.to_thread(
            binance_client.futures_create_order,
            symbol=symbol,
            side=opposite_side,
            type="TAKE_PROFIT_MARKET",
            stopPrice=tp_price,
            closePosition=True,
        )

        print(f"[SL/TP] {symbol} SL={sl_price}, TP={tp_price}")

    except BinanceAPIException as e:
        print(f"[SL/TP ERROR] Binance API: {e.message}")

    except Exception as e:
        print(f"[SL/TP ERROR] {e}")
