class MinStack:
    """如果没有特殊限制，就记录最小值就好了

    因为 getMin 只是获取，不是 pop
    如果是 pop 的话，每次移除时就需要算最小值
    按这种方法，将最值的计算转移到了 pop 中
    而 getMin 还量常量时间，哈

    如果是 pop，应该需要使用小顶堆
    """

    def __init__(self):
        """
        initialize your data structure here.
        """
        self.data = []
        self.min = None

    def push(self, x: int) -> None:
        self.data.append(x)
        if self.min is None:
            self.min = x
        else:
            if x < self.min:
                self.min = x

    def pop(self) -> None:
        top = self.data.pop()
        if top == self.min:
            self.min = self.find_min()

    def top(self) -> int:
        return self.data[-1]

    def getMin(self) -> int:
        return self.min

    def find_min(self):
        # 有系统方法，就不写了
        if self.data:
            return min(self.data)
        else:
            return None
        # min = None
        # for i in self.data:
        #     if min is None or i < min:
        #         min = i
        # return min


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
