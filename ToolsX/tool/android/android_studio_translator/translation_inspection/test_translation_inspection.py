# coding=utf-8
from tool.android.android_studio_translator.translation_inspection.translation_inspection import TranslationInspection

if __name__ == '__main__':
    print(TranslationInspection.inspect_space('', '你好test测试'))
    print(TranslationInspection.inspect_space('', '你好<a>test</a>测试'))
    print(TranslationInspection.inspect_space('', '你好<a>中文</a>测试'))
