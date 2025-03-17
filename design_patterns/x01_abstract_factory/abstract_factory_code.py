from typing import List, Dict
import pprint

from code.design_patterns.x01_abstract_factory.factory import AbstractFactory, WoodenFactory, IronFactory, BambooFactory


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
    wooden_factory, iron_factory, bamboo_factory = WoodenFactory(), IronFactory(), BambooFactory()

    my_factory = FlowFactory(use_factory=WoodenFactory())
    my_factory.set_chair_number(2)
    my_factory.set_gaming_chair_number(5)
    my_factory.set_sofa_number(3)

    production_completed = my_factory.run()
    pprint.pprint(production_completed)
