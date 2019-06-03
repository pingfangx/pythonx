import time

from .base_statistics import BaseStatistics


class RemainingTimeStatistics(BaseStatistics):
    """统计"""
    start_time: float
    max_speed = 0
    """最大速度"""

    def __init__(self, total=0):
        """初始化并启动"""
        self.total = total
        self.start()

    def start(self):
        """开始任务"""
        self.start_time = time.time()

    def count(self, count):
        """计数

        :param count: 当前进度
        :return:
        """
        spend_time = time.time() - self.start_time
        if spend_time == 0:
            spend_time = 1
        speed = count / spend_time
        if speed > self.max_speed:
            self.max_speed = speed
        remaining_time = (self.total - count) / speed
        print(f'item {count}/{self.total}, took {self.format_time(spend_time)},'
              f' speed {speed * 60:.2f}/{self.max_speed * 60:.2f} items/min,'
              f' remains {self.format_time(remaining_time)}')
