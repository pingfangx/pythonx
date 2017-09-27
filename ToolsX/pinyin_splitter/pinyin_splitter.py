import re

from xx import filex
from xx import iox


class PinyinSplitter:
    """
    分割拼音，用来分割大观楼长联的
    拼音来自[昆明大观楼长联赏析](http://www.scsynsh.com/Article/ShowArticle.asp?ArticleID=93)  
    有几个字注音不准，根据[《大观楼长联》（孙髯翁）朗诵践离 视频蓑衣孤客](http://baidu.iqiyi.com/watch/7073261620349673234.html?page=videoMultiNeed)手动修改了一下。
    相关博文
    [大观楼长联原文、注音及释义](http://blog.pingfangx.com/2386.html)
    [正则匹配带声调的汉语拼音](http://blog.pingfangx.com/2387.html)
    """

    def main(self):
        text = '''
        五(wǔ)百里(bǎilǐ)滇池(diānchí)奔(bēn)来(lái)眼底(yǎndǐ)，披(pī)襟(jīn)岸(àn)帻(zé)，喜(xǐ)茫茫(mángmáng)空阔(kōngkuò)无边(wúbiān)。看(kàn)东(dōng)骧(xiāng)神(shén)骏(jùn)，西(xī)翥(zhù)灵(líng)仪(yí)，北(běi)走(zǒu)蜿蜒(wānyán)，南(nán)翔(xiáng)缟素(gǎosù)。高人(gāorén)韵(yùn)士(shì)，何妨(héfáng)选(xuǎn)胜(shèng)登临(dēnglín)，趁(chèn)蟹(xiè)欤(yú)螺(luó)洲(zhōu)，梳(shū)裹(guǒ)就(jiù)风(fēng)鬟(huán)雾(wù)鬓(bìn)，更(gèng)频(pín)天(tiān)苇(wěi)地(dì)，点缀(diǎnzhuì)些(xiē)翠(cuì)羽(yǔ)丹霞(dānxiá)，莫(mò)辜负(gūfù)四围(sìwéi)香(xiāng)稻(dào)，万顷(wànqǐng)晴(qíng)沙(shā)，九(jiǔ)夏(xià)芙蓉(fúróng)，三春(sānchūn)杨柳(yángliǔ)；
        数千年(shùqiānnián)往事(wǎngshì)注(zhù)到(dào)心头(xīntóu)，把酒(bǎjiǔ)临(lín)虚(xū)，叹(tàn)滚滚(gǔngǔn)英雄(yīngxióng)谁(shuí)在(zài)？想(xiǎng)汉(hàn)习(xí)楼船(lóuchuán)，唐(táng)标(biāo)铁(tiě)柱(zhù)，宋(sòng)挥(huī)玉(yù)斧(fǔ)，元(yuán)跨(kuà)革囊(génáng)，伟(wěi)烈(liè)丰(fēng)功(gōng)，费尽(fèijìn)移(yí)山(shān)心力(xīnlì)，尽(jìn)珠帘(zhūlián)画(huà)栋(dòng)，卷(juǎn)不及(bùjí)暮(mù)雨(yǔ)朝(zhāo)云(yún)，便(biàn)断(duàn)碣(jié)残(cán)碑(bēi)，都(dōu)付与(fùyǔ)苍(cāng)烟(yān)落照(luòzhào)，只(zhǐ)赢得(yíngdé)几(jǐ)杵(chǔ)疏(shū)钟(zhōng)，半(bàn)江(jiāng)渔火(yúhuǒ)，两(liǎng)行(háng)秋(qiū)雁(yàn)，一(yì)枕(zhěn)清(qīng)霜(shuāng)。
        '''
        action_list = [
            ['退出', exit],
            ['过滤字与拼音', self.filter, text, 'data/pinyin.txt'],
        ]
        iox.choose_action(action_list)

    @staticmethod
    def filter(text, result_file=None):
        p_word = re.compile(r'([，。？]?)(.+?)\((.+?)\)')
        for line in text.split('\n'):
            word_list = list()
            pinyin_list = list()
            line = line.strip()
            match_list = re.findall(p_word, line)
            for match in match_list:
                symbol, word, pinyin = match
                if symbol:
                    # 添加标点符号
                    word_list.append(symbol)
                    pinyin_list.append(symbol)
                if len(word) > 1:
                    split_pinyin_list = PinyinSplitter.split_pinyin(pinyin)
                    if len(word) != len(split_pinyin_list):
                        print('汉字与拼音长度不匹配')
                        print(match)
                        return
                    # 添加多个字
                    word_list.extend(word)
                    pinyin_list.extend(split_pinyin_list)
                else:
                    # 添加一个字
                    word_list.append(word)
                    pinyin_list.append(pinyin)
            string = '\t'.join(['%5s' % i for i in pinyin_list])
            print(string)
            if result_file:
                filex.write(result_file, string + '\n', mode='a')

            string = '\t'.join(['%5s' % i for i in word_list])
            if result_file:
                filex.write(result_file, string + '\n', mode='a')
            print(string)

    @staticmethod
    def split_pinyin(pinyin):
        """分割拼音"""
        result = list()
        while pinyin:
            pinyin, last_pinyin = PinyinSplitter.get_last_pinyin(pinyin)
            result.insert(0, last_pinyin)
        return result

    @staticmethod
    def get_last_pinyin(pinyin):
        """
        获取最后一个拼音，返回除最后一个拼音外剩下的拼音，以及最后一个拼音
        :param pinyin: 要截取的字符串
        :return: (剩余拼音,最后一个拼音)
        """
        initial_consonant = 'zh|ch|sh|[bpmfdtnlgkhjqxzcsryw]'
        # 前面是声母，后面不能跟声母
        p_pinyin = re.compile(r'(?<![zcs])(%s)(?!%s)+' % (initial_consonant, initial_consonant))
        # 如zhi chi shi ，要加上这个判断才能匹配出 zhi ，否则会直接认为是 hi
        p_pinyin2 = re.compile(r'[^zcs]')
        length = len(pinyin)
        # 从1开始，因为一个声母不算拼音
        for i in range(1, length):
            if i == length - 1:
                # 最后一个单词了
                return None, pinyin
            else:
                sub_word1 = pinyin[-i - 1:]
                sub_word2 = pinyin[-i - 2:-i - 1]
                if re.match(p_pinyin, sub_word1) and re.match(p_pinyin2, sub_word2):
                    return pinyin[:length - len(sub_word1)], sub_word1


if __name__ == '__main__':
    PinyinSplitter().main()
