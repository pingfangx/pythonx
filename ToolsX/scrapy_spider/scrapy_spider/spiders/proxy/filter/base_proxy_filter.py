import queue

from xx import threadx


class BaseProxyFilter:
    """过滤有效的代理"""

    def __init__(self, proxy_list, validator_list=None):
        """

        :param proxy_list: 需要检查的代理列表
        :param validator_list: 检查器列表
        """
        self._q = queue.Queue()
        self.available_q = queue.Queue()
        self.validator_list = validator_list
        if self.validator_list is None:
            self.validator_list = []

        for proxy in proxy_list:
            self._q.put(proxy)

    def before_filter(self):
        """过滤前"""

    def filter(self):
        """过滤"""

        # 过滤前
        self.before_filter()

        # 执行过滤
        multi_thread = threadx.HandleQueueMultiThread(self._q, callback=self.validate_proxy, thread_num=100,
                                                      print_before_task=False,
                                                      print_after_task=False,
                                                      print_when_thread_exit=False)
        multi_thread.start()

        # 过滤后
        self.after_filter()

        # 返回结果
        available_proxy = []
        while not self.available_q.empty():
            available_proxy.append(self.available_q.get())
        return available_proxy

    def after_filter(self):
        """过滤后"""

    def validate_proxy(self, element, element_index, thread_id):
        for validator in self.validator_list:
            name = validator.__class__.__name__
            # print(f'{name} 校验 {element}')
            if not validator.validate(element):
                # print(f'{name} 校验 {element} 无效')
                return
            else:
                # print(f'{name} 校验 {element} 有效')
                pass
        # 都校验通过，认为有效
        self.available_q.put(element)
