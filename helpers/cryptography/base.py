import abc


class CipherBase(abc.ABC):
    @abc.abstractmethod
    def encrypter(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def decrypter(self, *args, **kwargs):
        raise NotImplementedError
