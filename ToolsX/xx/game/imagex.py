import os

import cv2
import numpy as np


def find_image(source_img, target_img, result_img=None):
    """
    在 source_img 中查找 find_img
    :param source_img: 源图
    :param target_img: 查找目标
    :param result_img: 如果不为 None，则输出结果至文件
    :return:
    """

    # 加载原始 RGB 图像
    img_rgb = cv2.imread(source_img)
    # 创建一个原始图像的灰度版本，所有操作在灰度版本中处理，然后在 RGB 图像中使用相同坐标还原
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    # 加载将要搜索的图像模板
    # template = cv2.imread(target_img, 0)
    # 为了中文文件名
    template = cv2.imdecode(np.fromfile(target_img, dtype=np.uint8), 0)
    # 记录图像模板的尺寸
    w, h = template.shape[::-1]

    # 使用 matchTemplate 对原始灰度图像和图像模板进行匹配
    result = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    # 阈值
    threshold = 0.8
    loc = np.where(result >= threshold)
    # 过滤出的结果是一个元组，在此示例中，通俗的说，0 表示第几行（对应点的 y），1 表示第几列（对应点的 x）
    # 所以也就是 (y 数组,x 数组)，其中相应位置的 x,y 组合起来是点坐标
    y_array, x_array = loc
    # 方便后面用 del
    y_array, x_array = list(y_array), list(x_array)

    length = len(loc[0])
    if length > 0:
        # 过滤 y，先过滤 y 以优先选择靠上的
        y_min = np.min(y_array)
        for i in range(len(y_array) - 1, -1, -1):
            if y_array[i] - y_min > h:
                # print(f'y 删除 {x_array[i]},{y_array[i]}')
                cv2.rectangle(img_rgb, (x_array[i], y_array[i]), (x_array[i] + w, y_array[i] + h), (255, 0, 0), 2)
                del x_array[i]
                del y_array[i]
        # 过滤 x
        x_min = np.min(x_array)
        # 如果超过宽，认为有多张图，抛弃后面的
        for i in range(len(x_array) - 1, -1, -1):
            if x_array[i] - x_min > w:
                # 删除
                # print(f'x 删除 {x_array[i]},{y_array[i]}')
                cv2.rectangle(img_rgb, (x_array[i], y_array[i]), (x_array[i] + w, y_array[i] + h), (0, 255, 0), 2)
                del x_array[i]
                del y_array[i]
        # 取平均值，要注意当找到多张图时，平均值就变成了多个结果的中点了，所以前面过滤了 x 和 y
        result = int(np.average(x_array)), int(np.average(y_array))
        if result_img:
            # 绘制找出的所有框（点为左上角）
            # for pt in zip(x_array, y_array):
            #     cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 0), 2)
            # 一黑一红
            thickness = 20

            # 内黑
            # 减去边框
            pt1 = np.add(result, (-thickness, -thickness))
            # 加上宽高
            pt2 = np.add(result, (w, h))
            # 加上边框
            pt2 = np.add(pt2, (thickness, thickness))
            cv2.rectangle(img_rgb, tuple(pt1), tuple(pt2), (0, 0, 0), thickness)

            # 外红
            # 减去边框
            pt1 = np.add(pt1, (-thickness, -thickness))
            # 加上边框
            pt2 = np.add(pt2, (thickness, thickness))
            cv2.rectangle(img_rgb, tuple(pt1), tuple(pt2), (0, 0, 255), thickness)
            # cv2.imwrite(result_img, img_rgb)
            cv2.imencode(os.path.splitext(result_img)[1], img_rgb)[1].tofile(result_img)
            print('共 %d 个匹配结果，输出至 %s' % (len(loc[0]), result_img))
        return result
    else:
        if result_img:
            print('没有匹配结果')
        return None
