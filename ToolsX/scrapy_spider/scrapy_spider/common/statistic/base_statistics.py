class BaseStatistics:
    """用于统计的工具"""

    @staticmethod
    def format_time(second):
        """格式化时间输出

        >>> BaseStatistics.format_time(0)
        '00:00'
        >>> BaseStatistics.format_time(1)
        '00:01'
        >>> BaseStatistics.format_time(60)
        '01:00'
        >>> BaseStatistics.format_time(61)
        '01:01'
        >>> BaseStatistics.format_time(3600)
        '01:00:00'
        >>> BaseStatistics.format_time(3661)
        '01:01:01'
        >>> BaseStatistics.format_time(3600*25)
        '25:00:00'

        """
        time_list = [
            60,
            60,
            0,
        ]
        result = [-1] * len(time_list)
        # min 总是需要
        result[1] = 0
        current_time = int(second)
        for i, max_time in enumerate(time_list):
            if current_time < max_time or max_time == 0:
                # 取整
                result[i] = current_time
                break
            else:
                # 求余
                result[i] = current_time % max_time
            current_time = int(current_time / max_time)
        result = [f'{i:#02d}' for i in reversed(list(filter(lambda x: x != -1, result)))]
        return ':'.join(result)
