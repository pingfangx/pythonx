import ctypes


def get_google_tk(a=''):
    """
    计算谷歌翻译的 tk
    翻译原始 js 自 :https://github.com/cocoa520/Google_TK/blob/master/google_tk.html
    :return: 
    """
    b = 406644
    b1 = 3293161072

    jd = "."
    _b = "+-a^+6"
    zb = "+-3^+b+-f"

    e = list()
    length = len(a)
    for g in range(0, length):
        m = ord(a[g])
        if 128 > m:
            e.append(m)
        elif 2048 > m:
            e.append(m >> 6 | 192)
        elif 55296 == (m & 64512) and g + 1 < length and 56320 == (ord(a[g + 1]) & 64512):
            m = 65536 + ((m & 1023) << 10) + (ord(a[++g]) & 1023)
            e.append(m >> 18 | 240)
            e.append(m >> 12 & 63 | 128)
        else:
            e.append(m >> 12 | 224)
            e.append(m >> 6 & 63 | 128)
            e.append(m & 63 | 128)

    a = b
    for f in e:
        a += f
        a = get_rl(a, _b)
    a = get_rl(a, zb)
    a ^= b1 or 0
    if 0 > a:
        a = (a & 2147483647) + 2147483648
    a %= 1E6
    a = int(a)
    return str(a) + jd + str(a ^ b)


def get_rl(a, b):
    t = 'a'
    yb = '+'
    for c in range(0, len(b) - 2, 3):
        d = b[c + 2]
        if d >= t:
            d = ord(d) - 87
        else:
            d = int(d)
        if b[c + 1] == yb:
            d = unsigned_right_shift(a, d)
        else:
            d = a << d
        if b[c] == yb:
            a = a + d & 4294967295
        else:
            a = a ^ d
    return a


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
