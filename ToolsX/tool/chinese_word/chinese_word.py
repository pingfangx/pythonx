import re

from xx import iox, filex


class ChineseWord:
    """
    中华字经
    偶然间看到有关消息，非常感兴趣
    来自 http://xh.5156edu.com/page/z4631m9119j18708.html

     “只学一篇韵文便识天下汉字”这句话说的似乎大了，但事实的确如此郑州大学郭保华教授用三年多的时间将4000汉字著成一篇韵文《中华字经》全文共一千句，用字4000无一字相重，涵盖了百科又韵语成章，高难度的写作换来了识字教材的全方位突破，小学6年的识字量，二个半月就可完成。
   《中华字经》是教育部语言文字应用研究所的 “ 快速识字，提前阅读 ” 课题的最新科研成果。该成果被立项为全国教育科学规划 “ 十五 ” 研究课题，题目是 “ 传统文化教育的现代价值研究与创新实践 ” 。
   《中华字经》及配套教材均为该成果的具体转化并被教育部语用所语言教学研究室作为 “ 快速识字、提前阅读特种教材 ” 向全国及海外推广，是中国侨联指定的海外华人学习的汉语教材。
   《中华字经》是一种超级识字教材，以四字一句、分门别类、字不重用、韵语连篇的方法编撰而成。
   全文收录汉字 4000 个，涵盖了国家教育部、国家语委联合颁布的常用汉字和 HSK 考试大纲规定的四级汉字。
   集识字、组词、习韵、正音、学知于一体，可使普通儿童学习 4 － 6 个月掌握一生常用的全部汉字，并经教育部语言文字研究所实验基地、多家幼儿园所验证，经公证处公证， 5 岁儿童 4 个月学完《中华字经》，巩固率为 74.6% ，即 2984 个字，提高现有识字速度的 15 － 20 倍。

   共 4 个部分，前三部分各 1000 字
   16*62+8=1000
   最后一部分 984 字
   16*61+8
   一开始以为是算错了，后来在 https://wenku.baidu.com/view/2de42d53c77da26924c5b015.html 中也显示是 984 字
   也就是说，4000 字是加上各部分的小标题的

   分析完之后，有 28 字重复，就算抛去多音字、录入错误，还是有重复，下文也有分析
   [中华字经里的重复字](http://dapengde.com/archives/17072)
    """

    def __init__(self):
        self.source_file = 'chinese_word.txt'
        self.target_file = 'chinese_word_2.txt'

    def main(self):
        action_list = [
            ['退出', exit],
            ['获取纯汉字', self.filter_word],
        ]
        iox.choose_action(action_list)

    def filter_word(self):
        lines = filex.read_lines(self.source_file, ignore_line_separator=True)
        # 过滤空格和逗号名号
        lines = [re.subn(r'[\s，。]', '', line)[0] for line in lines]
        # 过滤行
        lines = list(filter(self.filter_line, lines))
        # 写入文件暂存
        filex.write_lines(self.target_file, lines, add_line_separator=True)

        # 拼接以处理
        all_text = ''.join(lines)
        print(f'整理完毕，共 {len(all_text)} 字')
        self.find_duplicate(lines)

    @staticmethod
    def find_duplicate(lines):
        """
        查重，本来在拼接的结果处理更简单，但需要输出位置
        """
        line_length = len(lines)
        duplicate_count = 0
        for i in range(line_length):
            line = lines[i]
            for j in range(len(line)):
                word = line[j]

                # 检查当前行
                index = line.find(word, j + 1)
                if index > -1:
                    duplicate_count += 1
                    print(f'\n第 {duplicate_count} 处重复：第 {i+1} 行第 {j+1} 个字与第 {index+1} 个字重复')
                    print(word)
                    print(line)
                # 检查后续行
                for i2 in range(i + 1, line_length):
                    index = lines[i2].find(word)
                    if index > -1:
                        duplicate_count += 1
                        print(f'\n第 {duplicate_count} 处重复：第 {i+1} 行第 {j+1} 个字与第 {i2+1}行 第 {index+1} 个字重复')
                        print(word)
                        print(line)
                        print(lines[i2])

    @staticmethod
    def filter_line(line: str):
        """过滤行"""
        if not line:
            return False
        if line.startswith('#'):
            return False
        if re.search(r'[a-zA-Z]', line):
            # 有拼音
            return False
        if re.search(r'中华字经|(第.*部分)', line):
            return False
        return True


if __name__ == '__main__':
    ChineseWord().main()
