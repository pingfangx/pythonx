import os
import subprocess
from tkinter import *

import cv2

from xx import filex
from xx import iox


class WechatGame:
    def __init__(self):
        self.label_img = None
        self.label_msg = None
        self.pre_msg = ""
        self.img_path = 'data/img.png'
        self.duration = 0
        self.duration_path = 'data/duration.txt'
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0

    def main(self):
        action_list = [
            ['退出', exit],
            ['截屏', self.get_screenshot, self.img_path],
            ['写入时间', self.write_duration],
            ['计算', self.cal_img, self.img_path],
            ['显示图片', self.show_img],
        ]
        iox.choose_action(action_list)

    def get_screenshot(self, img_path):
        """截屏"""
        cmd = 'adb shell /system/bin/screencap -p /sdcard/xx/screenshot.png'
        self.call(cmd)

        cmd = 'adb pull /sdcard/xx/screenshot.png %s' % os.path.abspath(img_path)
        self.call(cmd)
        self.log('截屏完成')

    def write_duration(self):
        """写入时间"""
        filex.write(self.duration_path, str(self.duration))
        cmd = 'adb push %s /sdcard/xx/duration.txt' % os.path.abspath(self.duration_path)
        self.call(cmd)
        self.log('已写入时间 %d' % self.duration)

    @staticmethod
    def call(cmd):
        """执行命令"""
        print(cmd)
        subprocess.call(cmd, shell=True)

    def cal_img(self, img_path):
        """计算"""
        img = cv2.imread(img_path)
        # 彩色转灰度
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 2 值化
        ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        img, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # loop over the contours
        for c in contours:
            # compute the center of the contour
            M = cv2.moments(c)
            if M["m00"] == 0:
                continue
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            # draw the contour and center of the shape on the image
            cv2.drawContours(img, [c], -1, (0, 255, 0), 2)
            cv2.circle(img, (cX, cY), 20, (255, 0, 0), -1)
            cv2.putText(img, "center", (cX - 20, cY - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # show the image
            rows, cols = img.shape
            rate = 0.3
            img_zoom = cv2.resize(img, (int(cols * rate), int(rows * rate)), interpolation=cv2.INTER_AREA)
            cv2.imshow("Image", img_zoom)
            cv2.waitKey(0)

    def show_img(self):
        """显示图处"""
        root = Tk()

        btn_screen_shot = Button(root, text="重新截屏", command=self.change_screenshot)
        btn_screen_shot.pack()

        label_msg = Label(root, text="消息输出")
        label_msg.pack()
        self.label_msg = label_msg

        bm = PhotoImage(file=self.img_path)

        lable = Label(root, image=bm)
        lable.bm = bm

        lable.bind("<Button-1>", self.callBackLeft)
        lable.bind("<Button-3>", self.callBackRight)
        lable.pack()
        self.label_img = lable

        mainloop()

    def callBackLeft(self, event):
        self.x1 = event.x_root
        self.y1 = event.y_root
        self.log("左键点击的位置是 %d,%d" % (event.x_root, event.y_root))

    def callBackRight(self, event):
        self.x2 = event.x_root
        self.y2 = event.y_root
        self.log("右键点击的位置是 %d,%d" % (event.x_root, event.y_root))
        self.cal_distance()

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
        self.duration = int(715 * len1 / len0)
        self.log('x=%d,y=%d,len0=%d,len1=%d,duration=%d' % (dx, dy, len0, len1, self.duration))
        self.write_duration()

    def change_screenshot(self):
        """截屏并显示"""
        if not self.label_img:
            return
        self.get_screenshot(self.img_path)
        bm = PhotoImage(file=self.img_path)
        self.label_img.config(image=bm)
        self.label_img.bm = bm

    def log(self, msg):
        """输出，为了方便查看，显示到界面上"""
        print(msg)
        if self.label_msg:
            self.label_msg.config(text=self.pre_msg + '\n' + msg)
            self.pre_msg = msg


if __name__ == '__main__':
    WechatGame().main()
