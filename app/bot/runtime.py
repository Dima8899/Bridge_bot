import asyncio
from dataclasses import dataclass
from typing import Optional

from pyrogram import Client


@dataclass
class UserRuntime:
    client: Client
    stop_event: asyncio.Event
    task: Optional[asyncio.Task] = None

    async def run(self) -> None:
        """
        Запускает Pyrogram client и держит его живым, пока не придёт stop_event.
        Всегда корректно останавливает client.
        """
        try:
            await self.client.start()
            # держим runtime живым
            await self.stop_event.wait()
        finally:
            # гарантируем корректную остановку
            try:
                await self.client.stop()
            except Exception as e:
                print(f"[RUNTIME STOP ERROR] {e}")

    async def stop(self) -> None:
        """
        Сигнализирует остановку и ждёт завершения task.
        """
        self.stop_event.set()
        if self.task and not self.task.done():
            try:
                await self.task
            except asyncio.CancelledError:
                pass
            except Exception as e:
                print(f"[RUNTIME TASK ERROR] {e}")
