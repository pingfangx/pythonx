import json
import os
import queue
import sys
import time
import zipfile
from http.server import SimpleHTTPRequestHandler, HTTPServer

import requests

# from xx import excelx, filex
from xx import iox
from xx import netx
from xx import threadx


class Room:

    def __init__(self):
        pass

    def get_title_keys(self):
        """
        此列表中包含的 key 将会读取 Room 类中的属性值作为标题，不包含的直接使用属性名
        排序时按此列表中的顺序优先展示属性，不包含的按字母顺序
        """
        return []

    def get_keys(self):
        """
        按此 key 顺序显示值
        此处直接 sorted,也可以手动指定顺序
        """
        keys = []
        keys.extend(self.get_title_keys())
        for k in sorted(self.get_type().__dict__.keys()):
            if k not in keys:
                keys.append(k)
        return keys

    def get_title(self):
        """获取标题"""
        "如果 key 在此列表中,则表 room 类该 key 对应的值"
        title = self.get_keys()
        room = self.get_type()
        for i in range(len(title)):
            key = title[i]
            if key in self.get_title_keys():
                title[i] = room.__dict__[key]
        return title

    def sort_value(self, room):
        """
        将对象中的值排序
        """
        # return [str(data[key]) for key in Room.get_keys()]
        result = []
        for key in self.get_keys():
            value = str(room.__dict__[key])
            if key == 'area_display':
                # 面积将 约 去掉,方便排序
                value = value.lstrip('约')
            elif key == 'url':
                value = value.lstrip('/')
            result.append(value)
        return result

    def get_type(self):
        return Room()

    def filter_room(self, room):
        """过滤房源"""
        return True

    def export_rooms_to_excel(self, excel_file_path, rooms):
        """写入 excel ,不过滤数据,如果需要,请提前过滤数据"""
        if rooms:
            print('准备写入 excel,共 %d 条数据' % len(rooms))
            # 标题
            # data = [self.get_title()]
            # for value in rooms.values():
            #     data.append(self.sort_value(value))
            # if os.path.exists(excel_file_path):
            #     os.remove(excel_file_path)
            # filex.check_and_create_dir(excel_file_path)
            # excelx.write_list_to_excel(excel_file_path, data)


class MapRoom(Room):
    """根据地图 api 获取的"""

    def __init__(self):
        super().__init__()

        self.area_display = '面积'
        self.balcony_exist = 0  # 阳台
        self.bizcircle_code = ['611100400', '611100710']
        self.bizcircle_display = '商圈'
        self.bizcircle_name = ['门头沟其它', '城子']
        self.build_end_year = '2004'
        self.build_size = 99.53
        self.city_code = '110000'
        self.district_code = '23008620'  # 区域
        self.district_name = '门头沟'  # 区域
        self.facing = '朝向'
        self.first_figure = 'g2/M00/D1/DA/ChAFD1o7xhiAHB8iAAEEgVPkiS8271.jpg'
        self.floor = '5'  # 楼层
        self.floor_total = '7'  # 楼层
        self.garder_exist = 0  # 衣柜
        self.house_bedroom = '几室'
        self.house_code = 'BJZRGY0817152867'
        self.house_company = '每月'
        self.house_empty_count = '空室'
        self.house_facing = '东西'
        self.house_parlor = 1  # 客厅
        self.hx_photo = 'g2/M00/D1/E0/ChAFD1o7zUKAQhEzAAQ8G4mVCb4511.jpg'
        self.id = '60900114'
        self.index_no = 1
        self.is_ai_lock = '智能锁'  # 智能锁
        self.is_duanzu = 0  # 短租
        self.is_new = '新'
        self.is_reserve = 0  # 转租
        self.is_whole = 0  # 整合
        self.latitude = 39.95269
        self.longitude = 116.112665
        self.name = '友家 · 阁外山水3居室-东卧'
        self.payment_type = 1  # 付款类型
        self.photo = '照片'
        self.photo_webp = 'webp'
        self.resblock_id = '1111027374736'
        self.resblock_name = '阁外山水'
        self.room_code = 'BJZRGY0817152867_01'
        self.room_name = '门头沟门头沟其它阁外山水3居室-东卧'
        self.room_photos = ['g2/M00/D1/DA/ChAFD1o7xhiAHB8iAAEEgVPkiS8271.jpg',
                            'g2/M00/D1/DF/ChAFfVo7xwyAVRtUAAU-mN9V0Mk909.jpg',
                            'g2/M00/D1/DF/ChAFfVo7xwiAU5BMAAUEecGEnCY444.jpg']
        self.room_status = '状态'
        """
        dzz 待出租
        tzpzz 
        zxpzz
        yxd 已下订
        ycz 已出租
        """

        self.room_type_code = '308600000001'
        self.sell_price = '价格'
        self.sell_price_day = 0
        self.sell_price_duanzu = 0
        self.style_code = 97001001  # 风格
        self.style_tag = {'name': '友家4.0 拿铁', 'url': 'http://www.ziroom.com/zhuanti/youjia_fbh/'}
        self.sublet_attestation = 0  # 转租证明
        self.subway = '地铁'
        self.subway_display = '地铁'
        self.subway_line_code = []  # 地铁线
        self.subway_station_code = []  # 地铁
        self.subway_tag = []  # 地铁
        self.supply_heat = '2030001'  # 供暖
        """
        独立  2030001
        集体  2030002
        避挂炉 2030005
        """
        self.toliet_exist = 0  # 卫生间
        self.type_text = '合整'  # 类型
        self.url = 'url'  # 地址
        self.usage_area = 13.6  # 使用面积
        self.walking_distance_dt = []  # 走路距离
        self.ziroom_version_id = 1008  # 版本

    def get_type(self):
        return MapRoom()

    def get_title_keys(self):
        return [
            'type_text',
            'room_status',
            'area_display',
            'sell_price',
            'subway',
            'subway_display',
            'facing',
            'house_bedroom',
            'house_empty_count',
            'url',
            'is_new',
            'is_ai_lock',
        ]

    def filter_room(self, room):
        """过滤房源"""
        if room.room_status in ['yxd', 'ycz']:
            return False
        return True


class SubwayRoom(Room):
    """监控出的房源，字段有一些不一样，于是重写"""

    def __init__(self):
        super().__init__()
        self.read = '处理'
        self.comment = '注释'
        self.url = '地址'

        self.area = '面积'
        self.bedroom = 4
        self.code = 'BJZRCP73505292_05'
        self.face = '朝向'
        self.floor = '5'
        self.floor_total = '6'
        self.house_code = 'BJZRCP73505292'
        self.house_id = '60004888'
        self.id = '60028030'
        self.lat = 40.088456
        self.lng = 116.367231
        self.name = '和谐家园二区4居室-南卧'
        self.parlor = 1
        self.photo = ''
        self.photo_min = ''
        self.photo_min_webp = ''
        self.photo_webp = ''
        self.price = '价格'
        self.price_unit = '元/月'
        self.resblock_id = '1111027375383'
        self.resblock_name = '和谐家园二区'
        self.status = '状态'
        self.subway_station_info = '距8号线回龙观东大街站230米'
        self.tags = [{'title': '自如客转租'}, {'title': '独立供暖'}, {'title': '木棉4.0'}]
        self.turn = 1
        self.type = 1
        self.type_text = '类型'
        self.will_unrent_date = '20180308'

    def get_type(self):
        return SubwayRoom()

    def get_title_keys(self):
        return [
            'read',
            'comment',
            'type_text',
            'status',
            'area',
            'price',
            'face',
            'url',
        ]

    def filter_room(self, room):
        """过滤房源"""
        if room.status in ['yxd', 'ycz']:
            return False
        # 面积
        area = room.area
        area = area.replace('约', '')
        area = float(area)
        if area < 18:
            return False

        # 不要 5 居及以上
        if int(room.bedroom) > 4:
            return False
        return True


class SubwayRoomMonitor:
    """房源监控"""

    def __init__(self, delay_time=60):
        self.delay_time = delay_time
        self.excel_file_path = 'ignore/monitor_rooms.xls'
        self.excel_bak_file_path = 'ignore/monitor_rooms.bak.xls'
        self.url = 'https://phoenix.ziroom.com/v7/room/list.json'
        subway_dict = {
            '10号线': '北土城 安贞门 惠新西街南口 芍药居 太阳宫 三元桥',
            '5号线': '天通苑北 天通苑 天通苑南 立水桥 立水桥南 北苑路北 大屯路东 惠新西街北口 惠新西街南口',
            '8号线': '朱辛庄 育知路 平西府 回龙观东大街 霍营 育新 西小口 永泰庄 林萃桥 森林公园南门 奥林匹克公园 奥体中心 北土城',
            '13号线': '霍营 立水桥 北苑 望京西 芍药居'
        }
        "相关地铁站，这些地铁站直接从自如网页复制过来，就直接带空格了"
        self.subway_list = []
        for subway_line, value in subway_dict.items():
            for subway_name in reversed(value.split(' ')):
                self.subway_list.append((subway_line, subway_name))

        self.params = netx.parse_params_from_file('ziroom_params.txt')
        "请求参数，抓包的时候包含一些敏信息，测试发现只保留关键参数即可"

        self.all_rooms = {}
        self.pre_all_rooms = {}

    def get_subway_queue(self):
        q = queue.Queue()
        for subway in self.subway_list:
            q.put(subway)
        return q

    def run(self):
        """"""
        scan_times = 0
        while True:
            self.pre_all_rooms = self.read_all_rooms_from_excel()
            print('之前有记录 %d 条' % len(self.pre_all_rooms))
            scan_times += 1
            q = self.get_subway_queue()
            print()
            print('第 %d 轮扫描，共有 %d 个站点' % (scan_times, q.qsize()))
            self.all_rooms.clear()
            multi_thread = threadx.HandleQueueMultiThread(q, self.get_rooms, thread_num=10, print_before_task=True)
            multi_thread.start()
            print('任务结束，本轮共获得 %d 个房源' % len(self.all_rooms))
            monitor_room = SubwayRoom()
            valid_rooms = {}
            for key, room in self.all_rooms.items():
                if monitor_room.filter_room(room):
                    valid_rooms[key] = room
            self.all_rooms = valid_rooms
            print('其中 %d 套有效' % (len(self.all_rooms)))
            self.compare_rooms()

            # 延时
            for i in range(self.delay_time):
                sys.stdout.write('\r %d 秒后执行第 %d 轮扫描 ' % (self.delay_time - i, scan_times + 1))
                sys.stdout.flush()
                time.sleep(1)

    def read_all_rooms_from_excel(self):
        """从 excel 中读取"""
        result = {}
        # data = excelx.read_from_excel(self.excel_file_path)
        # keys = SubwayRoom().get_keys()
        # for row in data:
        #     monitor_room = SubwayRoom()
        #     for i in range(len(keys)):
        #         monitor_room.__dict__[keys[i]] = row[i]
        #     if monitor_room.id != 'id':
        #         result[monitor_room.id] = monitor_room
        return result

    def compare_rooms(self):
        """比校扫描的结果"""
        print('比较房源，上一次共有 %d 套房源，该次共有 %d 套' % (len(self.pre_all_rooms), len(self.all_rooms)))
        all_keys = self.pre_all_rooms.keys()
        append_num = 0
        for key, room in self.all_rooms.items():
            room.url = 'http://www.ziroom.com/z/vr/%s.html' % room.id
            if key in all_keys:
                # 已存在，读取之前的
                room.read = self.pre_all_rooms[key].read
                room.comment = self.pre_all_rooms[key].comment
                # 将其删除
                self.pre_all_rooms.pop(key)
            else:
                append_num += 1
                room.read = 0
                room.comment = '新添加'
        # 执行完循环后，剩余的表示该轮没有扫描出来
        for key, room in self.pre_all_rooms.items():
            room.read = 10
            if '已消失' not in room.comment:
                room.comment = '已消失' + room.comment
            self.all_rooms[key] = room

        self.pre_all_rooms = self.all_rooms
        print('本轮共添加 %d 个新房源' % append_num)
        if append_num > 0:
            self.notice(append_num)
        # 保存两个文件，一个方便阅读
        print()
        SubwayRoom().export_rooms_to_excel(self.excel_file_path, self.pre_all_rooms)
        try:
            SubwayRoom().export_rooms_to_excel(self.excel_bak_file_path, self.pre_all_rooms)
        except:
            pass

    def notice(self, append_num):
        """添加房源，给通知"""
        print('通知：添加了 %d 处房源' % append_num)
        # TODO 这里可以提醒

    def get_rooms(self, element, element_index, thread_id):
        # 新建一个字典，用于多线程处理（不知道是否必要）
        params = {}
        params.update(self.params)
        params['timestamp'] = '%d' % time.time()
        params['subway_code'] = element[0]
        params['subway_station_code'] = element[1]

        result = requests.get(self.url, params).json()
        print(result)
        if result['status'] == 'success':
            rooms = result['data']['rooms']
            for room_data in rooms:
                room = SubwayRoom()
                room.__dict__ = room_data
                self.all_rooms[room.id] = room
            print('线程 %d 第 %d 个任务,获取到 %d 个房源' % (thread_id, element_index, len(rooms)))


class RoomStatusMonitor:
    """房源状态监控"""

    def __init__(self, room_id, city_code='110000'):
        self.room_id = room_id
        self.city_code = city_code

    def run(self):
        """运行"""
        url = 'https://phoenix.ziroom.com/v7/room/detail.json'
        params = {
            'id': self.room_id,
            'city_code': self.city_code
        }
        params = netx.parse_params("""
house_id	60163300
sign	3819b75389894cc18418b81e882d560a
size	4
timestamp	1520072313
os	android:7.0
network	WIFI
sign_open	1
app_version	5.5.0
imei	868030026509339
id	61015398
ip	192.168.199.128
uid	0
city_code	110000
page	1
model	MI 5
        """)
        print(url)
        print(params)
        while True:
            result = netx.get(url, params, result_type='json', need_print=False)
            if result['status'] == 'success':
                data = result['data']
            print(result)
            return


class ZiroomTools:
    """自如找房的工具"""

    def main(self):
        zip_file_path1 = r'D:\workspace\github\ziroom_spider\web\all_rooms-2018-02-27-115445.zip'
        zip_file_path2 = r'D:\workspace\github\ziroom_spider\web\all_rooms-2018-02-27-193757.zip'
        web_dir = r'D:\workspace\github\ziroom_spider\web'
        action_list = [
            ['退出', exit],
            ['输出为 excel', self.export_file_to_excel, zip_file_path1],
            ['比较两处房源', self.compare_rooms, zip_file_path1, zip_file_path2],
            ['输出为展示网页用的 zip', self.export_to_share_and_whole_rooms, 'new_rooms.zip', web_dir],
            ['启动 web 服务', self.start_web_server, web_dir],
            ['监控地铁区域房源', self.monitor_subway_room],
            ['监控房源状态', self.monitor_room_status, '61015398']
        ]
        iox.choose_action(action_list)

    def export_file_to_excel(self, file_path):
        rooms = self.load_rooms(file_path)
        if rooms:
            MapRoom().export_rooms_to_excel('ignore/all_rooms.xls', rooms)

    def compare_rooms(self, file_path1, file_path2):
        """比较房源"""
        print('比较房源 %s 与 %s' % (os.path.basename(file_path1), os.path.basename(file_path2)))
        rooms1 = self.load_rooms(file_path1)
        rooms2 = self.load_rooms(file_path2)
        delta_num = len(rooms1) - len(rooms2)
        print('房源 %d → %d %s 了 %d 处' % (len(rooms1), len(rooms2), '减少' if delta_num > 0 else '增加', delta_num))

        keys1 = rooms1.keys()
        new_rooms = {}
        for k, v in rooms2.items():
            if k not in keys1:
                new_rooms[k] = v
        print('共计新增加 %d 处房源，即减少 %d 房源' % (len(new_rooms), delta_num - len(new_rooms)))
        print('输出新添加的房源')
        MapRoom().export_rooms_to_excel('new_rooms.xls', new_rooms)
        with zipfile.ZipFile('new_rooms.zip', 'w', zipfile.ZIP_DEFLATED) as f:
            f.writestr('all_rooms.json', json.dumps(new_rooms))
        print('保存完成')

    def export_to_share_and_whole_rooms(self, file_path, output_dir):
        """将所有的房间分为合租、整租，输出到不同的 zip"""
        all_rooms = self.load_rooms(file_path)

        available_rooms = list(
            filter(lambda x: x["room_status"] != "ycz" and x["room_status"] != "yxd", all_rooms.values()))
        share_rooms = list(filter(lambda x: x["is_whole"] == 0, available_rooms))
        whole_rooms = list(filter(lambda x: x["is_whole"] == 1, available_rooms))

        print('保存中')
        with zipfile.ZipFile('%s/share_rooms.zip' % output_dir, 'w', zipfile.ZIP_DEFLATED) as f:
            f.writestr('share_rooms.json', json.dumps(share_rooms))
        with zipfile.ZipFile('%s/whole_rooms.zip' % output_dir, 'w', zipfile.ZIP_DEFLATED) as f:
            f.writestr('whole_rooms.json', json.dumps(whole_rooms))
        print('保存完成')

    @staticmethod
    def start_web_server(web_dir):
        os.chdir(web_dir)
        port = 8000
        print('starting server, port', port)
        server_address = ('', port)
        httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
        print('running server...')
        httpd.serve_forever()

    @staticmethod
    def load_rooms(file_path):
        with zipfile.ZipFile(file_path) as zip_file:
            json_file_path = 'all_rooms.json'
            if json_file_path in zip_file.namelist():
                obj = json.loads(zip_file.read(json_file_path).decode())
                return obj
        return None

    @staticmethod
    def monitor_subway_room():
        SubwayRoomMonitor(600).run()

    def monitor_room_status(self, room_id):
        """监控房源状态"""
        RoomStatusMonitor(room_id).run()


if __name__ == '__main__':
    ZiroomTools().main()
