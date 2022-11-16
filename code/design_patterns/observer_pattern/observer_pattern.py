

from code.design_patterns.observer_pattern.heater_helper import WatterHeater
from code.design_patterns.observer_pattern.observer_helper import WashingObserver, DrinkingObserver


def main():
    watter_heater = WatterHeater()
    washing_observer = WashingObserver()
    drinking_observer = DrinkingObserver()

    watter_heater.add_observer(washing_observer)
    watter_heater.add_observer(drinking_observer)

    watter_heater.set_temperature(40)
    watter_heater.set_temperature(60)
    watter_heater.set_temperature(120)


if __name__ == '__main__':
    main()
