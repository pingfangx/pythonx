import os
import time
from typing import List, Dict


class Shift:
    """班次"""
    name_list = [
        '早',
        '午',
        '晚',
        '夜',
    ]

    def __init__(self, index: int, workday):
        self.index = index
        self.name: str = self._get_name(index)
        self.workday = workday
        self.worker: Person = None

    def _get_name(self, index) -> str:
        return self.name_list[index]

    def __str__(self):
        return f'{self.name}班'

    def name_with_workday(self):
        return f'{self.workday} {self}'


class WorkDay:
    """工作日"""

    name_list = [
        '一',
        '二',
        '三',
        '四',
        '五',
        '六',
        '日',
    ]

    def __init__(self, index: int = 0):
        self.index = index
        self.name: str = self._get_name(index)
        self.shifts: List[Shift] = [Shift(i, self) for i in range(4)]

    def _get_name(self, index):
        return self.name_list[index]

    def __str__(self):
        return f'星期{self.name}'

    def get_shifts_info(self):
        """获取本日排班信息"""
        return f'{self}\t' + '\t'.join([shift.worker.name for shift in self.shifts])


class Week:
    """每周"""

    def __init__(self):
        self.days: List[WorkDay] = [WorkDay(i) for i in range(7)]


class Person:
    """人员"""
    FEMALE = 1

    def __init__(self, name, sex=0):
        self.name = name
        self.sex = sex
        self.shift_list: List[Shift] = []
        self.shift_times = [0] * 4

    def schedule_shift(self, shift: Shift) -> bool:
        """排班

        :param shift: 班次
        :return: 是否排班成功
        """
        if self.support_shift(shift):
            # 设置人员
            shift.worker = self
            # 添加排班
            self.shift_list.append(shift)
            # 增加次数
            self.shift_times[shift.index] += 1
            return True
        else:
            return False

    def support_shift(self, shift: Shift) -> bool:
        """是否支持此班"""
        for scheduled_shift in self.shift_list:
            if scheduled_shift.name == '夜' and scheduled_shift.workday.index == shift.workday.index - 1:
                log(f'{self.name} 前一天刚值了夜班，不支持此班')
                return False
        if shift.name == '夜':
            if self.is_female():
                log(f'{self.name} 是女性，不支持此夜班')
                return False
        return True

    def get_shift_times(self) -> int:
        """获取班次数量"""
        times = 0
        for i in self.shift_times:
            times += i
        return times

    def get_same_time_shift_times(self, shift) -> int:
        """获取相同时间段的班次的次数，用来保证每个人不同时间段平均"""
        times = 0
        for scheduled_shift in self.shift_list:
            if scheduled_shift.index == shift.index:
                times += 1
        return times

    def is_female(self) -> bool:
        """是否是女性"""
        return self.sex == self.FEMALE

    def __str__(self):
        return self.name

    def get_shifts_info(self):
        """获取本人的排班信息"""
        info = self.name

        # 统计次数
        info += '\t'
        info += '\t'.join(f'{Shift.name_list[i]}({times})' for i, times in enumerate(self.shift_times))

        # 每个班
        info += '\t'
        info += '\t'.join([f'{shift.workday}{shift}' for shift in self.shift_list])
        return info

    def get_shifts_info_for_output(self):
        """用于输出的排班信息"""
        sex = '女' if self.is_female() else '男'
        shift_times = ','.join([str(i) for i in self.shift_times])
        return f"{self},{sex},{shift_times}"


class ScheduleShifts:
    """排班"""

    def __init__(self, person_input_file, person_output_file, shifts_output_file):
        self.person_input_file = person_input_file
        self.person_output_file = person_output_file
        self.shifts_output_file = shifts_output_file
        self.person_list: List[Person] = Helper.read_person_list(self.person_input_file)

        self.week = Week()

    def schedule(self):
        """排班"""
        log(f'当前读取到的人员')
        for person in self.person_list:
            log(f'{person.get_shifts_info_for_output()}')

        # 排班
        self.schedule_all_shift()

        shifts_output = self.print_schedule_by_word_day()
        shifts_output += '\n\n' + self.print_schedule_by_person()
        log(f'\n\n输出排班数据: {self.shifts_output_file}')
        log(shifts_output)
        Helper.write(shifts_output, self.shifts_output_file)

        person_output = ['# 名字,姓别,早班,午班,晚班,夜班']
        for person in self.person_list:
            person_output.append(person.get_shifts_info_for_output())
        person_output = '\n'.join(person_output)
        log(f'\n\n输出人员数据: {self.person_output_file}')
        log(person_output)
        Helper.write(person_output, self.person_output_file)

    def schedule_all_shift(self):
        """排所有班"""
        for day in self.week.days:
            log(f'\n排 {day} 的班')
            for shift in day.shifts:
                self.schedule_shift(shift)

    def schedule_shift(self, shift: Shift):
        """排班

        不支持班次肯定不排
        如果都支持
            如果总班数更少，排给他，因为每个人班数应该平均
            如果部班数相同，如果该班次更少，排给他，因为各班次应该平均给每个人

        :param shift:班次
        :return:
        """
        log(f'\n排 {shift.name_with_workday()}')
        log(f'选出支持此班的人员')
        candidate_list = []
        for person in self.person_list:
            if person.support_shift(shift):
                log(f'{person} 支持此班')
                candidate_list.append(person)
        log(f'\n共有 {len(candidate_list)} 人支持此班')
        log(','.join([person.name for person in candidate_list]))

        log(f'\n选出值 {shift} 次数少的人员')
        min_times = 1 << 30
        candidate_dict: Dict[int, List] = {}
        for person in candidate_list:
            shift_times = person.get_same_time_shift_times(shift)
            if shift_times in candidate_dict.keys():
                candidate_dict[shift_times].append(person)
            else:
                candidate_dict[shift_times] = [person]
            if shift_times < min_times:
                min_times = shift_times
        log(f'值 {shift} 次数最少为 {min_times} 次，共 {len(candidate_dict[min_times])} 人都值了 {min_times} 次')
        candidate_list = candidate_dict[min_times]
        log(','.join([person.name for person in candidate_list]))

        log(f'\n选出值班次数较少的人员')
        destination: Person = None
        min_times = 1 << 30
        for person in candidate_list:
            shift_times = person.get_shift_times()
            if shift_times < min_times:
                min_times = shift_times
                destination = person
        log(f'{destination} 值班总次数较少，为 {min_times} 次')

        if not destination:
            log(f'\n未找到人值此班，排班失败')
            exit()
        else:
            # 排给此人
            log(f'\n最终由 {destination} 值此班 {shift.name_with_workday()}')
            destination.schedule_shift(shift)
            # 将此人移到最后，不用移到最后，因为会统计总次数，如果要移动，最合输出时注意按顺序
            # self.person_list.remove(destination)
            # self.person_list.append(destination)

    def print_schedule_by_word_day(self):
        """按工作日输出班次"""
        lines = ['按工作日输出班次']
        for day in self.week.days:
            lines.append(day.get_shifts_info())
        return '\n'.join(lines)

    def print_schedule_by_person(self):
        """按人输出班次"""
        lines = ['按人输出班次']
        for person in self.person_list:
            lines.append(person.get_shifts_info())
        return '\n'.join(lines)


def log(text):
    print(text)
    Helper.log(text)


class Helper:
    """读写助手"""
    log_file = ''
    """日志文件"""

    @staticmethod
    def read_person_list(file_path):
        """读取排班数据"""
        if not os.path.exists(file_path):
            print(f'输入人员数据文件不存在 {file_path}')
            exit()
        person_list = []
        with open(file_path, encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                line = line.rstrip('\n')
                if line.startswith('#'):
                    continue
                data = line.split(',')
                length = len(data)
                if length <= 0:
                    continue

                name = data[0]
                sex = 0
                if length > 1:
                    # 性别
                    sex = (1 if data[1] == '女' else 0)
                person = Person(name, sex)

                if length == 6:
                    # 之前的排班记录
                    person.shift_times = [int(i) for i in data[2:6]]
                person_list.append(person)
        return person_list

    @staticmethod
    def write(text, file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)

    @staticmethod
    def log(text):
        with open(Helper.log_file, 'a', encoding='utf-8') as f:
            f.write('\n' + text)


if __name__ == '__main__':
    now = time.strftime('%Y%m%d%H%M%S', time.localtime())
    _person_input = '输入人员数据.txt'
    _person_output = f'{now}-输出人员数据.txt'
    _shifts_output = f'{now}-排班结果.txt'
    Helper.log_file = f'{now}-排班过程.txt'
    ScheduleShifts(_person_input, _person_output, _shifts_output).schedule()
