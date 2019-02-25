import subprocess
import time

from xx import iox


class AppStartTimer:
    """app 启动计时，用于启动优化时的统计"""

    def __init__(self, package, activity,
                 consider_time='TotalTime',
                 loop_count=10,
                 loop_delay=0,
                 print_cmd=True):
        """

        :param package: 包名
        :param activity: Activity 名，可以 . 开头的相对名
        :param consider_time:关心的时间， start 命令输出 ThisTime，TotalTime，WaitTime 不区分大小写
        :param loop_count: 循环执行的次数
        :param loop_delay:单次循环的延时，单位 s ，配合延时及 Displayed 过滤 log ，可以查看启动第一个 Activity 的时间
        :param print_cmd:是否输出命令
        """
        """
        :param package: 包名
        :param count: 次数
        :param consider_time: 关心的时间
        """
        if not package or not activity:
            print('package or activity is empty')
            exit()
        self.package = package
        self.intent = f'{package}/{activity}'
        self.loop_count = loop_count
        self.consider_time = consider_time
        self.loop_delay = loop_delay
        self.print_cmd = print_cmd

        # 用于循环计时
        self.time_sum = 0
        """总时间"""

        self.loop_index = 0
        """"循环 index"""

    def main(self):
        action_list = [
            ['退出', exit],
            ['执行一次', self.run_once],
            ['循环执行', self.run_in_loop],
        ]
        iox.choose_action(action_list)

    def run_once(self):
        """执行一次"""
        cmd = f'adb shell am force-stop {self.package}'
        if self.print_cmd:
            print(cmd)
        subprocess.call(cmd, shell=True)

        # 该命令好像要后台才有效，所以先执行 force-stop
        cmd = f'adb shell am kill {self.package}'
        if self.print_cmd:
            print(cmd)
        subprocess.call(cmd, shell=True)

        # -S 参数似乎并没有杀掉进程，似乎还是存在内存占用，导致随着启动次数时间有增加，于是在之前使用 kill 杀死进程
        cmd = f'adb shell am start -S -W {self.intent}'
        if self.print_cmd:
            print(cmd)
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        lines = process.stdout.readlines()
        for line in lines:
            line = line.decode()
            if line.lower().startswith(self.consider_time.lower()):
                spend_time = line.split(':')[1].strip()
                self.print_time(int(spend_time))

    def run_in_loop(self):
        """循环执行"""
        self.time_sum = 0
        for self.loop_index in range(self.loop_count):
            self.run_once()
            if self.loop_delay:
                time.sleep(self.loop_delay)

    def print_time(self, spend_time):
        # 累加
        self.time_sum += spend_time
        avg_time = self.time_sum / (self.loop_index + 1)
        print(f'第 {self.loop_index+1}/{self.loop_count} 次时间 {spend_time}，当前平均时间 {avg_time:#.2f}')


if __name__ == '__main__':
    AppStartTimer('', '', loop_count=10, print_cmd=False, loop_delay=5).main()
