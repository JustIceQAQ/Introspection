import abc
import dataclasses
import enum
from typing import List, Dict
import uuid
import pprint


class MaterialEnum(str, enum.Enum):
    # 材質類型
    Wooden = "Wooden"  # 木頭材質
    Iron = "Iron"  # 鋼鐵材質
    Bamboo = "Bamboo"  # 竹子材質


@dataclasses.dataclass
class Chair:
    # 椅子原型
    code: str
    material: str
    limited_weight: int = 110  # kg
    length: int = 50  # cm
    width: int = 45  # cm
    height: int = 80  # cm
    has_armrest: bool = False
    number_of_people: int = 1


@dataclasses.dataclass
class Sofa:
    code: str
    material: str
    limited_weight: int = 220  # kg
    length: int = 50  # cm
    width: int = 45  # cm
    height: int = 80  # cm
    has_armrest: bool = True
    number_of_people: int = 2


@dataclasses.dataclass
class GamingChair:
    code: str
    material: str
    limited_weight: int = 300  # kg
    length: int = 50  # cm
    width: int = 45  # cm
    height: int = 133  # cm
    has_armrest: bool = True
    number_of_people: int = 1


class AbstractFactory(abc.ABC):
    """一切的原型，只能被繼承使用"""

    def get_code(self) -> str:
        return uuid.uuid4().hex

    @abc.abstractmethod
    def create_chair(self):
        # 建立椅子 的方法
        return NotImplementedError

    @abc.abstractmethod
    def create_sofa(self):
        # 建立沙發 的方法
        return NotImplementedError

    @abc.abstractmethod
    def create_gaming_chair(self):
        # 建立電競椅 的方法
        return NotImplementedError


class WoodenFactory(AbstractFactory):
    """木製工廠"""
    material = MaterialEnum.Wooden

    def create_chair(self) -> Chair:
        return Chair(code=self.get_code(), material=self.material)

    def create_sofa(self) -> Sofa:
        return Sofa(code=self.get_code(), material=self.material)

    def create_gaming_chair(self) -> GamingChair:
        return GamingChair(code=self.get_code(), material=self.material)


class IronFactory(AbstractFactory):
    """鐵製工廠"""
    material = MaterialEnum.Iron

    def create_chair(self) -> Chair:
        return Chair(code=self.get_code(), material=self.material)

    def create_sofa(self) -> Sofa:
        return Sofa(code=self.get_code(), material=self.material)

    def create_gaming_chair(self) -> GamingChair:
        return GamingChair(code=self.get_code(), material=self.material)


class BambooFactory(AbstractFactory):
    """竹製工廠"""
    material = MaterialEnum.Bamboo

    def create_chair(self) -> Chair:
        return Chair(code=self.get_code(), material=self.material)

    def create_sofa(self) -> Sofa:
        return Sofa(code=self.get_code(), material=self.material)

    def create_gaming_chair(self) -> GamingChair:
        return GamingChair(code=self.get_code(), material=self.material)


class FlowFactory:

    def __init__(self, use_factory: AbstractFactory):
        self.use_factory = use_factory
        self.chair_number = 0
        self.sofa_number = 0
        self.gaming_chair_number = 0

    def set_chair_number(self, number: int):
        self.chair_number = number

    def set_sofa_number(self, number: int):
        self.sofa_number = number

    def set_gaming_chair_number(self, number: int):
        self.gaming_chair_number = number

    def workshop(self, factory_product, quantity: int) -> List:
        return [factory_product() for _ in range(quantity)]

    def run(self) -> Dict[str, List]:
        if self.chair_number is None:
            raise ValueError("chair number is empty.")
        if self.sofa_number is None:
            raise ValueError("sofa number is empty.")
        if self.gaming_chair_number is None:
            raise ValueError("gaming chair is empty.")
        return {
            "chair": self.workshop(self.use_factory.create_chair, self.chair_number),
            "sofa": self.workshop(self.use_factory.create_sofa, self.sofa_number),
            "gaming_chair": self.workshop(self.use_factory.create_gaming_chair, self.gaming_chair_number)
        }


if __name__ == '__main__':
    # wooden_factory, iron_factory, bamboo_factory = WoodenFactory(), IronFactory(), BambooFactory()
    # print(wooden_factory.create_chair())
    # print(wooden_factory.create_sofa())
    # print(wooden_factory.create_gaming_chair())
    #
    # print(iron_factory.create_chair())
    # print(iron_factory.create_sofa())
    # print(iron_factory.create_gaming_chair())
    #
    # print(bamboo_factory.create_chair())
    # print(bamboo_factory.create_sofa())
    # print(bamboo_factory.create_gaming_chair())

    my_factory = FlowFactory(use_factory=WoodenFactory())
    my_factory.set_chair_number(2)
    my_factory.set_gaming_chair_number(5)
    my_factory.set_sofa_number(3)

    production_completed = my_factory.run()
    pprint.pprint(production_completed)
