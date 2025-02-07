import abc


class CipherBase(abc.ABC):
    _encoding = "utf-8"

    class ReturnType:
        Str = "Str"
        Bytes = "Bytes"

    @abc.abstractmethod
    def encrypter(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def decrypter(self, *args, **kwargs):
        raise NotImplementedError
