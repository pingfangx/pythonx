"""
将字符转为数字
int(c)
ord(c)-ord(0)
应该是 int 快

结果是 ord 快，为什么……
int('1'),avg:0.016635743094403833
ord('1')-ord('0'),avg:0.011780517700376905
int('9'),avg:0.016104229760858808
ord('9')-ord('0'),avg:0.011589385002644885
"""
from tool.timeit import test_commands

if __name__ == '__main__':
    commands = [
        "int('1')",
        "ord('1')-ord('0')",
        "int('9')",
        "ord('9')-ord('0')",
    ]
    test_commands(commands)
