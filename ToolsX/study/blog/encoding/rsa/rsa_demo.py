import math

from study.blog.encoding.rsa import rsa_math


def output(txt):
    print(txt)


class RSADemo:
    """示例"""

    def __init__(self, p, q, e, m):
        self.p = p
        self.q = q
        self.e = e
        self.m = m

        # 检查
        if not rsa_math.is_prime(self.p):
            output(f'p 不是质数 {self.p}')
            exit()
        if not rsa_math.is_prime(self.q):
            output(f'q 不是质数 {self.q}')
            exit()
        if not rsa_math.is_coprime(self.p, self.q):
            output(f'p q 不互质 {self.p} {self.q}')
            exit()

        output(f'p={self.p},q={self.q}')

        # 求出 n
        self.n = self.p * self.q
        binary_n = bin(self.n)
        output(f'n={self.n},二进制为 {binary_n},密钥长度为 {len(binary_n[2:])}')

        # 求出欧拉函数
        self.phi_n = (self.p - 1) * (self.q - 1)
        output(f'φ(n)=φ({self.n})={self.phi_n}')

        if not (self.e < self.phi_n):
            output(f'e = {self.e} 不小于 φ(n) {self.phi_n} ')
            exit()

        # 求模反元素
        self.d = rsa_math.modular_multiplicative_inverse(self.e, self.phi_n)
        output(f'求出 d={self.d}')

        self.public_key = (self.n, self.e)
        self.private_key = (self.n, self.d)
        output(f'公钥 {self.public_key}')
        output(f'私钥 {self.private_key}')

    def encrypt(self, m: int) -> int:
        """加密"""
        return rsa_math.encrypt(self.n, self.e, m)

    def decrypt(self, c: int) -> int:
        """解密"""
        return rsa_math.decrypt(self.n, self.d, c)

    def demo(self):
        m = 65
        c = self.encrypt(m)
        output(f'加密 {m}，得到结果 {c}')
        result = self.decrypt(c)
        output(f'解密 {c}，得到结果 {result}')

        p, q = self.try_factorization(self.n)
        output(f'尝试解密 {c}，得到结果 {p},{q}')

    @staticmethod
    def try_factorization(n):
        """尝试分解"""
        print(f'尝试分解 n {n}')
        sqrt = int(math.sqrt(n)) + 1
        for i in range(2, sqrt + 1):
            if n % i == 0:
                # 可以整除
                if rsa_math.is_prime(i) and rsa_math.is_prime(n // i):
                    return i, n // i
        return 0, 0


if __name__ == '__main__':
    RSADemo(
        p=61,
        q=53,
        e=17,
        m=65,
    ).demo()
