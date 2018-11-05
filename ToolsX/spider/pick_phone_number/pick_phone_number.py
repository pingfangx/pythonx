import json
import queue
import re
import time

from xx import filex
from xx import iox
from xx import netx
from xx import threadx


class Demo:
    url = 'https://m.10010.com/NumApp/NumberCenter/qryNum?callback=jsonp_queryMoreNums&provinceCode=86&cityCode=860' \
          '&monthFeeLimit=0&groupKey=79237759&searchCategory=3&net=01&amounts=200&codeTypeCode=&searchValue=&qryType' \
          '=02&goodsNet=4&_= '
    num_file_path = 'ignore/num.txt'
    numbers = []

    def main(self):
        action_list = [
            ['退出', exit],
            ['循环中获取手机号', self.get_num_in_loop],
            ['多线程获取手机号', self.get_num_in_multi_thread],
            ['过滤号码', self.filter_num],
        ]
        iox.choose_action(action_list)

    def get_num_in_loop(self):
        for i in range(100):
            self.get_num()
            sleep_time = 1
            print(f'第 {i+1} 轮，休息 {sleep_time}s')
            time.sleep(sleep_time)

    def get_num(self):
        url = self.url
        url += str(int(time.time() * 1000))
        print(url)
        result = netx.get(url)
        result = result[result.index('(') + 1:result.index(')')]
        result = json.loads(result)
        num_list = list(filter(lambda x: len(str(x)) == 11, result['numArray']))
        num_list = [str(x) for x in num_list]
        print(num_list)
        print(f'获取到号码 {len(num_list)} 个')
        old_numbers = filex.read_lines(self.num_file_path, ignore_line_separator=True)
        print(f'之前有号码 {len(old_numbers)} 个')
        num_list = list(filter(lambda x: x not in old_numbers, num_list))
        print(f'过滤后，剩号码 {len(num_list)} 个')
        filex.write_lines(self.num_file_path, num_list, 'a', add_line_separator=True)

    def get_num_in_multi_thread(self):
        self.numbers = filex.read_lines(self.num_file_path, ignore_line_separator=True)
        if self.numbers is None:
            self.numbers = []
        length = len(self.numbers)
        print(f'获取前共 {length} 个')
        q = queue.Queue()
        for i in range(1000):
            q.put(i)
        t = threadx.HandleQueueMultiThread(q, self.get_in_thread, thread_num=10, print_before_task=True)
        t.start()
        current_length = len(self.numbers)
        print(f'获取结束，获取到 {current_length-length}号码，当前共 {current_length} 个')
        filex.write_lines(self.num_file_path, self.numbers, add_line_separator=True)

    def get_in_thread(self, element, element_index, thread_id):
        url = self.url
        url += str(int(time.time() * 1000))
        print(url)
        result = netx.get(url, need_print=False)
        result = result[result.index('(') + 1:result.index(')')]
        result = json.loads(result)
        num_list = list(filter(lambda x: len(str(x)) == 11, result['numArray']))
        num_list = [str(x) for x in num_list]
        print(num_list)
        print(f'获取到号码 {len(num_list)} 个')
        num_list = list(filter(lambda x: x not in self.numbers, num_list))
        print(f'过滤后，剩号码 {len(num_list)} 个')
        self.numbers.extend(num_list)
        print(f'当前号码 {len(self.numbers)} 个')

    def filter_num(self):
        pattern = '87910'
        pattern = re.compile(pattern)
        numbers = filex.read_lines(self.num_file_path, ignore_line_separator=True)
        result = []
        for num in numbers:
            if re.search(pattern, num):
                result.append(num)
        print(f'共 {len(numbers)} 个号码，过滤 {pattern} ，得到 {len(result)} 个')
        for num in result:
            print(num)


if __name__ == '__main__':
    Demo().main()
