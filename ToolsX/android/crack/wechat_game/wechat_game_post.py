import base64
import json

import requests
from Crypto.Cipher import AES

from xx import iox


class WechatGamePost:
    """
    微信跳一跳游戏，直接发包
    来自 [麦文俊《微信跳一跳万分攻(作)略(弊)》](https://zhuanlan.zhihu.com/p/32473340)
    """

    def __init__(self, session_id):
        self.session_id = session_id
        self.times = 0

    def main(self):
        action_list = [
            ['退出', exit],
            ['获取排行榜', self.get_friends_score],
            ['结算成绩', self.settlement],
            ['上报数据', self.report],
            ['解包数据测试', self.unpack_test]
        ]
        while True:
            iox.choose_action(action_list)

    def unpack_test(self):
        action_data = r''
        ciphertext = base64.b64decode(action_data)
        print(ciphertext)

        aes_key = self.session_id[0:16]
        aes_iv = aes_key
        cryptor = AES.new(aes_key, AES.MODE_CBC, aes_iv)

        json_str = cryptor.decrypt(ciphertext)
        print(json_str)
        json_str = json_str.decode('utf-8')
        print(json_str)

    def get_friends_score(self):
        """获取排行榜"""
        url = 'https://mp.weixin.qq.com/wxagame/wxagame_getfriendsscore'
        result = self.post(url)
        print('result is %s' % result)

        # 我的信息
        my_user_info = MyUserInfo()
        my_user_info.__dict__ = result['my_user_info']
        print(my_user_info)
        self.times = my_user_info.times

        # 好友列表
        user_info_list = result['user_info']
        # 排序
        user_info_list = sorted(user_info_list, key=lambda x: x['week_best_score'], reverse=True)
        for user_info_dict in user_info_list:
            user_info = UserInfo()
            user_info.__dict__ = user_info_dict
            print(user_info)

    def settlement(self):
        """结算成绩"""
        if self.times == 0:
            print('没有次数，请选获取')
            return
        score = input('请输入成绩\n')
        if not score:
            print('没有输入成绩')
            return

        url = 'https://mp.weixin.qq.com/wxagame/wxagame_settlement'

        # 次数加 1
        # self.times += 1
        action_data = {
            "score": score,
            "times": self.times,
            "game_data": {}
        }

        aes_key = self.session_id[0:16]
        aes_iv = aes_key

        cryptor = AES.new(aes_key, AES.MODE_CBC, aes_iv)
        str_action_data = json.dumps(action_data).encode("utf-8")
        print("json_str_action_data ", str_action_data)
        # Pkcs7
        length = 16 - (len(str_action_data) % 16)
        str_action_data += bytes([length]) * length
        cipher_action_data = base64.b64encode(cryptor.encrypt(str_action_data)).decode("utf-8")
        data = {'action_data': cipher_action_data}
        result = self.post(url, data)
        print(result)

    def report(self):
        """上报数据"""
        report_list = []
        url = 'https://mp.weixin.qq.com/wxagame/wxagame_bottlereport'
        data = {'report_list': report_list}
        result = self.post(url, data, True)
        print(result)

    def post(self, url, data=None, add_client_info=False):
        """发包

        :param url:地址
        :param data:数据，添加到 base_req 中
        :param add_client_info: 是否添加，只有上报数据时需要
        :return:
        """

        post_data = {
            "base_req": {
                "session_id": self.session_id,
                "fast": 1,
            }
        }
        if add_client_info:
            post_data['base_req']['cliend_info'] = {
                "platform": "android",
                "brand": "Xiaomi",
                "model": "MI 5",
                "system": "Android 7.0"
            }
        if data:
            post_data.update(data)
        print('post to %s' % url)
        print(post_data)

        response = requests.post(url, json=post_data)
        return response.json()


class UserInfo:
    def __init__(self):
        self.headimg = None
        self.nickname = None
        self.score_info = None
        self.grade = None
        self.hongbao_list = None
        self.week_best_score = None

    def __str__(self):
        return '%s,周最高 %d,级别 %d' % (self.nickname, self.week_best_score, self.grade)


class MyUserInfo(UserInfo):
    def __init__(self):
        super().__init__()
        self.times = None
        self.history_best_score = None

    def __str__(self):
        if 'week_best_score' not in self.__dict__:
            self.week_best_score = 0
        return '%s,%d 次,最高 %d,周最高 %d,级别 %d' % (
            self.nickname, self.times, self.history_best_score, self.week_best_score, self.grade)


class Report:
    """报告"""

    def __init__(self):
        self.ts = 0
        """时间"""

        self.type = 0
        """类型
        
        0 可能是开始游戏
        1 不知道
        2 是游戏结果
        10 再玩一局
        
        {
            "ts": 1514728963,
            "type": 0,
            "scene": 1089
        },
        {
            "ts": 1514728969,
            "type": 1,
            "duration": 6
        },
        {
            "ts": 1514729045,
            "type": 2,
            "score": 2,
            "best_score": 500,
            "break_record": 0,
            "duration": 6,
            "times": 129
        },
        {
            "ts": 1514729052,
            "type": 10
        },
        """

        self.score = 0
        self.best_score = 0
        self.break_record = 0
        self.duration = 0
        self.times = 0


if __name__ == '__main__':
    with open('session_id.txt') as file:
        saved_session_id = file.readline()
    if saved_session_id:
        WechatGamePost(saved_session_id).main()
    else:
        print('session_id.txt 不存在或无内容')
