"""正常的 str 与 空内插

print('test')
print(f'test')

因为 print 需要输出，所以只测试赋值语句
测试发现差距不大，只有当 f'' 中需要计算时才会有差距
"""

if __name__ == '__main__':
    import timeit

    commands = [
        "a='test'",
        "b=f'test'",
        "c=f'test{1+2}'"
    ]
    number = 100000
    repeat = 100
    r = []
    size = len(commands)
    for i, command in enumerate(commands):
        print(f'测试命令 {i + 1}/{size}:{command}')
        time = timeit.repeat(command, repeat=repeat, number=number)
        r.append(f'{command},avg:{sum(time) / len(time)},time:{time}')
    print('\n'.join(r))
