"""
数组拼接时，使用 extend 和 + 哪个快

+ 更快
[1]+[2],avg:0.017182895124134998
[1].extend([2]),avg:0.025214982981907982
"""
from tool.timeit import test_commands

if __name__ == '__main__':
    commands = [
        "[1]+[2]",
        "[1].extend([2])",
    ]
    test_commands(commands)
