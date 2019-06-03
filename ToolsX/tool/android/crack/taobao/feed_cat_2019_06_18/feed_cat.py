import time

from scrapy_spider.scrapy_spider.common.statistic.remaining_time_tatistics import RemainingTimeStatistics
from xx import iox
from xx.game import adbx
from xx.game import gamex


class FeedCat:
    """淘宝 2019 6.18 理想猫"""

    def __init__(self):
        self.screenshot_path = 'ignore/screenshot.png'
        """截图路径"""
        self.config_path = '1080_1920'
        """配置路径"""
        self.game_count = 0
        """记录游戏次数"""
        self.adb = adbx.Adb()
        """adb"""
        self.statistics = RemainingTimeStatistics(50)

    def main(self):
        action_list = [
            ['退出', exit],
            ['adb 测试', self.adb.test_device],
            ['截屏', self.adb.screenshot, self.screenshot_path],
            ['开始游戏', self.start_game],
        ]
        iox.choose_action(action_list, True)

    def start_game(self):
        """游戏流程"""
        action_list = [
            # 下一状态置为 0 ，重新搜索,
            gamex.Action(1, '首页', '领喵币', 2),
            gamex.Action(2, '领喵币中心', '去逛店', 3, delay=12),
            gamex.Action(3, '店铺首页', '猫猫出现啦', 4),
            gamex.Action(4, '成功抓到猫猫', '开心收下', 0),
        ]
        for action in action_list:
            if action.delay == 1:
                # 修改默认
                # action.delay = 5
                pass
            action.perform = self.perform
        game = gamex.GameX(self.config_path, self.screenshot_path, action_list, adb=self.adb, debug=True)
        game.run()

    def add_game_count(self):
        """添加游戏次数"""
        self.game_count += 1
        divider = "=" * 30
        print(f'{divider}当前已进行游戏 {self.game_count} 次{divider}')
        if self.game_count >= 50:
            print(f'已进行游戏 50 次,退出')
            exit()
        else:
            self.statistics.count(self.game_count)

    def perform(self, arguments):
        """执行操作"""
        action = arguments.action
        status = action.status
        adb = arguments.adb
        if status == 4:
            # 成功抓到猫猫
            # 执行默认
            action.perform_default(arguments)
            # 累加次数
            self.add_game_count()
            # 按返回
            time.sleep(1)
            adb.back()
        else:
            # 默认
            action.perform_default(arguments)

    @staticmethod
    def next_status(arguments):
        """下一个状态"""
        return arguments.action.next_status


if __name__ == '__main__':
    FeedCat().main()
