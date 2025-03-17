from design_patterns.state.base import Stats, StatsV2


class SolidState(Stats):
    def get_name(self) -> str:
        return "Solid State"


class LinearState(Stats):
    def get_name(self) -> str:
        return "Linear State"


class GasState(Stats):
    def get_name(self) -> str:
        return "Gas State"


class SupercriticalFluidState(Stats):
    # 超臨界流體
    def get_name(self) -> str:
        return "Supercritical Fluid State"


def singleton(cls, *args, **kwargs):
    instances = {}

    def _singleton(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
            return instances[cls]
        return instances[cls]

    return _singleton


@singleton
class SolidStateV2(StatsV2):
    def __init__(self, name: str):
        super().__init__(name)

    def is_match(self, state_info: int) -> bool:
        return state_info < 0


@singleton
class LinearStateV2(StatsV2):
    def __init__(self, name: str):
        super().__init__(name)

    def is_match(self, state_info: int) -> bool:
        return 0 < state_info <= 100


@singleton
class GasStateV2(StatsV2):
    def __init__(self, name: str):
        super().__init__(name)

    def is_match(self, state_info: int) -> bool:
        return 373 >= state_info > 100


@singleton
class SupercriticalFluidStateV2(StatsV2):
    def __init__(self, name: str):
        super().__init__(name)

    def is_match(self, state_info: int) -> bool:
        return state_info > 373
