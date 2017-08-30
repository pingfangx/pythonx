import json
import os
import re

from bs4 import BeautifulSoup

from xx import excelx
from xx import filex
from xx import iox
from xx import netx


class TiebaFloor:
    """
    贴吧抢楼统计工具
    """

    def __init__(self, config_file):
        """
        
        :param config_file: 配置文件
        """
        self.config_file = config_file

    def main(self):
        config_file = self.config_file
        config = filex.get_config(config_file)
        if not config.has_option('thread', 'id'):
            print('配置不正确，缺少id')
            return
        if not config.has_option('thread', 'max_page'):
            print('配置不正确，缺少max_page')
            return

        tid = config.get('thread', 'id')
        max_page = config.getint('thread', 'max_page')

        floors_file = 'data/all_floors.txt'
        result_file = 'data/result.txt'
        action_list = [
            ['退出', exit],
            ['抓取所有楼层', self.get_all_floors, tid, max_page, floors_file],
            ['检查中奖情况', self.validate_gift, floors_file, config_file, result_file],
            ['将结果写入excel', self.write_to_excel, result_file],
        ]
        iox.choose_action(action_list)

    def get_all_floors(self, tid, max_page, result_file):
        """
        获取所有楼层
        :param tid:贴子id 
        :param max_page: 最大页数
        :param result_file: 结果文件
        :return: 
        """
        if os.path.exists(result_file):
            os.remove(result_file)
        for page in range(1, max_page + 1):
            self.get_floor_of_page(tid, page, result_file)

    @staticmethod
    def get_floor_of_page(tid, page, result_file):
        """
        获取某一页的所有楼层
        :param tid: 贴子id
        :param page: 页数
        :param result_file:结果文件 
        :return: 
        """
        url = 'http://tieba.baidu.com/p/%s?pn=%d' % (tid, page)
        page = netx.get(url)
        print('开始解析')
        # 解析结果
        soup = BeautifulSoup(page, "html.parser")
        floor = soup.select('.l_post.j_l_post.l_post_bright')
        result = []
        for div in floor:
            # 含有clearfix的是广告
            if 'clearfix' not in div['class']:
                data_field = json.loads(div['data-field'])
                # print(data_field)

                author = data_field['author']
                name = author['user_name']
                level_id = author['level_id']

                content = data_field['content']
                post_no = content['post_no']
                post_id = content['post_id']

                content = div.select_one('#post_content_' + str(post_id))
                if content is not None:
                    content = content.text
                else:
                    content = ''
                result.append(str(Floor(floor_no=post_no, name=name, level=level_id, content=content.lstrip())) + '\n')

        filex.write_lines(result_file, result, mode='a')

    def validate_gift(self, floors_file, config_file, result_file):
        """
        校验礼物
        :param floors_file: 楼层文件
        :param config_file: 奖品配置文件
        :param result_file: 结果文件
        :return: 
        """
        lines = filex.read_lines(floors_file)
        if lines is None:
            return

        config = filex.get_config(config_file)
        if config is None:
            return

        # 读取所有的楼层
        floor_dict = dict()
        for line in lines:
            line = line.replace('\n', '')
            floor = Floor.from_str(line)
            floor_dict[floor.floor_no] = floor

        # 检查礼物的楼层
        for gift_name, gift_floors in config.items('gift'):
            for gift_floor in gift_floors.split(' '):
                gift_floor = int(gift_floor)
                if gift_floor in floor_dict.keys():
                    # 礼物
                    floor_dict[gift_floor].gift_name = gift_name
                    # 检查礼物
                    check_floor = gift_floor
                    while check_floor is not None:
                        # 防止递归，这里让其返回
                        check_floor = self.validate_floor(gift_floor, check_floor, floor_dict, gift_name, config)
        # 输出结果
        result = []
        for floor_no, floor in floor_dict.items():
            result.append(floor.to_excel_string() + '\n')
        filex.write_lines(result_file, result)

    @staticmethod
    def validate_floor(gift_floor, next_floor, floor_dict, gift_name, config):
        """
        校验楼层是否有效
        :param gift_floor:礼物楼层 
        :param next_floor: 校验楼层
        :param floor_dict: 楼层字典
        :param gift_name: 礼物名称
        :param config: 礼物配置
        :return: 
        """
        floor = floor_dict[next_floor]
        if config.options('validation') is None:
            # 没有校验，直接返回
            floor.gift_validation = '%s,%d层的礼物' % (gift_name, gift_floor)
            return

        msg = None
        max_floor = sorted(floor_dict.keys())[-1]

        # 检查最低等级
        min_level = 0
        if config.has_option('validation', 'min_level'):
            min_level = config.getint('validation', 'min_level')
        if min_level != 0 and floor.level < min_level:
            msg = '等级低于%d级' % min_level
        else:
            # 检查内容
            content = floor.content
            regex = None
            if config.has_option('validation', 'content_validation_regex'):
                regex = config.get('validation', 'content_validation_regex')
                if regex != '':
                    regex = re.compile(regex)
            if regex is not None and regex != '' and regex.search(content) is None:
                msg = '回复内容无效'
            else:
                # 检查连续刷楼
                max_continuous_floor = 0
                if config.has_option('validation', 'max_continuous_floor'):
                    max_continuous_floor = config.getint('validation', 'max_continuous_floor')
                if max_continuous_floor != 0:

                    name = floor.name
                    floor_no = floor.floor_no
                    start_floor = floor_no
                    while name == floor.name:
                        start_floor = floor_no
                        floor_no -= 1
                        while floor_no not in floor_dict.keys() and floor_no > 0:
                            # 如果楼层不存在（可能被楼主删除），继续下移
                            floor_no -= 1
                            start_floor -= 1
                        name = floor_dict[floor_no].name

                    name = floor.name
                    floor_no = floor.floor_no
                    end_floor = floor_no

                    while name == floor.name:
                        end_floor = floor_no
                        floor_no += 1
                        while floor_no not in floor_dict.keys() and floor_no <= max_floor:
                            # 如果楼层不存在（可能被楼主删除），继续上移
                            floor_no += 1
                            start_floor += 1
                        name = floor_dict[floor_no].name
                    floor.floor_range = '%d-%d' % (start_floor, end_floor)
                    if end_floor - start_floor + 1 > max_continuous_floor:
                        msg = '刷楼%d-%d，超过%d层' % (start_floor, end_floor, max_continuous_floor)

        if msg is None:
            # 没有错误信息，校验通过
            floor.gift_validation = '获奖,%d层的礼物' % gift_floor
            floor.gift = gift_name
            return
        floor.gift_validation = msg
        next_floor += 1
        # 有可能下一楼层不存在，进行查找
        while next_floor not in floor_dict.keys() and next_floor <= max_floor:
            next_floor += 1
        if next_floor > max_floor:
            # 超限
            return
        # 这里还可以校验最多顺延多少层
        return next_floor

    @staticmethod
    def write_to_excel(result_file, excel_file=None):
        """
        写入excel
        :param result_file: 
        :param excel_file: 
        :return: 
        """
        if excel_file is None:
            excel_file = filex.get_result_file_name(result_file, '', 'xls')
        lines = filex.read_lines(result_file, ignore_line_separator=True)
        if lines is None:
            return
        excelx.write_list_to_excel(excel_file, lines, title=Floor.get_excel_title())


class Floor:
    """
    楼层对象
    """

    def __init__(self, floor_no, name, level, content):
        """

        :param floor_no: 楼层
        :param name: 用户id
        :param level: 用户等级
        :param content: 回复内容
        """
        self.floor_no = int(floor_no)
        self.name = name
        self.level = int(level)
        self.content = content
        if self.content == '':
            # 可能是纯表情之类的
            self.content = '<无内容>'
        self.floor_count = 0
        self.floor_range = ''
        self.gift_name = ''
        self.gift_validation = ''
        self.gift = ''

    def __str__(self):
        return '%d|%s|%d|%s' % (self.floor_no, self.name, self.level, self.content)

    @staticmethod
    def from_str(string):
        """
        从字符中解析出楼层
        :param string: 
        :return: 
        """
        data = string.split('|')
        return Floor(int(data[0]), data[1], int(data[2]), data[3])

    def to_excel_string(self):
        """
        excel要保存的数据
        :return: 
        """
        return '%d|%s|%s|%s|%s|%d|%s|%s' % (
            self.floor_no, self.gift_name, self.gift_validation, self.gift, self.name, self.level, self.floor_range,
            self.content)

    @staticmethod
    def get_excel_title():
        """
        excel中的标题
        :return: 
        """
        return ['楼层', '楼层奖品', '奖品校验', '最终奖品', 'ID', '等级', '刷楼范围', '回复内容']


if __name__ == '__main__':
    TiebaFloor('data/gift.cfg').main()
