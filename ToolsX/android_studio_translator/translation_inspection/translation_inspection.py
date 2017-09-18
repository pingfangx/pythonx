from xx import iox
from android_studio_translator.tools import Tools
from android_studio_translator.delete_action import DeleteAction


class TranslationInspection:
    def main(self):
        pseudo_file = 'data/pseudo.tmx'
        translation_file = 'data/AndroidBundle.tmx'
        inspection_list = []
        action_list = [
            ['退出', exit],
            ['检查', self.inspect, pseudo_file, translation_file, inspection_list],
        ]
        iox.choose_action(action_list)

    def inspect(self, pseudo_file, translation_file, inspection_list):
        pseudo_dict = Tools.get_dict_from_omegat(pseudo_file)
        translation_dict = Tools.get_dict_from_omegat(translation_file)
        print('pseudo size is %d' % (len(pseudo_dict)))
        print('translation size is %d' % (len(translation_dict)))
        for en in pseudo_dict.keys():
            abbreviated_en = DeleteAction.delete_all_symbol_of_string(en, False)
            if abbreviated_en in translation_dict.keys():
                value = translation_dict[abbreviated_en]
                print('key is 【%s】,value is 【%s】' % (en, value))
                for inspection in inspection_list:
                    value = inspection(en, value)
        pass


if __name__ == '__main__':
    TranslationInspection().main()
