import random

from helpers.timit import Timit


def binary_search(a: list[int], x: int) -> int | None:
    low = 0
    high = len(a) - 1
    while low <= high:
        mid = (low + high) // 2
        mid_value = a[mid]
        if mid_value == x:
            return mid
        elif mid_value < x:
            low = mid + 1
        else:
            high = mid - 1
    return None

if __name__ == "__main__":
    random_list = [random.randint(1, 100) for i in range(10000)] + [100]
    random_list.sort()
    with Timit():
        print(binary_search(random_list, 100))
    with Timit():
        for i in random_list:
            if i== 100:
                break
        print(i)