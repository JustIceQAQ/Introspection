import asyncio

from design_patterns.observer.base import Observer


class MailObserver(Observer):
    def update(self, message: str):
        print(f"Mail Send: {message}")


class AsyncMailObserver(Observer):
    async def update(self, message: str):
        await asyncio.sleep(1)
        print(f"Async Mail Send: {message}")
