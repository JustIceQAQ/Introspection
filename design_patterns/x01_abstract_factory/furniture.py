import dataclasses


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
