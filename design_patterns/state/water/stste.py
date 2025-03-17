from design_patterns.state.base import Stats


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
