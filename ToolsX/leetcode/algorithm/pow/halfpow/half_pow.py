class Pow:
    """求幂"""

    def half_pow(self, x, n):
        """
        二分幂，英文命名没有找到相关介绍

        O(n)=O(log n)

        比如 2^4=2^2 * 2^2
        而 2^5=2 * 2^2 * 2^2

        n=5
            n=2
                n=1
                t=2
            t=4
        t=4*4*2=32

        n=10
            n=5
                n=2
                    n=1
                    t=2
                t=4
            t=2*4*4=32
        t=32*32=1024

        相当于 (2^2 * 2^2 * 2)^2

        递归，t 的值为各次递归时的乘方值

        >>> Pow().half_pow(2,5)
        32
        >>> Pow().half_pow(2,10)
        1024
        """
        if n == 1:
            return x
        else:
            # 一半的平方
            t = self.half_pow(x, n // 2)
            if n & 1 == 0:
                return t * t
            else:
                # 为奇数多乘一个 x
                return x * t * t

    def half_pow1(self, x, n):
        """上面的方法使用递归，这里使用迭代

        n=5,r=2,t=4
            n=2,r=2,t=16
                n=1,r=32

        n=10,r=1,t=4
            n=5,r=4,t=16
                n=2,r=4,t=256
                    n=1,r=4*256=1024

        >>> Pow().half_pow1(2,5)
        32
        >>> Pow().half_pow1(2,10)
        1024
        """
        r = 1
        # 注意要取为 x 第一次乘就直接平方
        t = x
        while n:
            if n & 1 == 1:
                # t 只有奇数时才乘，乘的是 t 不是 2，在上面的方法中，虽然是乘 2 ，但是递归回上一层时，又平方了，如果再递归一层，就 4 次方了
                # 所以这里乘以 t ，而 t 也总是平方增长的，符合递归时的平方增长
                # 当 n == 1 时将 t 的累积结果乘到 r 上
                r *= t
            # t 每次循环都需要乘，从 2 开始每次平方
            t *= t
            n >>= 1
        return r


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
