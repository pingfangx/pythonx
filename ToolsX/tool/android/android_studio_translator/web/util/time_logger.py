import time


class TimeLogger:
    """用来记时"""

    def __init__(self, task_name='任务'):
        self._start_time = time.time()
        self._task_name = task_name
        print(f'{self._task_name}开始')

    def stop(self):
        end_time = time.time()
        print(f'{self._task_name}结束，耗时 {end_time-self._start_time:.3f}s')
