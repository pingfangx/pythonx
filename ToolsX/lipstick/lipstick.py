import os
import urllib.parse

from bs4 import BeautifulSoup

from xx import filex
from xx import iox
from xx import netx


class ChooseLipstick:
    dior_host = 'https://www.dior.cn'

    def main(self):
        dior_list_file = r'data/dior_list.txt'
        dior_details_file = r'data/dior_details.txt'
        dior_html_file = r'D:\workspace\pingfangx.github.io\baby\lipstick\dior.html'
        dior_color_html_file = r'D:\workspace\pingfangx.github.io\baby\lipstick\dior_color.html'

        ysl_list_file = r'data/ysl_list.txt'
        ysl_detail_file = r'data/ysl_details.txt'
        ysl_html_file = r'D:\workspace\pingfangx.github.io\baby\lipstick\ysl.html'
        ysl_color_html_file = r'D:\workspace\pingfangx.github.io\baby\lipstick\ysl_color.html'
        action_list = [
            ['退出', exit],
            ['读取 Dior 口红列表', self.get_dior_list, dior_list_file],
            ['读取 Dior 口红详情', self.get_dior_details, dior_list_file, dior_details_file],
            ['导出 Dior html', self.export_html, dior_details_file, dior_html_file],
            ['导出 Dior 颜色 html', self.export_color_html, dior_details_file, dior_color_html_file],
            ['读取 YSL 口红列表', self.get_ysl_list, ysl_list_file],
            ['读取 YSL 口红详情', self.get_ysl_details, ysl_list_file, ysl_detail_file],
            ['导出 YSL html', self.export_html, ysl_detail_file, ysl_html_file],
            ['导出 YSL 颜色 html', self.export_color_html, ysl_detail_file, ysl_color_html_file],
        ]
        iox.choose_action(action_list)

    @staticmethod
    def get_dior_list(result_file):
        """读取口红列表"""
        url = 'https://www.dior.cn/beauty/zh_cn/%E9%A6%99%E6%B0%9B%E4%B8%8E%E7%BE%8E%E5%AE%B9/%E5%BD%A9%E5%A6%86/%E5' \
              '%94%87%E9%83%A8/%E5%94%87%E8%86%8F/fr-lipsticks-%E5%94%87%E8%86%8F.html '
        page = netx.get(url, need_print=False)

        # 解析结果
        soup = BeautifulSoup(page, "html.parser")
        result = list()
        i = 0
        for category in soup.select('.category.js-category'):
            '大的分组'
            category_name = category.select_one('.category-title').string.replace('Dior迪奥', '')
            print('\n分组:%s' % category_name)
            for column in category.select('.column.product'):
                '每一个系列'
                legend_name = column.select_one('.legend-name').string.replace('Dior迪奥', '')
                legend_desc = column.select_one('.legend-description').string.strip()
                print('系列名:' + legend_name)
                legend_swatches_list = column.select_one('.legend-swatches-list')
                for legend_li in legend_swatches_list.select('li'):
                    a = legend_li.find('a')
                    url = a['href']
                    color = a.find('img')
                    image = ChooseLipstick.dior_host + color['src']
                    i += 1
                    lipstick = Lipstick('%03d' % i, category_name + '-' + legend_name, '', url, '', legend_desc, image)
                    result.append(str(lipstick) + '\n')
        filex.write_lines(result_file, result)

    @staticmethod
    def get_dior_details(source_file, result_file):
        """获取口红详情"""
        lipstick_list = filex.read_lines(source_file, ignore_line_separator=True)
        length = len(lipstick_list)
        for i in range(length):
            lipstick = Lipstick.from_string(lipstick_list[i])
            print('获取第 %d/%d个口红信息' % (i + 1, length))

            url = ChooseLipstick.dior_host + urllib.parse.quote(lipstick.url)
            page = netx.get(url, need_print=False)
            soup = BeautifulSoup(page, "html.parser")
            cover_img_tag = soup.select_one('.png-bg.cover-bg')
            # all_image = cover_img['data-zoom-views']
            cover_img = cover_img_tag.select_one('.js-cover-img')['src']
            cover_img = ChooseLipstick.dior_host + cover_img

            # name = soup.select_one('.quickbuy-title').string
            # desc = soup.select_one('.quickbuy-subtitle').string
            price = soup.select_one('.details-price.js-order-value').string.strip()
            color_name = soup.select_one('.swatches-list').select_one('li.selected').select_one('a')['data-swatch-name']
            # color_span = soup.select_one('.swatch-name.js-swatch-name')
            # color = color_span.select_one('span').string
            # swatches_list = soup.select_one('.swatches-list.js-products-selector')
            # swatches = swatches_list.select_one('li.selected')
            lipstick.url = url
            lipstick.price = price
            lipstick.name = color_name
            lipstick.img = ','.join((lipstick.img, cover_img))
            filex.write_lines(result_file, [str(lipstick)], mode='a', add_line_separator=True)

    @staticmethod
    def get_ysl_list(result_file):
        """读取口红列表"""
        # 官网的读不出来列表，反正也不多，手动加一下
        url_list = [
            'http://www.yslbeautycn.com/product/00030YSL.html',
            'http://www.yslbeautycn.com/product/00031YSL.html',
        ]
        result = list()
        i = 0
        for details_url in url_list:
            page = netx.get(details_url, need_print=False)
            soup = BeautifulSoup(page, "html.parser")
            category = soup.select_one('.pdp_top_content_wrapper').select_one('.product_subtitle').string
            category = category.replace('圣罗兰', '')
            # image = soup.select_one('.primary_image')['src']
            # color_2 = soup.select_one('.product_image.b-product_img')['src']
            color_list = soup.select_one('.swatches.js_swatches.color.contentcarousel_list')
            for color_li in color_list.select('li'):
                for color_div in color_li.select('div'):
                    url = color_div.select_one('a')['href']
                    color_image = color_div.select_one('img')['src']
                    name = color_div.select_one('span').string
                    name = name.replace('（', '(').replace('）', ')')
                    split_list = name.split('(', 1)
                    if len(split_list) > 1:
                        name = split_list[0].strip()
                        other = '(' + split_list[1].strip()
                    else:
                        other = ''
                    i += 1
                    lipstick = Lipstick('%03d' % i, category, name, url, '', other, color_image)
                    result.append(str(lipstick))
        filex.write_lines(result_file, result, add_line_separator=True)

    @staticmethod
    def get_ysl_details(source_file, result_file):
        lines = filex.read_lines(source_file, ignore_line_separator=True)
        length = len(lines)
        for i in range(length):
            print('获取 %d/%d ' % (i + 1, length))
            line = lines[i]
            lipstick = Lipstick.from_string(line)
            # 有一些颜色没指定，打开会转到默认颜色
            page = netx.get(lipstick.url, need_print=False)
            soup = BeautifulSoup(page, "html.parser")
            cover_image = soup.select_one('.primary_image')['src']
            color_image2 = soup.select_one('.product_tab_shades_left').select_one('.product_image.b-product_img')['src']
            price = soup.select_one('.product_price.price_sale.b-product_price-sale').text.strip()
            lipstick.img = ','.join((lipstick.img, color_image2, cover_image))
            lipstick.price = price
            filex.write_lines(result_file, [str(lipstick)], mode='a', add_line_separator=True)

    @staticmethod
    def export_html(source_file, result_file):
        """导出 html"""
        lipstick_type = os.path.splitext(os.path.basename(result_file))[0].split('_')[0]
        current_path = os.path.dirname(result_file) + '/'
        lines = filex.read_lines(source_file, ignore_line_separator=True)
        length = len(lines)
        html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>选呀选呀选口红~</title>
    <link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css"
          integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
    <link rel="stylesheet" href="css/lipstick.css">
</head>
<body>
<div class="container-fluid">
    [content]
</div>
</body>
</html>
        '''
        content = list()
        for i in range(length):
            content.append('<div class="row">')
            lipstick = Lipstick.from_string(lines[i])
            # 左边
            content.append('<div class="%s">' % 'col-xs-3')
            item_list = ['编号:' + lipstick.index, '色号:' + lipstick.name, '类别:' + lipstick.category, lipstick.other]
            for cell in item_list:
                content.append('<h4>%s</h4>' % cell)
            content.append('</div>')

            # 右边的图
            image_list = lipstick.img.split(',')
            length = len(image_list)
            for j in range(length):
                if length == 2:
                    if j == 0:
                        col_style = 'col-xs-3'
                    else:
                        col_style = 'col-xs-5'
                else:
                    col_style = 'col-xs-3'
                img = image_list[j]
                image_path = '%simage/%s_%03d_%d.jpg' % (current_path, lipstick_type, i + 1, j + 1)
                ima_tag = '<img class="%s" src="%s"/>' % (col_style, image_path.replace(current_path, ''))
                if not os.path.exists(image_path):
                    netx.get_file(img, image_path)
                content.append(ima_tag)
            content.append('</div>')

        content = html.replace('[content]', '\n'.join(content))
        filex.write(result_file, content)

    @staticmethod
    def export_color_html(source_file, result_file):
        """导出 html"""
        html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>选呀选呀选口红~</title>
    <link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css"
          integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
    <link rel="stylesheet" href="css/lipstick_color.css">
</head>
<body>
<div class="container-fluid">
    [content]
</div>
</body>
</html>
        '''
        lipstick_type = os.path.splitext(os.path.basename(result_file))[0].split('_')[0]
        content = list()

        lines = filex.read_lines(source_file, ignore_line_separator=True)
        length = len(lines)
        for i in range(0, length, 4):
            content.append('<div class="row">')
            end_index = i + 4
            if end_index > length:
                end_index = length
            for j in range(i, end_index):
                lipstick = Lipstick.from_string(lines[j])
                name_tag = '<span class="item">%s</span>' % '<br/>'.join(
                    ('编号:' + lipstick.index, '色号:' + lipstick.name))
                image_path = 'image/%s_%03d_%d.jpg' % (lipstick_type, j + 1, 1)
                img_tag = '<img class="center-block" src="%s"/>' % image_path

                content.append('<div class="col-xs-3">')
                content.append(name_tag)
                content.append(img_tag)
                content.append('</div>')

            content.append('</div>')

        html = html.replace('[content]', '\n'.join(content))
        filex.write(result_file, html)


class Lipstick:
    """口红"""

    def __init__(self, index, category, name, url, price, other, img):
        self.index = index
        self.category = category
        self.name = name
        self.url = url
        self.price = price
        self.other = other
        self.img = img

    def __str__(self):
        return '|'.join((self.index, self.category, self.name, self.url, self.price, self.other, self.img))

    @staticmethod
    def from_string(string):
        return Lipstick(*string.split('|'))


if __name__ == '__main__':
    ChooseLipstick().main()
