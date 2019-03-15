from scrapy_spider.common.statistic.base_statistics import BaseStatistics


class IncreaseStatistics(BaseStatistics):
    """增加量"""

    start_num = 0
    pre_num = 0
    count_num = 0

    def start(self, num):
        self.start_num = self.pre_num = self.count_num = num

    def count(self, num):
        self.pre_num = self.count_num
        self.count_num = num

    def dif(self) -> int:
        return self.count_num - self.start_num

    def print_count(self) -> str:
        return f'{self.count_num - self.pre_num}(本次)/{self.count_num - self.start_num}(累计)/{self.count_num}(总计)'
