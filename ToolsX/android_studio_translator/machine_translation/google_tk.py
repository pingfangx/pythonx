def TL(a=''):
    k = ''
    b = 406644
    b1 = 3293161072

    jd = "."
    _b = "+-a^+6"
    Zb = "+-3^+b+-f"

    e = list()
    f = 0
    length = len(a)
    for g in range(0, length):
        m = ord(a[g])
        if 128 > m:
            e.append(m)
        else:
            if 2048 > m:
                e.append(m >> 6 | 192)
            else:
                if 55296 == (m & 64512) and g + 1 < length and 56320 == (ord(a[g + 1]) & 64512):
                    m = 65536 + ((m & 1023) << 10) + (ord(a[++g]) & 1023)
                    e.append(m >> 18 | 240)
                    e.append(m >> 12 & 63 | 128)
                else:
                    e.append(m > 12 | 224)
                    e.append(m >> 6 & 63 | 128)
                    e.append(m & 63 | 128)

    a = b
    for f in range(len(e)):
        a += e[f]
        a = RL(a, _b)
    a = RL(a, Zb)
    a ^= b1 or 0
    if 0 > a:
        a = (a & 2147483647) + 2147483648
    a %= 1E6
    a = int(a)
    return str(a) + jd + str(a ^ b)


def RL(a, b):
    t = 'a'
    Yb = '+'
    for c in range(0, len(b) - 2, 3):
        d = b[c + 2]
        if d >= t:
            d = ord(d) - 87
        else:
            d = int(d)
        if b[c + 1] == Yb:
            d = unsigned_right_shift(a, d)
        else:
            d = a << d
        if b[c] == Yb:
            a = a + d & 4294967295
        else:
            a = a ^ d
    return a


import ctypes


def unsigned_right_shift(n, i):
    """
    无符号右移
    from http://www.jianshu.com/p/24d11ab44ae6
    :param n: 
    :param i: 
    :return: 
    """
    # 数字小于0，则转为32位无符号uint
    if n < 0:
        n = ctypes.c_uint32(n).value
    # 正常位移位数是为正数，但是为了兼容js之类的，负数就右移变成左移好了
    if i < 0:
        return -int_overflow(n << abs(i))
    return int_overflow(n >> i)


def int_overflow(val):
    maxint = 2147483647
    if not -maxint - 1 <= val <= maxint:
        val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
    return val
