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
    # 创建一个原始图像的灰度版本，所有操作在灰度版本中处理，然后在RGB图像中使用相同坐标还原
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    # 加载将要搜索的图像模板
    # template = cv2.imread(target_img, 0)
    # 为了中文文件名
    template = cv2.imdecode(np.fromfile(target_img, dtype=np.uint8), 0)
    # 记录图像模板的尺寸
    w, h = template.shape[::-1]

    # 使用matchTemplate对原始灰度图像和图像模板进行匹配
    result = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(result >= threshold)
    # 过滤出的结果是一个元组 (y 数组,x 数组)

    length = len(loc[0])
    if length > 0:
        # 取平均值
        result = int(np.average(loc[1])), int(np.average(loc[0]))
        if result_img:
            # for pt in zip(*loc[::-1]):
            #     cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
            # 一红一黑
            thickness = 2
            cv2.rectangle(img_rgb, result, (result[0] + w, result[1] + h), (0, 0, 0), thickness)
            cv2.rectangle(img_rgb, (result[0] - thickness, result[1] - thickness),
                          (result[0] + w + thickness, result[1] + h + thickness), (0, 0, 255), thickness)
            # cv2.imwrite(result_img, img_rgb)
            cv2.imencode(os.path.splitext(result_img)[1], img_rgb)[1].tofile(result_img)
            print('共 %d 个匹配结果，输出至 %s' % (len(loc[0]), result_img))
        return result
    else:
        if result_img:
            print('没有匹配结果')
        return None
