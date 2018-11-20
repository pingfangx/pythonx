import os

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from xx import iox


class NinePatchTool:
    """
    绘制 .9
    不想一像素一像素的拖动
    找了一下没有相关的工具，于是简单写一个，通过参数指定绘制的地方

    需要注意的是，左右两边的位置会影响最后的拉伸结果
    比如 100*100，加上点9 变为 102* 102
    在上方左右各画 5 个点，即 (6,10) 和 (-6,-10) 设置拉伸
    结果为 6,7,8,9,10 像素和 92,93,94,95,96
    如果按像素计数，0,1,2,3,4,5 有 6 个像素，而 101,100,99,98,97 只有 5 个像素
    但实际就是 6-11 与 92-97 才能等距缩放
    6-11 与 91-96，右边较多，中心偏左
    原因暂不知道
    """
    black_pixel = np.array([0, 0, 0, 255])
    transparent_pixel = np.array([0, 0, 0, 0])

    def __init__(self, image_path, draw_position, add_transparent=False):
        """

        :param image_path:图片路径
        :param draw_position:绘制位置
        :param add_transparent 是否添加边缘的空像素
        """
        self.image_path = image_path
        self.add_transparent = add_transparent

        # 位置
        self.position = [[] for _ in range(4)]
        if draw_position:
            length = len(draw_position)
            for i in range(4):
                if length > i:
                    self.position[i] = draw_position[i]
        # 赋值完成

    def main(self):
        action_list = [
            ['退出', exit],
            ['显示图片', self.read_and_show_image],
            ['画 .9', self.draw_nine_image],
        ]
        iox.choose_action(action_list)

    def read_and_show_image(self):
        """读取并显示"""
        img = self.read_img()
        rows, cols, _ = img.shape
        print(f'宽:{cols},高:{rows}')
        self.show_image(img)

    def draw_nine_image(self):
        """绘制 .9"""
        img = self.read_img()
        rows, cols, _ = img.shape

        right = cols - 1
        bottom = rows - 1

        # 绘制左边竖线
        self.draw_black_line(img, True, stop=bottom, x=0, y=0, position_index=0)

        # 绘制上方横线
        self.draw_black_line(img, False, stop=right, x=0, y=0, position_index=1)

        # 绘制右边竖线
        self.draw_black_line(img, True, stop=bottom, x=0, y=right, position_index=2)

        # 绘制下方横线
        self.draw_black_line(img, False, stop=right, x=bottom, y=0, position_index=3)

        self.show_image(img)

        save_path = 'result/' + self.image_path
        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))
        print(f'保存至 {save_path}')
        Image.fromarray(img).save(save_path)

    def draw_black_line(self, img, vertical, stop, x=0, y=0, position_index=0):
        """在某个方向画黑线"""
        for i in range(1, stop):
            if not self.position[position_index]:
                # 为空
                if vertical:
                    self.set_black_pixel(img, i, y)
                else:
                    self.set_black_pixel(img, x, i)
            else:
                for start, end in self.position[position_index]:
                    # 这里需要多加 1 ，如类说明所述
                    if start < 0:
                        start = stop + start + 1
                    if end < 0:
                        end = stop + end + 1
                    if end < start:
                        start, end = end, start
                    if start <= i <= end:
                        if vertical:
                            self.set_black_pixel(img, i, y, True)
                        else:
                            self.set_black_pixel(img, x, i, True)

    def set_black_pixel(self, img, x, y, print_msg=False):
        """将某个像素设为默色"""
        if print_msg:
            print(f'({x},{y})')
        img[x, y] = self.black_pixel

    def read_img(self, img_path=None):
        """读取图片"""
        if img_path is None:
            img_path = self.image_path
        img = np.array(Image.open(img_path))
        if self.add_transparent:
            img = self.add_nine_patch_transparent(img)
        return img

    @staticmethod
    def show_image(img):
        """显示图片"""
        plt.figure("图片")
        plt.imshow(img)
        plt.axis('off')
        plt.show()

    def add_nine_patch_transparent(self, img):
        """添加边缘的空像素"""
        rows, cols, _ = img.shape
        # 不太会用 insert 方法
        # 插入第一行，最后一行
        img = np.insert(img, [0, rows], self.transparent_pixel, axis=0)
        # 插入第一列，最后一列
        img = np.insert(img, [0, cols], self.transparent_pixel, axis=1)
        return img


if __name__ == '__main__':
    # 已经加了边缘的各 1 px
    p_image_path = r'ic_common_place_holder.9.png'
    p_draw_position = [
        # left
        [(6, 10), (-6, -10)],
        # top
        [(6, 10), (-6, -10)],
        # right 绘制全部
        [],
        # bottom 绘制全部
        [],
    ]
    NinePatchTool(p_image_path, p_draw_position, add_transparent=False).main()
