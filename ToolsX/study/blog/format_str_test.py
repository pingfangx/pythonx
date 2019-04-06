import timeit

p = 'param'


def print_str():
    """直接输出"""
    print('test', p)


def concat_str():
    """拼接"""
    print('test ' + str(p))


def interpolation_str():
    """插值"""
    print(f'test {p}')


def format_str():
    """格式化"""
    print('test %s' % p)


def test(method_name):
    import_pre = 'from __main__ import '
    repeat = 100
    number = 10_000
    result = timeit.repeat(f'{method_name}()', f'{import_pre}{method_name}', repeat=repeat, number=number)
    return f'{method_name:20s}\trepeat {repeat}\tnumber {number}\tsum:{sum(result)}\tavg:{sum(result) / len(result)}'


def test_all():
    name_list = [
        'print_str',
        'concat_str',
        'interpolation_str',
        'format_str',
    ]
    result = '\n'.join([test(name) for name in name_list])
    print(result)


if __name__ == '__main__':
    test_all()
