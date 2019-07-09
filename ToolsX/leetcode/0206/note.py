if __name__ == '__main__':
    import dis

    dis.dis('a, b, c=b, c, a')
    """
  1           0 LOAD_NAME                0 (b)
              2 LOAD_NAME                1 (c)
              4 LOAD_NAME                2 (a)
              # 注栈后 b>c>a
              6 ROT_THREE
              # 后两个上移，a>b>c
              8 ROT_TWO
              # 交换最上两个，a>c>b
             10 STORE_NAME               2 (a)
             12 STORE_NAME               0 (b)
             14 STORE_NAME               1 (c)
             16 LOAD_CONST               0 (None)
             18 RETURN_VALUE
    """

    dis.dis('c,a,b=b,c,a')
    """
  1           0 LOAD_NAME                0 (b)
              2 LOAD_NAME                1 (c)
              4 LOAD_NAME                2 (a)
              # b>c>a
              6 ROT_THREE
              # a>b>c
              8 ROT_TWO
              # a>c>b
             10 STORE_NAME               1 (c)
             12 STORE_NAME               2 (a)
             14 STORE_NAME               0 (b)
             16 LOAD_CONST               0 (None)
             18 RETURN_VALUE
    """
    dis.dis('a,b,c=a,b,c')
    """还是一样，没有优化
  1           0 LOAD_NAME                0 (a)
              2 LOAD_NAME                1 (b)
              4 LOAD_NAME                2 (c)
              # a>b>c
              6 ROT_THREE
              # c>a>b
              8 ROT_TWO
              # c>b>a
             10 STORE_NAME               0 (a)
             12 STORE_NAME               1 (b)
             14 STORE_NAME               2 (c)
             16 LOAD_CONST               0 (None)
             18 RETURN_VALUE"""
    dis.dis('a,b,c,d=d,a,b,c')
    """
    变为 TUPLE 了
  1           0 LOAD_NAME                0 (d)
              2 LOAD_NAME                1 (a)
              4 LOAD_NAME                2 (b)
              6 LOAD_NAME                3 (c)
              8 BUILD_TUPLE              4
             10 UNPACK_SEQUENCE          4
             12 STORE_NAME               1 (a)
             14 STORE_NAME               2 (b)
             16 STORE_NAME               3 (c)
             18 STORE_NAME               0 (d)
             20 LOAD_CONST               0 (None)
             22 RETURN_VALUE
    """
