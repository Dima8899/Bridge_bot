import sqlite3
from typing import Dict, Any

DB_PATH = "hotbot.db"


def get_conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                telegram_user_id INTEGER PRIMARY KEY,
                session_name TEXT NOT NULL,
                authorized INTEGER NOT NULL,
                channel_id INTEGER,
                dry_run INTEGER NOT NULL
            )
            """
        )
        conn.commit()


def load_users() -> Dict[int, Dict[str, Any]]:
    users = {}

    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT
                telegram_user_id,
                session_name,
                authorized,
                channel_id,
                dry_run
            FROM users
            """
        ).fetchall()

    for row in rows:
        (
            telegram_user_id,
            session_name,
            authorized,
            channel_id,
            dry_run,
        ) = row

        users[telegram_user_id] = {
            "session_name": session_name,
            "authorized": bool(authorized),
            "channel_id": channel_id,
            "dry_run": bool(dry_run),
            "running": False,  # runtime всегда false после рестарта
        }

    return users


def save_user(user_id: int, user: Dict[str, Any]):
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO users (
                telegram_user_id,
                session_name,
                authorized,
                channel_id,
                dry_run
            )
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(telegram_user_id)
            DO UPDATE SET
                session_name = excluded.session_name,
                authorized   = excluded.authorized,
                channel_id   = excluded.channel_id,
                dry_run      = excluded.dry_run
            """,
            (
                user_id,
                user.get("session_name"),
                int(user.get("authorized", False)),
                user.get("channel_id"),
                int(user.get("dry_run", True)),
            ),
        )
        conn.commit()
