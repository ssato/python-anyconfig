# flake8: noqa: E122
"""A simple map with values."""
import datetime
import math

DATA = {
    'x': {
        'a0': 0,
        'a1': 1,
        'a2': 42,
        'a3': - 17,
        'b0': 'foo',
        'b1': 'Hello,\nworld\n',
        'b2': '"Lorem ipsum dolor sit amet,\nconsectetur adipiscing elit\n',
        'b3': 'Tom "Dubs" Preston-Werner',
        'b4': "I [dw]on't need \\d{2} apples",
        'c0': 3735928559,
        'c1': 493,
        'c2': 214,
        'c3': 3.14159265,
        'c4': 1000000.0,
        'c5': - math.inf,
        # .. note::
        #    math.nan is not comparable with '==' and math.isnan should be used
        #    but it's a bit hard to do that so I comment this until finding a
        #    solution for this issue.
        # 'c6': math.nan,
        'd0': datetime.datetime(
            1979, 5, 27, 0, 32,
            tzinfo=datetime.timezone(
            datetime.timedelta(seconds=32400))),
        'd1': datetime.date(2024, 1, 8),
    }
}
