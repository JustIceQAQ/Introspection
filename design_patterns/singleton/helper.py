from design_patterns.singleton.base import Singleton


class Gril(Singleton):
    pass

if __name__ == '__main__':
    a = Gril()
    b = Gril()
    print(id(a), id(b))
    print(f"{id(a)==id(b)}")