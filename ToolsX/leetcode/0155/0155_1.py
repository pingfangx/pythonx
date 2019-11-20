class MinStack:
    """如果没有特殊限制，就记录最小值就好了

    因为 getMin 只是获取，不是 pop
    如果是 pop 的话，每次移除时就需要算最小值
    按这种方法，将最值的计算转移到了 pop 中
    而 getMin 还量常量时间，哈

    如果是 pop，应该需要使用小顶堆

    1
    看了答案，我们知道，pop 时其实不需要再计算 min
    因为 stack lilo 所以只需要保存 push 时的最小值就行了
    """

    def __init__(self):
        self.stack = []

    def push(self, x: int) -> None:
        if self.stack:
            self.stack.append((x, min(x, self.stack[-1][1])))
        else:
            self.stack.append((x, x))

    def pop(self) -> None:
        if self.stack:
            self.stack.pop()

    def top(self) -> int:
        return None if not self.stack else self.stack[-1][0]

    def getMin(self) -> int:
        return None if not self.stack else self.stack[-1][1]


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
