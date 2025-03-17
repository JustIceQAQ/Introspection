class Observable:
    """"""

    def __init__(self):
        self._observer = []

    def add_observer(self, observer):
        self._observer.append(observer)

    def remove_observer(self, observer):
        self._observer.remove(observer)

    def notify_observer(self, obj=0):
        for o in self._observer:
            o.update(self, obj)


class WatterHeater(Observable):
    """熱水器"""

    def __init__(self):
        super().__init__()
        self._temperature = 25

    def get_temperature(self):
        return self._temperature

    def set_temperature(self, temperature):
        self._temperature = temperature
        print(f"溫度已設定為 {self._temperature}")
        self.notify_observer()
