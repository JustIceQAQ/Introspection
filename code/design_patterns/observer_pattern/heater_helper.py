class WatterHeater:
    """熱水器"""

    def __init__(self):
        self._observer = []
        self._temperature = 25

    def get_temperature(self):
        return self._temperature

    def set_temperature(self, temperature):
        self._temperature = temperature
        print(f"溫度已設定為 {self._temperature}")
        self.notifies()

    def add_observer(self, observer):
        self._observer.append(observer)

    def notifies(self):
        for o in self._observer:
            o.update(self)
