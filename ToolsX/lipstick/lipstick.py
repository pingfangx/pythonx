from bs4 import BeautifulSoup

from xx import iox
from xx import netx


class Demo:
    def main(self):
        action_list = [
            ['退出', exit],
            ['选择Dior颜色', self.choose_dior_color, ''],
        ]
        iox.choose_action(action_list)

    def choose_dior_color(self, param):
        url = 'https://www.dior.cn/beauty/zh_cn/%E9%A6%99%E6%B0%9B%E4%B8%8E%E7%BE%8E%E5%AE%B9/%E5%BD%A9%E5%A6%86/%E5%94%87%E9%83%A8/%E5%94%87%E8%86%8F/fr-lipsticks-%E5%94%87%E8%86%8F.html'
        page = netx.get(url, need_print=False)

        # 解析结果
        soup = BeautifulSoup(page, "html.parser")
        for category in soup.select('.category.js-category'):
            '大的分组'
            category_title = category.select_one('.category-title')
            print('\n分组:%s' % category_title.string)
            for column in category.select('.column.product'):
                '每一个系列'
                legend_name = column.select_one('.legend-name')
                print('系列名:' + legend_name.text)
                legend_swatches_list = column.select_one('.legend-swatches-list')
                for legend_li in legend_swatches_list.select('li'):
                    a = legend_li.find('a')
                    url = a['href']
                    color = a.find('img')
                    image = color['src']
                    print('地址%s' % url)
                    print('图片%s' % image)
        pass


if __name__ == '__main__':
    Demo().main()
