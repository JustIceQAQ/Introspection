def flatten_json(y, delimiter="."):
    out = {}

    def flatten(x, name=""):
        if type(x) is dict:
            for key, value in x.items():
                flatten(value, f"{name}{key}{delimiter}")

        elif type(x) is list:

            for index, item in enumerate(x, 0):
                flatten(item, f"{name}{index}{delimiter}")

        else:
            out[name[:-1]] = x

    flatten(y)
    return out
