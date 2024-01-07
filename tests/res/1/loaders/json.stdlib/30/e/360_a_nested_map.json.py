class MyDict(dict):
    pass


DATA = MyDict(
    {
        "a": 1, "b": "c",
        "d": MyDict(
            {"e": MyDict({"f": [1, 2, 3], "g": "GGG"})}
        )
    }
)
