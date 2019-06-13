import time

try:
    # noinspection PyUnresolvedReferences
    from scrapy_spider.scrapy_spider.common.statistic.remaining_time_tatistics import RemainingTimeStatistics
except ImportError:
    pass
from xx import iox
from xx.game import adbx, imagex
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
        try:
            self.statistics = RemainingTimeStatistics(50)
        except NameError:
            self.statistics = None
        self.game = gamex.GameX(self.config_path, self.screenshot_path, [], adb=self.adb, debug=True)
        self.store_home_action = gamex.Action(3, '店铺首页', '猫猫出现啦', 4)
        self.store_home_action_2 = gamex.Action(3, '店铺首页', '猫猫出现了', 0)

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
        version = 3
        if version == 2:
            # 后来更新
            action_list = [
                # 下一状态置为 0 ，重新搜索,
                gamex.Action(1, '首页', '召唤理想猫', 2),
                gamex.Action(2, '首页弹窗', '逛店铺', self.next_status, delay=15),
                self.store_home_action,
                gamex.Action(4, '成功抓到猫猫', '开心收下', 0),
            ]
        elif version == 3:
            action_list = [
                # 下一状态置为 0 ，重新搜索,
                gamex.Action(1, '首页', '合合卡', 2),
                gamex.Action(2, '首页弹窗', '进店领取', self.next_status, delay=15),
                self.store_home_action,
                gamex.Action(4, '成功抓到猫猫', '开心收下', 0),
            ]
        else:
            # 旧版本
            action_list = [
                # 下一状态置为 0 ，重新搜索,
                gamex.Action(1, '首页', '领喵币', 2),
                gamex.Action(2, '领喵币中心', '去浏览', self.next_status, delay=25),
                gamex.Action(2, '领喵币中心', '去逛店', self.next_status, delay=15),
                self.store_home_action,
                gamex.Action(4, '成功抓到猫猫', '开心收下', 0),
            ]
        for action in action_list:
            if action.delay == 1:
                # 修改默认
                # action.delay = 5
                pass
            action.perform = self.perform
        self.game.action_list = action_list
        self.game.run()

    def add_game_count(self):
        """添加游戏次数"""
        self.game_count += 1
        divider = "=" * 30
        print(f'{divider}当前已进行游戏 {self.game_count} 次{divider}')
        if self.game_count >= 50:
            print(f'已进行游戏 50 次,退出')
            exit()
        else:
            if self.statistics:
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
            time.sleep(1)
        else:
            # 默认
            action.perform_default(arguments)

    def next_status(self, arguments):
        """下一个状态"""
        if arguments.action.status == 2:
            # 从中心过去，需要找一下有没有“猫猫出现啦”
            # 截图
            self.adb.screenshot(self.game.screenshot)
            # 找图
            status_path = self.game.get_action_status_img(self.store_home_action)
            position = imagex.find_image(self.game.screenshot, status_path,
                                         self.game.image_log.get_log_image(self.store_home_action.status, status_path))
            if position:
                # 操作
                return self.game.perform_action(self.store_home_action, position)

            # 查找猫猫出现了
            status_path = self.game.get_action_status_img(self.store_home_action_2)
            position = imagex.find_image(self.game.screenshot, status_path,
                                         self.game.image_log.get_log_image(self.store_home_action.status, status_path))
            if position:
                # 点击直接获得，所以后续按返回
                self.game.perform_action(self.store_home_action_2, position)
            # 没有找到则按返回
            self.adb.back()
            time.sleep(1)
            return 0
        return arguments.action.status + 1


if __name__ == '__main__':
    FeedCat().main()
