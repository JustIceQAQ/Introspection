import abc


class Stats(abc.ABC):
    @abc.abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError()


class StatsV2(abc.ABC):
    def __init__(self, name: str):
        self._name = name

    def get_name(self) -> str:
        return self._name

    def is_match(self, state_info) -> bool:
        return False


class Contest(abc.ABC):
    def __init__(self, state_info:int, cur_state:StatsV2):
        self._states: set[StatsV2] = set()
        self._state_info = state_info
        self._cur_state = cur_state

    def add_state(self, state: StatsV2):
        self._states.add(state)

    def change_state(self, state: StatsV2):
        self._cur_state = state

    def set_state_info(self, number: int):
        self._state_info = number
        for state in self._states:
            if state.is_match(number):
                print(f"{self._cur_state.get_name()} -> {state.get_name()}")
                self.change_state(state)
                break
