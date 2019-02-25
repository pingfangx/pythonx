import os
import subprocess
import time
from tkinter import *

from xx import iox


class WechatGame:
    """
    微信跳一跳游戏
    相关博文:[《[2460]程序猿是怎么玩游戏的——微信跳一跳》](http://blog.pingfangx.com/2460.html)
    """

    def __init__(self):
        self.label_img = None
        "显示截图"
        self.label_msg = None
        "显示消息"
        self.btn_auto = None
        self.auto = True
        """
        自动,如果启用,则在点击右键后自动执行模拟滑动
        然后再执行截屏
        """
        self.pre_msg = ""
        "上一条消息，简单处理用来显示 2 行数据"
        self.img_path = 'data/img.png'
        "图片地址"
        self.default_duration = 715
        self.duration = self.default_duration
        "按下时长"
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0

    def main(self):
        action_list = [
            ['退出', exit],
            ['显示图片', self.show_img],
            ['截屏', self.get_screenshot],
            ['模拟滑动', self.mock_swipe],
        ]
        iox.choose_action(action_list)

    def get_screenshot(self):
        """截屏"""
        cmd = 'adb shell /system/bin/screencap -p /sdcard/xx/screenshot.png'
        self.call(cmd)

        cmd = 'adb pull /sdcard/xx/screenshot.png %s' % os.path.abspath(self.img_path)
        self.call(cmd)
        self.log('截屏完成')

    def mock_swipe(self):
        """
        模拟滑动
        这里加上了 50 ，之前用按键精灵是很准确的，改用 swipe 之后，需要加上 50 的偏差
        """
        cmd = 'adb shell input swipe 500 500 500 500 %d' % (self.duration + 50)
        self.call(cmd)

    def toggle_auto(self):
        self.auto = not self.auto
        if self.btn_auto:
            if self.auto:
                self.btn_auto.config(text="已启用自动")
            else:
                self.btn_auto.config(text="已禁用自动")

    @staticmethod
    def call(cmd):
        """执行命令"""
        print(cmd)
        subprocess.call(cmd, shell=True)

    def show_img(self):
        """显示图片"""
        root = Tk()
        root.title("微信跳一跳X")

        frame = Frame(root)
        btn_screen_shot = Button(frame, text="重新截屏", command=self.change_screenshot)
        btn_screen_shot.grid(row=0, column=0)

        btn_mock_swipe = Button(frame, text="模拟滑动", command=self.mock_swipe)
        btn_mock_swipe.grid(row=0, column=1, padx=10)

        btn_auto = Button(frame, text="", command=self.toggle_auto)
        btn_auto.grid(row=0, column=2)
        self.btn_auto = btn_auto
        # 执行一次
        self.auto = not self.auto
        self.toggle_auto()

        frame.pack()

        label_msg = Label(root, text="\n消息输出")
        label_msg.pack()
        self.label_msg = label_msg

        bm = PhotoImage(file=self.img_path)
        lable = Label(root, image=bm)

        lable.bind("<Button-1>", self.onclick_mouse_left)
        lable.bind("<Button-3>", self.onclick_mouse_right)
        lable.pack()
        self.label_img = lable

        mainloop()

    def onclick_mouse_left(self, event):
        self.x1 = event.x_root
        self.y1 = event.y_root
        self.log("左键点击的位置是 %d,%d" % (event.x_root, event.y_root))

    def onclick_mouse_right(self, event):
        self.x2 = event.x_root
        self.y2 = event.y_root
        self.log("右键点击的位置是 %d,%d" % (event.x_root, event.y_root))
        self.cal_distance()
        if self.auto:
            self.log("模拟滑动...")
            self.mock_swipe()
            self.log("重新截屏...")
            time.sleep(5)
            self.change_screenshot()

    def cal_distance(self):
        """
        计算距离
        测试发现，在起始状态的 x=450,y=260 时，按下 715 ms 正好能跳到中心
        跳的距离与按下时间成正比
        :return:
        """
        dx = abs(self.x1 - self.x2)
        dy = abs(self.y1 - self.y2)
        len0 = (450 ** 2 + 260 ** 2) ** (1 / 2)
        len1 = (dx ** 2 + dy ** 2) ** (1 / 2)
        self.duration = int(self.default_duration * len1 / len0)
        self.log('x=%d,y=%d,len0=%d,len1=%d,duration=%d' % (dx, dy, len0, len1, self.duration))

    def change_screenshot(self):
        """截屏并显示"""
        if not self.label_img:
            return
        self.get_screenshot()
        bm = PhotoImage(file=self.img_path)
        self.label_img.config(image=bm)
        self.label_img.bm = bm
        # 这里为什么既要 config 又要 bm

    def log(self, msg):
        """输出，为了方便查看，显示到界面上"""
        print(msg)
        if self.label_msg:
            self.label_msg.config(text=self.pre_msg + '\n' + msg)
            self.pre_msg = msg


if __name__ == '__main__':
    WechatGame().main()
