class Solution:
    def countAndSay(self, n: int) -> str:
        """
        读懂题目，递归就好了
        """
        if n < 1:
            return ''
        if n == 1:
            return '1'
        else:
            text = self.countAndSay(n - 1)
            buffer = ''
            pre = ''
            times = 0
            for c in text:
                if c == pre:
                    # 相同，累加次数
                    times += 1
                else:
                    if pre:
                        # 不相同，记录之前的
                        buffer += str(times) + pre
                    # 重新计数
                    times = 1
                    pre = c
            buffer += str(times) + pre
            return buffer


if __name__ == '__main__':
    for i in range(6):
        print(Solution().countAndSay(i))
