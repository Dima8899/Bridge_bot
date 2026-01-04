from dataclasses import dataclass
from typing import List


@dataclass
class TradingSettings:
    leverage: int
    notional_usd: float
    sl_percent: float
    tp_percent: float
    auto_close_minutes: int | None
    dry_run: bool


@dataclass
class UserContext:
    user_id: int
    telegram_session_name: str
    channel_ids: List[int]
    binance_api_key: str
    binance_api_secret: str
    trading: TradingSettings
