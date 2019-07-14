"""
x**0.5
math.pow(x,0.5)
哪个快

用符号更快
by_symbol(),avg:0.012180216483431212
by_math(),avg:0.04381652316952369

"""

import math

from tool.timeit import test_commands


def by_symbol():
    return 2 ** 0.5


def by_math():
    return math.pow(2, 0.5)


if __name__ == '__main__':
    commands = [
        "by_symbol()",
        "by_math()",
    ]
    test_commands(commands, setup="from __main__ import by_symbol,by_math")
