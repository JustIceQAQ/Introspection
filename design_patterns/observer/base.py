import abc
import asyncio


class Observer(abc.ABC):
    # 監聽模組
    @abc.abstractmethod
    def update(self, message: str):
        pass


class Observable:
    # 使用 監聽模組 的框架
    def __init__(self):
        self.observers: list[Observer] = []

    def add_observer(self, observer: Observer):
        self.observers.append(observer)

    def remove_observer(self, observer: Observer):
        self.observers.remove(observer)

    def notify_observers(self, message: str):
        for observer in self.observers:
            observer.update(message)


class AsyncObserver(Observer):
    @abc.abstractmethod
    async def update(self, message: str):
        pass


class AsyncObservable:
    def __init__(self):
        self.observers: set[Observer] = set()

    def add_observer(self, observer: Observer):
        self.observers.add(observer)

    def remove_observer(self, observer: Observer):
        self.observers.remove(observer)

    async def notify_observers(self, message: str):
        await asyncio.gather(
            *[
                observer.update(message)
                for observer in self.observers
            ]
        )
