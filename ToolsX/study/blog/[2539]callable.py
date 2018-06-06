import types

from inspect import isfunction

"""
[Python 判断变量是否是一个方法](https://www.pingfangx.com/blog/2539)

判断是否是方法

首先看到 function 与 method 的不同
最后选用 callable

use callable
<function a at 0x00000000003C3E18> ,result is True
<bound method Demo.b of <__main__.Demo object at 0x0000000009CE0780>> ,result is True
<function Demo.c at 0x0000000009EBD1E0> ,result is True
<built-in function open> ,result is True
<function Demo.main.<locals>.<lambda> at 0x0000000002288950> ,result is True

use hasattr
<function a at 0x00000000003C3E18> ,result is True
<bound method Demo.b of <__main__.Demo object at 0x0000000009CE0780>> ,result is True
<function Demo.c at 0x0000000009EBD1E0> ,result is True
<built-in function open> ,result is True
<function Demo.main.<locals>.<lambda> at 0x0000000002288950> ,result is True

use FunctionType
<function a at 0x00000000003C3E18> ,result is True
<bound method Demo.b of <__main__.Demo object at 0x0000000009CE0780>> ,result is False
<function Demo.c at 0x0000000009EBD1E0> ,result is True
<built-in function open> ,result is False
<function Demo.main.<locals>.<lambda> at 0x0000000002288950> ,result is True

use isfunction
<function a at 0x00000000003C3E18> ,result is True
<bound method Demo.b of <__main__.Demo object at 0x0000000009CE0780>> ,result is False
<function Demo.c at 0x0000000009EBD1E0> ,result is True
<built-in function open> ,result is False
<function Demo.main.<locals>.<lambda> at 0x0000000002288950> ,result is True
"""


def a():
    pass


class Demo:
    def b(self):
        pass

    @staticmethod
    def c():
        pass

    def main(self):
        test_list = [
            a,
            self.b,
            self.c,
            open,
            lambda x: x,
        ]
        print('\nuse callable')
        for test in test_list:
            print('%s ,result is %s' % (test, callable(test)))

        print('\nuse hasattr')
        for test in test_list:
            print('%s ,result is %s' % (test, hasattr(test, '__call__')))

        print('\nuse FunctionType')
        for test in test_list:
            print('%s ,result is %s' % (test, isinstance(test, types.FunctionType)))

        print('\nuse isfunction')
        for test in test_list:
            print('%s ,result is %s' % (test, isfunction(test)))


if __name__ == '__main__':
    Demo().main()
