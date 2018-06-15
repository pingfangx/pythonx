import json
import time

import scrapy
from scrapy_spider.common.log import log
from scrapy_spider.items import AwemeItem
from scrapy_spider.spiders.ignore.douyin_encypt import DouyinEncrypt  # 不公开


class DouyinSpider(scrapy.Spider):
    """
    来自 https://github.com/a232319779/appspider
    感谢
    """
    name = 'douyin'

    douyin_encrypt = DouyinEncrypt()
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; MI 4S Build/LMY47V) AppleWebKit/537.36 ('
                      'KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 '
                      'XiaoMi/MiuiBrowser/9.1.3',
    }
    feed_url = 'http://aweme.snssdk.com/aweme/v1/feed/?aid=1128&count=20'
    has_more = 1
    exit_code = 1
    total_items = 0

    sleep_time = 1

    def start_requests(self):
        i = 0
        while i < 1:
            # i += 1
            print(f'sleep {self.sleep_time}')
            time.sleep(self.sleep_time)
            self.sleep_time = 1
            now = int(time.time())
            # 并发的时候，time 是相同的，被 scrapy 认为是相同地址而忽略
            url = self.douyin_encrypt.cal_url(now, self.feed_url)
            log.info("crawl " + url)
            yield scrapy.Request(url=url, headers=self.headers)
            if self.has_more == 0 or self.exit_code == 0:
                break

    def parse(self, response):
        try:
            result = json.loads(response.body.decode())
            status_code = result['status_code']
            if result['status_code'] == 0:
                self.has_more = result['has_more']
                aweme_list = result['aweme_list']
                self.total_items += len(aweme_list)
                log.info(f'scraped {len(aweme_list)}/{self.total_items} items')
                for aweme in aweme_list:
                    item = AwemeItem(aweme)
                    yield item
            elif status_code == 2145:
                log.warning('请求已过期')
                self.exit_code = 0
            elif status_code == 2151:
                log.warning('签名错误')
                self.exit_code = 0
            elif status_code == 2154:
                # 大约会被禁 1 个小时
                log.warning('请求太频繁，设备被禁')
                log.warning('休息 10 分钟')
                self.sleep_time = 10 * 60
                # self.exit_code = 0
            else:
                log.warning('错误码 %d' % status_code)
                log.warning(response.body.decode())
                self.exit_code = 0
        except Exception as e:
            log.error('出错了')
            log.error(repr(e))
