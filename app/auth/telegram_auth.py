import os
from typing import Dict

from pyrogram import Client
from pyrogram.errors import SessionPasswordNeeded

from app.config import API_ID, API_HASH


# phone -> auth state
_pending_auth: Dict[str, dict] = {}


def _ensure_sessions_dir():
    os.makedirs("sessions", exist_ok=True)


async def send_code(phone: str, session_name: str) -> None:
    """
    Отправляет код подтверждения в Telegram и сохраняет phone_code_hash.
    """
    _ensure_sessions_dir()

    client = Client(
        name=session_name,
        api_id=API_ID,
        api_hash=API_HASH,
        workdir="sessions",
        in_memory=False,
    )

    await client.connect()

    sent = await client.send_code(phone)

    # сохраняем ВСЁ, что нужно для verify_code
    _pending_auth[phone] = {
        "client": client,
        "phone_code_hash": sent.phone_code_hash,
    }


async def verify_code(
    phone: str,
    code: str,
    password: str | None = None,
) -> None:
    """
    Подтверждает код и завершает авторизацию.
    """
    if phone not in _pending_auth:
        raise RuntimeError("No pending auth for this phone")

    state = _pending_auth[phone]
    client: Client = state["client"]
    phone_code_hash: str = state["phone_code_hash"]

    try:
        await client.sign_in(
            phone_number=phone,
            phone_code=code,
            phone_code_hash=phone_code_hash,
        )

    except SessionPasswordNeeded:
        if not password:
            raise RuntimeError("2FA password required")
        await client.check_password(password)

    finally:
        await client.disconnect()
        _pending_auth.pop(phone, None)
