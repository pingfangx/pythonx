import sys

import requests
from xx import iox
from xx import netx


class Progress:
    def __init__(self, all):
        self.all = all
        self.all_size = self.get_size(self.all)
        self.progress = 0

    def append(self, progress):
        self.progress += progress
        self.print()

    def print(self):
        sys.stdout.write('\r 下载中 %.2f%% ,%s/%s '
                         % (self.progress / self.all * 100, self.all_size, self.get_size(self.progress)))
        sys.stdout.flush()

    @staticmethod
    def get_size(count):
        if count < 0:
            return 'error size.'
        size_unit = [
            'B',
            'K',
            'M',
            'G'
        ]
        """
        level 标记当前大小，如果小于 level+1 次方，说明属于 level 级别，break
        如果都不属于，退出时 level 取的是 3，注意这和 i++ 的形式不同， i++ 应该为 4 才退出
        
        
    private String getSize(double count) {
        //注意使用了 double 类型，如果还不够
        if (count < 0) {
            return "error size.";
        }
        String[] sizeUnits = new String[]{"B", "K", "M", "G"};
        int i;
        for (i = 0; i < sizeUnits.length; i++) {
            if (count < Math.pow(1024, i + 1)) {
                break;
            }
        }
        if (i == sizeUnits.length) {
            //退出循环时相等
            i--;
        }
        return String.format("%.2f%s", count / Math.pow(1024, i), sizeUnits[i]);
    }

    private String getSize2(double count) {
        if (count < 0) {
            return "error size.";
        }
        if (count == 0) {
            //防上后面的 log
            return "0.00B";
        }
        String[] sizeUnits = new String[]{"B", "K", "M", "G"};
        int i = (int) Math.floor(Math.log(count) / Math.log(1024));
        if (i >= sizeUnits.length) {
            //这里要判断 >=
            i = sizeUnits.length - 1;
        }
        return String.format("%.2f%s", count / Math.pow(1024, i), sizeUnits[i]);
    }

        
        """
        level = 0
        for level in range(len(size_unit)):
            if count < 1024 ** (level + 1):
                break
        return '%.2f%s' % (count / 1024 ** level, size_unit[level])


class Aweme:
    def __init__(self):
        self.chunk_size = 1024
        self.params_file_path = r'ignore/params.txt'
        self.api_feed = 'https://aweme.snssdk.com/aweme/v1/feed/'

    def main(self):
        video_url = r'https://aweme.snssdk.com/aweme/v1/play/?video_id=cf887355f4fa491a9604b228dad63919&line=0&ratio' \
                    r'=720p&media_type=4&vr_type=0&test_cdn=None&improve_bitrate=0 '
        file_path = '1.mp4'
        action_list = [
            ['退出', exit],
            ['抓取列表', self.get_feed_list],
            ['下载视频', self.download_video, video_url, file_path],
        ]
        iox.choose_action(action_list)

    def get_feed_list(self):
        """抓取列表"""
        params = netx.parse_params_from_file(self.params_file_path)
        print(params)
        url = self.api_feed
        r = requests.get(url, params).json()
        print(r)

    def download_video(self, url, file_path):
        print('开始下载')
        r = requests.get(url, stream=True)
        content_size = int(r.headers['content-length'])
        progress = Progress(content_size)
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(self.chunk_size):
                f.write(chunk)
                progress.append(len(chunk))
        print('下载完成')


if __name__ == '__main__':
    Aweme().main()
