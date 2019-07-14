"""
x**2
x*x
哪个快

后者快
2**2,avg:0.0025651156002803027
2*2,avg:0.0020352332593166407
"""
from tool.timeit import test_commands

if __name__ == '__main__':
    commands = [
        "2**2",
        "2*2",
    ]
    test_commands(commands, repeat=1000)
