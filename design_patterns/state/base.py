import abc


class Stats(abc.ABC):
    @abc.abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError()
