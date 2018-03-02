import queue
import threading


class HandleQueueMultiThread:
    """处理 queue 的多线程"""

    def __init__(self, q, callback, callback_arg_num=3, thread_num=4, element_str_function=str,
                 print_before_task=False, print_after_task=False, print_when_thread_exit=True):
        """
        :param q: 队列
        :param callback: 回调，最多接受 3 个参数，element,element_index,thread_id
        :param callback_arg_num: 回调方法的参数数量,默认为3
        :param thread_num: 线程数
        :param element_str_function: 用于输出元素时调用的方法,默认为 str
        :param print_before_task: 任务开始前是否输出,默认为 False
        :param print_after_task: 任务结束后是否输出,默认为 False
        :param print_when_thread_exit: 线程退出时是否输出,默认为 True
        """

        self.q = q
        self.callback = callback
        self.callback_arg_num = callback_arg_num
        self.thread_num = thread_num
        self.element_str_function = element_str_function
        self.print_before_task = print_before_task
        self.print_after_task = print_after_task
        self.print_when_thread_exit = print_when_thread_exit

        self.running_thread_num = 0
        "正在运行中的线程数"

        self.element_index = 0
        "已运行的任务数"

    def start(self):
        self.running_thread_num = 0
        self.element_index = 0
        threads = []
        thread_num = self.thread_num
        if thread_num > self.q.qsize():
            thread_num = self.q.qsize()

        for i in range(0, thread_num):
            worker = threading.Thread(target=self.iterator, args=(self.callback, i + 1))
            worker.start()
            threads.append(worker)
        # 这里好像不需要 thread 的 join，queue 的 join 也会阻塞，但还是加上线程的 join，以使线程结束后再继续执行后续代码
        # 注意调用 task_done()
        # https://docs.python.org/3/library/queue.html
        # http://blog.csdn.net/xiao_huocai/article/details/74781820
        # block until all tasks are done
        self.q.join()
        for t in threads:
            t.join()

    def iterator(self, callback, thread_id):
        """在线程中迭代,直到出错"""
        while True:
            try:
                self.running_thread_num += 1
                element = self.q.get(block=True, timeout=1)
                self.element_index += 1

                if self.print_before_task:
                    print('线程 %d 开始执行第 %d 个任务，剩余 %d 个任务，%s' % (
                        thread_id, self.element_index, self.q.qsize(), self.element_str_function(element)))

                if self.callback_arg_num == 1:
                    callback(element)
                elif self.callback_arg_num == 2:
                    callback(element, self.element_index)
                elif self.callback_arg_num == 3:
                    callback(element, self.element_index, thread_id)
                # 告知结束一个任务
                self.q.task_done()

                if self.print_after_task:
                    print('线程 %d 执行第 %d 个任务结束，剩余 %d 个任务，%s' % (
                        thread_id, self.element_index, self.q.qsize(), self.element_str_function(element)))
            except queue.Empty:
                if self.print_when_thread_exit:
                    print('线程 %d 结束，还有 %d 个线程运行中' % (thread_id, self.running_thread_num - 1))
                break
            finally:
                self.running_thread_num -= 1
