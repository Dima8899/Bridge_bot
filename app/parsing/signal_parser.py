import re

signal_patterns = [
    re.compile(r"#(\w+)\s+(Buy|Sell)", re.IGNORECASE),
    re.compile(r"\$(\w+)\s+(Long|Short)", re.IGNORECASE),
    re.compile(r"(\w+)/(\w+)\s+(Buy|Sell|Long|Short)", re.IGNORECASE),
]


def normalize_action(action_raw: str) -> str:
    if action_raw.lower() in ["long", "buy"]:
        return "buy"
    if action_raw.lower() in ["short", "sell"]:
        return "sell"
    raise ValueError(f"Unknown action: {action_raw}")


def normalize_ticker(*groups) -> str:
    return groups[0].upper()


def parse_signal(content: str):
    for pattern in signal_patterns:
        match = pattern.search(content)
        if match:
            *tickers, action = match.groups()
            return normalize_ticker(*tickers), normalize_action(action)
    return None
