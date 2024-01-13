from collections import OrderedDict as OD

DATA = OD(
    {
        "a": 1, "b": "c",
        "d": OD(
            {"e": OD({"f": [1, 2, 3], "g": "GGG"})}
        )
    }
)
