"""
x**2
x*x
哪个快

后者快
2**2,avg:0.0025651156002803027
2*2,avg:0.0020352332593166407
"""

if __name__ == '__main__':
    import timeit

    commands = [
        "2**2",
        "2*2",
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
