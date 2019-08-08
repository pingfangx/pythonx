def swap_with_add(a, b):
    """
    x+y=z
    y=z-x

    所以
    x'=x+y
    x'-y=x
    x'-x=y
    """
    print(a, b)
    a = a + b
    print(a, b)
    b = a - b
    print(a, b)
    a = a - b
    print(a, b)


def swap_with_xor(a, b):
    """
    需要类似于逆运算
    0 xor 1 = 1
    1 xor 1 = 0
    1 xor 0 = 1

    0 xor 0 = 1
    1 xor 0 = 0

    1 xor 1 = 0
    0 xor 1 = 1

    满足
    """
    print_binary(a, b)
    a ^= b
    print_binary(a, b)
    b ^= a
    print_binary(a, b)
    a ^= b
    print_binary(a, b)


def print_binary(a, b):
    print(bin(a), bin(b))


if __name__ == '__main__':
    swap_with_add(1, 2)
    swap_with_xor(1, 2)
