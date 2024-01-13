"""_dict example."""
import collections


DATA = collections.OrderedDict(
    [
        (
            'x',
            collections.OrderedDict(
                [('a0', 0), ('a1', 1), ('a2', 42), ('a3', -17)]
            )
        )
    ]
)
