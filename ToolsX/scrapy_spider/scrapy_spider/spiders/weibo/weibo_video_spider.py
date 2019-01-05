import urllib.parse

import scrapy
from bs4 import BeautifulSoup

from scrapy_spider.common.log import log
from scrapy_spider.spiders.weibo.items import WeiboVideoItem


class WeiboVideoSpider(scrapy.Spider):
    name = 'weibo_video'
    max_page = 50
    """最大页数"""

    keyword_list = [
        '测试',
    ]
    keyword = ''
    """搜索关键字"""

    start_urls = [
        'https://s.weibo.com/weibo?q={keyword}&typeall=1&hasvideo=1&Refer=g&page={page}',
        'https://s.weibo.com/weibo?q={keyword}&xsort=hot&hasvideo=1&Refer=g&page={page}',
    ]

    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 1,
        'ITEM_PIPELINES': {
            'scrapy_spider.spiders.weibo.pipelines.WeiboVideoPostgreSQLPipeline': 300,
        },
    }

    def start_requests(self):
        if not self.max_page:
            self.max_page = 1

        keyword_length = len(self.keyword_list)
        for i in range(keyword_length):
            self.keyword = self.keyword_list[i]
            page = 0
            while page < self.max_page:
                page += 1
                url_length = len(self.start_urls)
                for j in range(url_length):
                    url = self.start_urls[j]
                    url = url.format(keyword=urllib.parse.quote(self.keyword), page=page)
                    log.info(f'爬取关键字{i + 1}/{keyword_length},地址{j + 1}/{url_length},页数{page}/{self.max_page},'
                             f'{url}')
                    yield scrapy.Request(url=url)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        card_list = soup.find_all('div', class_='card-wrap')
        count = 0
        for card in card_list:
            content = card.select_one('div.content')
            if not content:
                continue
            txt_list = content.select('p.txt')
            # 可能有多个，取最后一个
            txt = txt_list[-1]
            nick_name = txt.attrs['nick-name']
            content = txt.text
            content = content.strip(' \n')
            video_url = ''
            link_list = txt.select('a')
            for link in link_list:
                if '视频' in link.text:
                    # 如果包含
                    video_url = link.attrs['href']

            # 获取评论
            comment = ''
            card_act = card.select_one('div.card-act')
            if card_act:
                li_list = card_act.select('li')
                if li_list and len(li_list) > 2:
                    comment_li = li_list[2]
                    comment = comment_li.text
                    comment = comment.replace('评论', '')
                    comment = comment.strip()
            data = {
                'author': nick_name,
                'comment': comment,
                'content': content,
                'keyword': self.keyword,
                'video_url': video_url
            }
            item = WeiboVideoItem(data)
            yield item
            count += 1
        print(f'爬取视频 {count} 个')
