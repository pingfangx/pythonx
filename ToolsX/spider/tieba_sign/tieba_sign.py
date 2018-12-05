#!/usr/bin/env python3
# 因为要运行在云主机上，装了两个版本的 python，指定 python3

import configparser
import logging
import os
import time

import pytz
import requests
from apscheduler.schedulers.blocking import BlockingScheduler


class TiebaSign:
    """贴吧签到"""

    def __init__(self):
        self.config_file = 'ignore/sign.conf'
        self.log_file = 'ignore/sign.log'
        self.lock_file = 'ignore/sign.lock'

        self.logger: logging = None
        self.scheduler: BlockingScheduler = None

        self.sign_url = ''
        """签到地址"""

        self.sign_hour = ''
        """签到触发小时，用于配置 add_job cron 对应的 hour 参数"""

    def init_logger(self):
        if self.logger is None:
            self.logger = self.get_logger(self.log_file)

    @staticmethod
    def get_logger(file):
        file_handler = logging.FileHandler(file, encoding='utf-8')

        fmt = '%(asctime)s %(message)s'
        date_fmt = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(fmt=fmt, datefmt=date_fmt)
        file_handler.setFormatter(formatter)

        logger = logging.getLogger('sign')
        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)
        return logger

    def init_config(self):
        """初始化配置"""
        config = configparser.ConfigParser()
        config.read(self.config_file)
        if 'sign' in config:
            sign = config['sign']
            if 'sign_url' in sign:
                self.sign_url = sign['sign_url']
            if 'sign_hour' in sign:
                self.sign_hour = sign['sign_hour']

    def check_lock(self):
        """
        检查锁
        如果存在，更新时间
        如果不存在，停止任务
        """
        if os.path.exists(self.lock_file):
            self.write_lock()
        else:
            # 文件不存在，停止程序
            if self.scheduler is not None:
                self.scheduler.shutdown(wait=False)
                self.log(f'{self.lock_file} 不存在，停止任务')
                exit(1)

    def write_lock(self):
        """更新锁文件记录的时间"""
        with open(self.lock_file, 'w') as f:
            message = time.strftime('Now is %Y%m%d %H:%M:%S %z.')
            if self.scheduler:
                jobs = self.scheduler.get_jobs()
                if jobs:
                    for job in jobs:
                        message += f'\n{job}'
            f.write(message)

    def sign(self):
        """签到"""
        try:
            result = requests.get(self.sign_url)
            result = result.json()
            sign_message = self.get_sign_message(result)
            if sign_message:
                self.log('请求结果:' + sign_message)
            else:
                self.log('请求结果:' + str(result))
        except Exception as e:
            self.log('请求出错了:' + str(e))

    @staticmethod
    def get_sign_message(result):
        """
        获取返回结果的签到信息
        用于减少 log 字数
        """
        if result and isinstance(result, dict):
            if 'code' not in result.keys():
                return ''
            if result['code'] != 200:
                return ''
            if 'data' not in result.keys():
                return ''
            data = result['data']
            if data and isinstance(data, dict):
                if 'signMessage' in data.keys():
                    return data['signMessage']

    def start(self):
        """启动"""
        self.init_logger()
        self.init_config()
        if not self.sign_url:
            self.log(f'未在 {self.config_file} 中 [sign] 内配置 sign_url')
            exit(1)
        if not self.sign_hour:
            self.log(f'未在 {self.config_file} 中 [sign] 内配置 sign_hour')
            exit(1)
        # 首次写入锁
        self.write_lock()

        # 服务器上时区不一致，手动指定
        timezone = pytz.timezone('Asia/Shanghai')
        self.scheduler = BlockingScheduler(timezone=timezone)
        # 每分钟触发一次
        self.scheduler.add_job(self.check_lock, trigger='cron', second='0')
        # 早 6 点一次，晚 10 点一次
        self.scheduler.add_job(self.sign, trigger='cron', hour=self.sign_hour)
        self.scheduler._logger = self.logger
        self.log('开始运行')
        try:
            self.scheduler.start()
        except KeyboardInterrupt:
            self.log('按键中断')
        except SystemExit:
            self.log('异常退出')

    def log(self, text):
        now = time.strftime('%Y%m%d %H:%M:%S %z')
        print(f'[{now}] {text}')
        self.logger.info(text)


if __name__ == '__main__':
    TiebaSign().start()
