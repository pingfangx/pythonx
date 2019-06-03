import time

try:
    from xx import iox
    from xx.game import adbx
    from xx.game import imagex
    from xx.game import gamex
except Exception as ex:
    print(ex)
    print('请将 xx 添加至 lib ，或将脚本与 xx 文件夹放到相同目录')
    exit(1)


class FeedCat:
    """淘宝 2018 6.18 养萌猫"""

    def __init__(self):
        self.screenshot = 'ignore/screenshot.png'
        self.config_path = '1080_1920'
        self.game_count = 0
        """记录游戏次数"""
        self.adb = adbx.Adb()

    def main(self):
        action_list = [
            ['退出', exit],
            ['adb 测试', self.adb.test_device],
            ['截屏', self.adb.screenshot, self.screenshot],
            ['开始玩游戏', self.start_game],
            ['开始喂猫', self.start_feed],
        ]
        iox.choose_action(action_list)

    def start_game(self):
        """游戏流程"""
        action_list = [
            # 下一状态置为 0 ，重新搜索
            gamex.Action(99, '没中', '这次没中', 0),
            gamex.Action(10, '抽奖', '马上抽', 11),
            gamex.Action(1, '首页', '快速抢红包', 0),
            gamex.Action(2, '打气球游戏', '打气球', 5),
            gamex.Action(3, '取猫粮游戏', '取猫粮', 6),
            gamex.Action(4, '左右滑游戏', '甩猫爪', 7),
            # 因为 5 中的点猫页面会误判，所以放到后面
            gamex.Action(8, '游戏结果', '再玩一次', next_status=self.next_status),
            gamex.Action(9, '游戏结果', '关闭按钮', 0),
            gamex.Action(11, '抽奖结果', '关闭按钮', 0),  # 只需点击关闭
            gamex.Action(5, '打气球界面', '点击猫爪', 0),
            gamex.Action(6, '取猫粮界面', '点击猫爪', 0, delay=10),
            gamex.Action(7, '左右滑界面', '关闭按钮', 0),  # 关闭按钮只用来校验
            gamex.Action(100, '弹出广告', '关闭按钮2', 0),  # 关闭按钮只用来校验
        ]
        for action in action_list:
            if action.delay == 1:
                # 修改默认
                action.delay = 5
            action.perform = self.perform
        game = gamex.GameX(self.config_path, self.screenshot, action_list, adb=self.adb, debug=True)
        game.run()

    def start_feed(self):
        """喂猫"""
        action_list = [
            gamex.Action(99, '猫粮不足', '领猫粮', delay=5, perform=self.perform),
            # 下一状态置为 0 ，重新搜索
            gamex.Action(2, '拍照结果', '关闭按钮', 0, delay=1),
            gamex.Action(1, '首页', '喂养', 0, delay=5),
        ]
        game = gamex.GameX(self.config_path, self.screenshot, action_list, adb=self.adb, debug=True)
        game.run()

    def add_game_count(self):
        """添加游戏次数"""
        self.game_count += 1
        print('{0}当前已进行游戏 {1} 次{0}'.format('=' * 30, self.game_count))

    def perform(self, arguments):
        """
        执行操作
        """
        action = arguments.action
        status = action.status
        adb = arguments.adb
        position = arguments.position
        if status == 5:
            # 点击10次
            for i in range(10):
                adb.tap_position(position)
        elif status == 7:
            # 左右滑
            for i in range(10):
                adb.swipe(100, 1500, 1000, 1500, 300)
                time.sleep(2)
                adb.swipe(1000, 1500, 100, 1500, 300)
                time.sleep(2)
        elif status == 8:
            # 游戏结果
            self.add_game_count()
            action.perform_default(arguments)
        elif status == 9:
            # 点击关闭
            self.add_game_count()
            action.perform_default(arguments)
            time.sleep(1)
            adb.back()
        elif status == 99:
            # 结束程序
            print('没有猫粮，结束脚本')
            exit()
        else:
            # 默认
            action.perform_default(arguments)

    @staticmethod
    def next_status(arguments):
        """下一个状态"""
        action = arguments.action
        status = action.status
        if status == 8:
            return arguments.game.pre_status
        else:
            return action.next_status


if __name__ == '__main__':
    FeedCat().main()
