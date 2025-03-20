def func(i: int):
    if i <= 1:
        return 1
    return i + func(i - 1)


if __name__ == "__main__":
    print(func(5))
