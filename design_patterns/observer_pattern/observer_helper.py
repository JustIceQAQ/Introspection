import abc

from code.design_patterns.observer_pattern.heater_helper import WatterHeater


class Observer(abc.ABC):
    """ 洗澡模式 與 飲用模式 父類別 """

    @abc.abstractmethod
    def update(self, observable, watter_heater):
        raise NotImplementedError


class WashingObserver(Observer):
    """洗澡模式"""

    def update(self, observable, obj):
        if isinstance(observable, WatterHeater):
            runtime_temperature = observable.get_temperature()
            if 50 <= runtime_temperature < 70:
                print(f"目前水溫{runtime_temperature}, 適合用於盥洗溫度")


class DrinkingObserver(Observer):
    """飲水模式"""

    def update(self, observable, obj):
        if isinstance(observable, WatterHeater):
            runtime_temperature = observable.get_temperature()
            if runtime_temperature >= 100:
                print(f"目前水溫{runtime_temperature}, 僅可用於飲用溫度")
