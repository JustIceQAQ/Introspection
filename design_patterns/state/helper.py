from design_patterns.state.base import Stats, Contest
from design_patterns.state.water.stste import (
    SolidState, LinearState, GasState, SupercriticalFluidState,
    SolidStateV2, LinearStateV2, GasStateV2, SupercriticalFluidStateV2
)


class Water:
    def __init__(self, state: Stats | None = None):
        self._atmospheric = 1
        self._temperature = 25
        self._state: Stats = state or LinearState()

    def get_temperature(self):
        return self._temperature

    def get_atmospheric(self):
        return self._atmospheric

    def get_environment(self) -> tuple[int, int]:
        return self._temperature, self._atmospheric

    def set_temperature(self, temperature: int):
        self._temperature = temperature

    def set_atmospheric(self, atmospheric: int):
        self._atmospheric = atmospheric

    def _change_state(self, state: Stats):
        print(f"{self._state.get_name()} -> {state.get_name()}")
        self._state = state

    def change_environment(self, temperature: int, atmospheric: int | None = 1):
        self.set_temperature(temperature)
        self.set_atmospheric(atmospheric)
        if self._temperature > 374 and self._atmospheric > 22:
            self._change_state(SupercriticalFluidState())
            return

        if self._temperature <= 0:
            self._change_state(SolidState())
        elif 1 <= self._temperature <= 100:
            self._change_state(LinearState())
        elif self._temperature > 100:
            self._change_state(GasState())


class WaterV2(Contest):
    def __init__(self, ):
        super().__init__(state_info=25, cur_state=LinearStateV2("液態"))
        self.add_state(SolidStateV2("固態"))
        self.add_state(LinearStateV2("液態"))
        self.add_state(GasStateV2("氣態"))
        self.add_state(SupercriticalFluidStateV2("超臨界流體"))

    def change_environment(self, temperature: int, atmospheric: int | None = 1):
        self.set_state_info(temperature)

def main_1():
    water = Water()
    print(water.get_environment())

    water.change_environment(-20)
    water.change_environment(50)
    water.change_environment(150)
    water.change_environment(400, 30)

def main_2():
    water = WaterV2()
    water.change_environment(-30)
    water.change_environment(60)
    water.change_environment(101)
    water.change_environment(400)

if __name__ == "__main__":
    main_2()
