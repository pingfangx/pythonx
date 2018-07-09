import asyncio
import threading
import time
from multiprocessing import Process


class TestMulti():

    def work(self, num):
        print(f'work-{num} start')
        time.sleep(1)
        for i in range(3):
            print(f'work-{num} sleep {i}')
            time.sleep(1)
        print(f'work-{num} finish')

    def test_multi_thread(self):
        """测试多线程"""
        thread_list = []
        for i in range(10):
            thread_list.append(threading.Thread(target=self.work, args=(i,)))

        for thread in thread_list:
            thread.start()

        for thread in thread_list:
            thread.join()
        print('finish.')

    def test_multi_processing(self):
        """测试多进程"""
        process_list = []
        for i in range(10):
            process_list.append(Process(target=self.work, args=(i,)))

        for process in process_list:
            process.start()
        for process in process_list:
            process.join()
        print('finish')

    async def work2(self, num):
        print(f'work-{num} start')
        await asyncio.sleep(1)
        for i in range(3):
            print(f'work-{num} sleep {i}')
            time.sleep(1)
        print(f'work-{num} finish')

    def test_coroutine(self):
        """测试协程"""
        loop = asyncio.get_event_loop()
        tasks = [self.work2(i) for i in range(5)]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()


if __name__ == '__main__':
    TestMulti().test_multi_thread()
    # TestMulti().test_multi_processing()
    # TestMulti().test_coroutine()
