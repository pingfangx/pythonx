"""正常的 str 与 空内插

print('test')
print(f'test')

因为 print 需要输出，所以只测试赋值语句
测试发现差距不大，只有当 f'' 中需要计算时才会有差距
"""
from tool.timeit import test_commands

if __name__ == '__main__':
    commands = [
        "a='test'",
        "b=f'test'",
        "c=f'test{1+2}'"
    ]
    test_commands(commands)
