import os
from pyrogram import Client
from app.config import API_ID, API_HASH


def create_telegram_client(session_name: str) -> Client:
    os.makedirs("sessions", exist_ok=True)

    return Client(
        name=session_name,
        api_id=API_ID,
        api_hash=API_HASH,
        workdir="sessions",
        in_memory=False,
    )
