import abc
import uuid

from code.design_patterns.x01_abstract_factory.furniture import Chair, Sofa, GamingChair
from code.design_patterns.x01_abstract_factory.material import MaterialEnum


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
