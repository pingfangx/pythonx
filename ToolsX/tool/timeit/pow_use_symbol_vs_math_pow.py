"""
x**0.5
math.pow(x,0.5)
哪个快

用符号更快
by_symbol(),avg:0.012180216483431212
by_math(),avg:0.04381652316952369

"""

import math


def by_symbol():
    return 2 ** 0.5


def by_math():
    return math.pow(2, 0.5)


if __name__ == '__main__':
    import timeit

    commands = [
        "by_symbol()",
        "by_math()",
    ]
    number = 100000
    repeat = 100
    r = []
    size = len(commands)
    for i, command in enumerate(commands):
        print(f'测试命令 {i + 1}/{size}:{command}')
        time = timeit.repeat(command, repeat=repeat, number=number, setup="from __main__ import by_symbol,by_math")
        r.append(f'{command},avg:{sum(time) / len(time)},time:{time}')
    print('\n'.join(r))
