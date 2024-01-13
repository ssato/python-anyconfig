from collections import OrderedDict

DATA = OrderedDict(
    [
        ('a', 1),
        ('b', 'c'),
        (
            'd',
            OrderedDict([('e', OrderedDict([('f', [1, 2, 3]), ('g', 'GGG')]))])
        )
    ]
)
