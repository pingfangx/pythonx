from xx import iox


class Dimension:
    def __init__(self, size_in, width_px, height_px):
        """

        :param size_in: 大小，英寸
        :param width_px: 宽度，像素
        :param height_px: 高度，像素
        """
        self.size_in = size_in
        self.width_px = width_px
        self.height_px = height_px

    def main(self):
        action_list = [
            ['退出', exit],
            ['计算', self.calculate],
        ]
        iox.choose_action(action_list)

    def calculate(self):
        self.calculate_and_print(self.size_in, self.width_px, self.height_px)

    def calculate_and_print(self, size_in, width_px, height_px):
        """计算"""
        all_pixels = width_px * height_px
        print()
        print(f'分辨率 {width_px} x {height_px},{int(all_pixels/10000)}万像素')

        print('\n根据尺寸计算宽高')
        # 宽^2 + 高^2 = 斜边^2
        scale = height_px / 1.0 / width_px
        print(f'宽^2 +({scale}*宽)^2={size_in}^2')
        width_in = (size_in ** 2 / (1 + scale ** 2)) ** 0.5
        width_mm = self.inch_to_mm(width_in)
        print(f'宽为 {width_in} inches，{width_mm} mm')
        height_in = width_in * scale
        height_mm = self.inch_to_mm(height_in)
        print(f'高为 {height_in} inches,{height_mm} mm')
        cal_size_in = (width_in ** 2 + height_in ** 2) ** 0.5
        size_px = (width_px ** 2 + height_px ** 2) ** 0.5
        print(f'计算尺寸为 {cal_size_in} inch,{size_px} px')

        print('\n计算 ppi(pixels per inch)')
        width_ppi = width_px / width_in
        height_ppi = height_px / height_in
        size_ppi = size_px / size_in
        print(f'以宽计算 {width_ppi}，以高计算 {height_ppi}，以对角线计算 {size_ppi}')

        density, dpi_level = self.get_density_and_dpi_level(size_ppi)
        print(f'\ndensity 为 {density},dpi 级别为 {dpi_level}')

    @staticmethod
    def inch_to_mm(inch):
        return inch * 25.4

    @staticmethod
    def get_density_and_dpi_level(dpi):

        """
        获取 dpi 等级，结果不准确，真机应该取的是近似值
        由 android.util.DisplayMetrics#getDeviceDensity 获取 density ，density 再对应 dpi
        https://developer.android.com/guide/practices/screens_support?hl=zh-cn#range
        :return density,dpi_level
        """
        level = {
            "ldpi": 120,
            "mdpi": 160,
            "hdpi": 240,
            "xhdpi": 320,
            "xxhdpi": 480,
            "xxxhdpi": 640,
        }
        level2 = {v: k for k, v in level.items()}
        for k in sorted(level2.keys()):
            if dpi < k:
                return k / 160, f'{level2[k]}({k})'
        return 1, 'unknown'

    def cal_px_in_css(self):

        a1_in = 28
        b1_in = 1 / 96

        radio = a1_in / b1_in

        print(f'比例为 {radio}')

        a = 138
        b = a / radio
        print(f'a={a} inch，b={b:.2f} inch,{self.inch_to_mm(b):.2f} mm')

        print(f'Android 定义 160dpi 下 1dp=1px')
        b = 1 / 160
        a = b * radio
        print(f'b={b} inch,a={a:.2f} inch,{self.inch_to_mm(a):.2f} mm')


if __name__ == '__main__':
    # DisplayMetrics{density=3.0, width=1080, height=1920, scaledDensity=3.0, xdpi=428.625, ydpi=427.789}
    Dimension(5.15, 1080, 1920).calculate()
