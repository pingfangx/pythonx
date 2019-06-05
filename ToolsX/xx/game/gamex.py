import os
import time

from xx.game import adbx
from xx.game import imagex
from xx.game.image_log import ImageLog


class Action:
    def __init__(self, status, status_desc=None, action_desc=None, next_status=None, delay=1, perform=None):
        """

        :param status:状态
        :param status_desc:状态描述
        :param action_desc:操作描述，也用于查找状态图片
        :param next_status:执行任务后的下一状态，如果置为 0 会重新开启检查状态
        :param delay:执行任务后的延时
        :param perform:执行的方法，如果为 None 则执行点击，方法签名为 action, adb, position
        """
        self.status = status
        self.status_desc = status_desc
        self.action_desc = action_desc
        self.next_status = status + 1 if next_status is None else next_status
        self.delay = delay
        self.perform = perform

    @staticmethod
    def perform_default(arguments):
        """默认操作，就是点击"""
        arguments.adb.tap_position(arguments.position)


class Arguments:
    def __init__(self, game, action, adb, position):
        self.game = game
        self.action = action
        self.adb = adb
        self.position = position


class GameX:
    """游戏助手"""

    def __init__(self, config_path, screenshot, action_list, adb=None, debug=False):
        """

        :param config_path:配置目录，可区分不同分辨
        :param screenshot:截图
        :param action_list:操作列表
        :param adb 如果需要，可以指定路径等
        :param debug 是否调试，用于保存截图
        """
        self.config_path = config_path
        self.screenshot = screenshot
        self.action_list = action_list
        if adb is None:
            adb = adbx.Adb()
        self.adb = adb
        self.image_log = ImageLog(self.screenshot, max_count=100, debug=debug)
        self.pre_status = 0
        self.pre_status_not_found_index = 0
        """记录上一次查找状态时未找到的索引"""

    def run(self):
        """运行"""
        self.adb.test_device()

        # 设置一定的循环次数或退出条件
        i = 0
        max_times = 100
        while i < max_times:
            i += 1
            self.get_status_and_start_loop()
        print(f'运行超限 {max_times} 次，结束')

    def get_status_and_start_loop(self):
        """获取状态并开始循环"""
        print('开始截图')
        self.adb.screenshot(self.screenshot)
        print('读取状态')
        status = self.get_status()
        print('获取到状态为 ', status)
        last_status = status
        last_status_count = 0
        while status:
            # 获取到初始状态后，每次获取相关状态
            if last_status == status:
                last_status_count += 1
                if last_status_count > 10:
                    print('已经连续 %d 次是状态 %d，退出循环' % (10, status))
                    return 0
            else:
                last_status = status
                last_status_count = 0
            print('开始截图')
            self.adb.screenshot(self.screenshot)
            if last_status_count == 0:
                print('查找状态', status)
            else:
                print('第 %d 次查找状态 %d' % (last_status_count, status))
            status = self.check_status(status)

    def get_status(self):
        """
        获取状态，按照传递的 action_list 中的顺序
        如果找到相关操作，则执行
        :return: 对应状态，如果没有到某一状态没有对应图片，则返回 0
        """
        for action in self.action_list:
            status = self.check_status(action.status, True)
            if status is None:
                # 为空，继续
                continue
            else:
                # 有结果或为 0 异常，退出
                return status
        return 0

    def check_status(self, status, loop_check=False):
        """
        检查是否是对应状态
        :param status: 要检查的状态
        :param loop_check: 是否是循环检查
        :return:
        """
        print('检查是否是状态', status)
        # 检查数量
        self.image_log.check_log_image_count()
        index, action = self.get_status_action(status)
        status_path = self.get_action_status_img(action)
        if status_path:
            print('状态图片', os.path.split(status_path)[1])
        else:
            print('没有找到状态 %d 对应的图片' % status)
            if not loop_check:
                self.image_log.save_not_found_image(self.image_log.get_log_image(status, status_path, '未找到'))
            # 没有图片返回 0 终止搜索
            return status if loop_check else 0
        position = imagex.find_image(self.screenshot, status_path, self.image_log.get_log_image(status, status_path))
        if position:
            # 未找到索引置为 -1
            self.pre_status_not_found_index = -1
            print('找到状态 %d 对应的图片，当前状态为 %s，执行操作' % (status, action.status_desc))
            find_status = status  # 先记录找到的状态，在 perform_action 中不使用该状态
            status = self.perform_action(action, position)
            self.pre_status = find_status  # 赋值
            return status
        else:
            # 没有找到，记录未找到的索引
            self.pre_status_not_found_index = index
            if not loop_check:
                return status
            else:
                # 否则返回 None 继续查找
                return None

    def get_action_status_img(self, action):
        """获取操作状态的图片"""
        # 使用 status 和 action_desc
        name_list = [
            '%d' % action.status,
            '%02d' % action.status,
            '%s' % action.action_desc,
        ]
        # 不同扩展名
        file_name_list = []
        file_name_list.extend([name + '.png' for name in name_list])
        file_name_list.extend([name + '.jpg' for name in name_list])
        for file_name in file_name_list:
            file_path = os.path.join(self.config_path, file_name)
            if os.path.exists(file_path):
                return file_path
        return None

    def get_status_action(self, status):
        """
        获取状态对应的操作，返回结果为 (index,action)
        如果没有预设，返回一个默认
        """
        find_action = []
        for i, action in enumerate(self.action_list):
            if action.status == status:
                find_action.append((i, action))
        if find_action:
            # 找到
            if len(find_action) > 1:
                # 有多个结果
                for i, (index, action) in enumerate(find_action):
                    if index == self.pre_status_not_found_index:
                        # 找到上一次未查找的结果
                        if i + 1 < len(find_action):
                            # 还有下一个，返回下一个
                            return find_action[i + 1]
            # 只有一个结果，或者循环结束，没有匹配
            return find_action[0]
        else:
            return -1, Action(status)

    def perform_action(self, action, position):
        """
        执行操作
        """
        arguments = Arguments(self, action, self.adb, position)
        if action.perform is None:
            action.perform_default(arguments)
        else:
            action.perform(arguments)
        print('sleep', action.delay)
        time.sleep(action.delay)
        if callable(action.next_status):
            return action.next_status(arguments)
        else:
            return action.next_status
