import asyncio

from design_patterns.observer.base import Observable, Observer, AsyncObservable
from design_patterns.observer.medium.mail import MailObserver, AsyncMailObserver
from design_patterns.observer.medium.sms import SMSObserver, AsyncSMSObserver


class MessageObservable(Observable):
    def __init__(self, account: str):
        super().__init__()
        self.account = account

    def get_observer_list(self) -> list[Observer]:
        return self.observers

    def notify(self, message: str):
        print(f"正在通知{self.account} 訊息: {message}")
        self.notify_observers(message)


class AsyncMessageObservable(AsyncObservable):
    def __init__(self, account: str):
        super().__init__()
        self.account = account

    def get_observer_list(self) -> list[Observer]:
        return self.observers

    async def notify(self, message: str):
        print(f"正在通知{self.account} 訊息: {message}")
        await self.notify_observers(message)


def main():
    message_observable = MessageObservable(account="QAQ")
    message_observable.add_observer(MailObserver())
    message_observable.add_observer(SMSObserver())
    message_observable.notify("HI HI")

async def async_main():
    message_observable = AsyncMessageObservable(account="QAQ")
    message_observable.add_observer(AsyncMailObserver())
    message_observable.add_observer(AsyncSMSObserver())
    await message_observable.notify("HI HI")


if __name__ == "__main__":
    asyncio.run(async_main())
