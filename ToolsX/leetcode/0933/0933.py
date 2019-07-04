class RecentCounter:
    """如果超时就移除

    如果 t 不是递增的，传任意时间，统计任意时间之前的，那应该就需要队列所有请求了

    答案中使用的是 collections.deque()
    """

    def __init__(self):
        self.queue = []

    def ping(self, t: int) -> int:
        self.queue.append(t)
        while t - self.queue[0] > 3000:
            self.queue.pop(0)
        return len(self.queue)
