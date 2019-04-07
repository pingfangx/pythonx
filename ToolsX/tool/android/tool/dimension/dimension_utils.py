from xx import iox


class Dimension:
    """尺寸"""

    def __init__(self, name=''):
        self.name = name

        self.inch = 0
        self.px = 0
        self.ppi = 0
        self.mm = 0

    def get_px(self):
        return self.get('px')

    def get_ppi(self):
        return self.get('ppi')

    def get_inch(self):
        return self.get('inch')

    def get_mm(self):
        return self.get('mm')

    def get(self, unit):
        return f'{self.__dict__[unit]} {unit}'

    def calculate_size_base_px(self, px, ppi):
        """基于像素计算尺寸"""
        self.px = px
        self.ppi = ppi

        print(f'计算 {self.name},{self.get_px()},{self.get_ppi()}')
        self.inch = self.px / ppi
        self.mm = self.inch_to_mm(self.inch)
        print(f'结果为:{self.get_inch()},{self.get_mm()}')

    @staticmethod
    def inch_to_mm(inch):
        return inch * 25.4


class Screen:
    """屏幕"""

    def __init__(self):
        self.width = Dimension('宽')
        self.height = Dimension('高')
        self.diagonal = Dimension('对角线')

    def calculate_size_base_ppi(self, width_px, height_px, ppi):
        """根据 ppi 计算宽高"""
        print(f'根据 ppi 计算宽高, ppi 为 {ppi}')
        self.width.calculate_size_base_px(width_px, ppi)
        self.height.calculate_size_base_px(height_px, ppi)
        self.diagonal.calculate_size_base_px(self.calculate_diagonal(width_px, height_px), ppi)

    @staticmethod
    def calculate_diagonal(width, height):
        """根据宽高计算对角线"""
        return (width ** 2 + height ** 2) ** 0.5


class DimensionUtils:
    """计算工具"""

    def main(self):
        screen = Screen()
        action_list = [
            ['退出', exit],
            ['根据 ppi 计算记算屏幕的实际宽高', screen.calculate_size_base_ppi, 1200, 1920, 224],
        ]
        iox.choose_action(action_list)


if __name__ == '__main__':
    DimensionUtils().main()
