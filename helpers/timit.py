import time


class Timit:
    def __init__(self, name: str | None = None) -> None:
        self.name = name

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.time()
        self.duration = self.end - self.start
        print(f"{self.name or ""}: {self.duration}")
