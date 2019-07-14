import timeit
from typing import List


def test_commands(commands: List[str], repeat=100, number=100000, **kwargs):
    r = []
    size = len(commands)
    for i, command in enumerate(commands):
        print(f'测试命令 {i + 1}/{size}:{command}')
        time = timeit.repeat(command, repeat=repeat, number=number, **kwargs)
        r.append(f'{command},avg:{sum(time) / len(time)}')
    print('\n'.join(r))
