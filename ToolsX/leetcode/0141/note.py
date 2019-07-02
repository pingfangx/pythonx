"""

如何判断是否访问过某个元素？
判断两个元素相等，可以使用 is ，或者使用 id()

6.10.3. Identity comparisons
The operators is and is not test for an object’s identity: x is y is true if and only if x and y are the same object. An Object's identity is determined using the id() function. x is not y yields the inverse truth value. 4



# O(1) 算法中为什么一定会相遇，会不会每次都错过呢？
不会，因为是1 和 2 的关系。
当 fast 绕一圏走到 slow 前面时，要么位于前面 2 个元素(两步后相遇)，要么位于前面 1 个元素(一步后相遇)。
"""

if __name__ == '__main__':
    import dis

    dis.dis('a=b=c=1')
    """
  1           0 LOAD_CONST               0 (1)
              2 DUP_TOP
              4 STORE_NAME               0 (a)
              6 DUP_TOP
              8 STORE_NAME               1 (b)
             10 STORE_NAME               2 (c)
             12 LOAD_CONST               1 (None)
             14 RETURN_VALUE
    """
