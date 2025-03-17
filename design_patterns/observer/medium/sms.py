import asyncio

from design_patterns.observer.base import Observer


class SMSObserver(Observer):
    def update(self, message: str):
        print(f"SMS Send: {message}")


class AsyncSMSObserver(Observer):
    async def update(self, message: str):
        await asyncio.sleep(1)
        print(f"Async SMS Send: {message}")
