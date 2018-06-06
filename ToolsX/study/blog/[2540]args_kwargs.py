def f1(a, b, c=0, d=1, *args, **kwargs):
    print('a={},b={},c={},d={},args={},kwargs={}'.format(a, b, c, d, args, kwargs))


# def f2(a, b, c=0, d):  # non-default parameter follows default parameter


def f2(a, b, c=0, *, d, **kwargs):
    # 可以直接命名为 * ，如果命名为 *ignore 反而提示未使用
    print('a={},b={},c={},d={},kwargs={}'.format(a, b, c, d, kwargs))


def f3(**kwargs):
    for k, v in kwargs.items():
        print('{} = {}'.format(k, v))


def f4(a=1, b=2):
    print('a={},b={}'.format(a, b))


class Demo:
    def main(self):
        f1(1, 2)
        f1(1, 2, 3)
        f1(1, 2, d=3, c=4)  # 可以任意顺序
        f1(1, 2, 3, 4, 'a', 'b')
        f1(1, 2, 3, 4, 'a', 'b', x=9, y='10')  # 可变参数和关键字参数，分别解析为元组和字典
        # f1(1, 2, 3, 4, 'a', x=9, 'b', y='10')  # Positional argument after keyword argument
        f1(1, 2, 3, 4, *('a', 'b'), **{'x': 9, 'y': '10'})  # 解包元组和字典

        # f2(1, 2, 3, 4)  # Parameter 'd' unfilled
        f2(1, 2, 3, d=4)
        f2(1, 2, d=4)

        # f3({'a': 1, 'b': 2})  # Unexpected argument，不可以直接传字典
        f3(**{'a': 1, 'b': 2})  # Unexpected argument
        f3(a=3, b=4)  # 可以

        f4(a=3, b=4)
        f4(b=5, a=6)
        f4(**{'a': 7, })
        f4(**{'a': 7, 'b': 8})
        # f4(**{'a': 7, 'b': 8, 'c': 9})#TypeError: f4() got an unexpected keyword argument 'c'


if __name__ == '__main__':
    Demo().main()
