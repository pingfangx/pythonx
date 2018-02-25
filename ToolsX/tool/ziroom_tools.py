import json
import os
import zipfile
from http.server import SimpleHTTPRequestHandler, HTTPServer

from xx import excelx
from xx import iox


class Room:
    title_keys = [
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
    """
    此列表中包含的 key 将会读取 Room 类中的属性值作为标题，不包含的直接使用属性名
    排序时按此列表中的顺序优先展示属性，不包含的按字母顺序
    """

    def __init__(self):
        self.area_display = '面积'
        self.balcony_exist = 0
        self.bizcircle_code = ['611100400', '611100710']
        self.bizcircle_display = '门头沟其它'
        self.bizcircle_name = ['门头沟其它', '城子']
        self.build_end_year = '2004'
        self.build_size = 99.53
        self.city_code = '110000'
        self.district_code = '23008620'
        self.district_name = '门头沟'
        self.facing = '朝向'
        self.first_figure = 'g2/M00/D1/DA/ChAFD1o7xhiAHB8iAAEEgVPkiS8271.jpg'
        self.floor = '5'
        self.floor_total = '7'
        self.garder_exist = 0
        self.house_bedroom = '几室'
        self.house_code = 'BJZRGY0817152867'
        self.house_company = '每月'
        self.house_empty_count = '空室'
        self.house_facing = '东西'
        self.house_parlor = 1
        self.hx_photo = 'g2/M00/D1/E0/ChAFD1o7zUKAQhEzAAQ8G4mVCb4511.jpg'
        self.id = '60900114'
        self.index_no = 1
        self.is_ai_lock = '智能锁'
        self.is_duanzu = 0
        self.is_new = '新'
        self.is_reserve = 0
        self.is_whole = 0
        self.latitude = 39.95269
        self.longitude = 116.112665
        self.name = '友家 · 阁外山水3居室-东卧'
        self.payment_type = 1
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
        self.style_code = 97001001
        self.style_tag = {'name': '友家4.0 拿铁', 'url': 'http://www.ziroom.com/zhuanti/youjia_fbh/'}
        self.sublet_attestation = 0
        self.subway = '地铁'
        self.subway_display = '地铁'
        self.subway_line_code = []
        self.subway_station_code = []
        self.subway_tag = []
        self.supply_heat = '2030001'
        self.toliet_exist = 0
        self.type_text = '合整'
        self.url = 'url'
        self.usage_area = 13.6
        self.walking_distance_dt = []
        self.ziroom_version_id = 1008

    @staticmethod
    def get_keys():
        """
        按此 key 顺序显示值
        此处直接 sorted,也可以手动指定顺序
        """
        keys = []
        keys.extend(Room.title_keys)
        for k in Room().__dict__.keys():
            if k not in keys:
                keys.append(k)
        return keys

    @staticmethod
    def get_title():
        """获取标题"""
        "如果 key 在此列表中,则表 room 类该 key 对应的值"
        title = Room.get_keys()
        room = Room()
        for i in range(len(title)):
            key = title[i]
            if key in Room.title_keys:
                title[i] = room.__dict__[key]
        return title

    @staticmethod
    def sort_value(data):
        """
        将对象中的值排序
        """
        # return [str(data[key]) for key in Room.get_keys()]
        result = []
        for key in Room.get_keys():
            value = str(data[key])
            if key == 'area_display':
                # 面积将 约 去掉,方便排序
                value = value.lstrip('约')
            elif key == 'url':
                value = value.lstrip('/')
            result.append(value)
        return result


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
            ['启动 web 服务', self.start_web_server, web_dir]
        ]
        iox.choose_action(action_list)

    @staticmethod
    def filter_room(data):
        """过滤房源"""
        room = Room()
        room.__dict__ = data
        if room.room_status in ['yxd', 'ycz']:
            return False
        return True

    def export_file_to_excel(self, file_path):
        rooms = self.load_rooms(file_path)
        if rooms:
            self.export_rooms_to_excel('all_rooms.xls', rooms)

    def export_rooms_to_excel(self, excel_file_path, rooms):
        if rooms:
            print('共 %d 条数据' % len(rooms))
            # 标题
            data = [Room.get_title()]
            for value in rooms.values():
                if self.filter_room(value):
                    data.append(Room.sort_value(value))
            print('开始写入，共 %d 条数据' % len(data))
            if os.path.exists(excel_file_path):
                os.remove(excel_file_path)
            excelx.write_list_to_excel(excel_file_path, data)

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
        self.export_rooms_to_excel('new_rooms.xls', new_rooms)
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


if __name__ == '__main__':
    ZiroomTools().main()
