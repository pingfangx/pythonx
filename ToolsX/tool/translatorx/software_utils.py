import os
import re
import shutil
import subprocess
import zipfile
from typing import Callable, List

import common_utils
import translatorx_utils
from software import Software
from translatorx_config import TranslatorXConfig

"""
软件相关工具，参数一般为 Software
那么为什么不直接作为 Software 的子类呢？
"""


def get_software_list(config_file='') -> List[Software]:
    """根据配置获取软件列表"""
    config = TranslatorXConfig(config_file)
    software_home_path = config.get_software_home_path()
    omegat_workspace = config.get_omegat_workspace()
    software_name_list = config.get_software_name_list()
    software_version_list = config.get_software_version_list()
    translation_locale = config.get_translation_locale()
    if not translation_locale:
        translation_locale = Software.DEFAULT_LOCALE

    print('读取配置为')
    print(f'软件安装目录 {software_home_path}')
    print(f'OmegaT 工作目录 {omegat_workspace}')
    if not os.path.exists(omegat_workspace):
        print('OmegaT 工作目录不在在')
    print(f'翻译区域 {translation_locale}')
    print()

    software_list = []
    for i, name in enumerate(software_name_list):
        if i >= len(software_version_list):
            # 取最后一个
            version = software_version_list[-1]
        else:
            # 取对应版本
            version = software_version_list[i]
        if '-' in version:
            version, release_version = version.split('-')
        else:
            release_version = 1
        software = Software(
            name=name,
            version=version,
            release_version=release_version,
            software_home_path=software_home_path,
            omegat_workspace=omegat_workspace,
            translation_locale=translation_locale,
        )
        software_list.append(software)
    return software_list


def extract_jar_to_source_dir(software: Software):
    """将 jar 解压到 source 目录"""
    out_dir = software.omegat_workspace_source_resources_en
    common_utils.remove_dir(out_dir)
    jars = software.original_jar_list
    jars = list(filter(lambda x: os.path.exists(x), jars))
    for i, jar in enumerate(jars):
        print(f'解压 jar {i + 1}/{len(jars)}/{len(software.original_jar_list)}:{jar}')
        with zipfile.ZipFile(jar) as zip_file:
            namelist = zip_file.namelist()
            for name in namelist:
                if re.search(software.ignore_file_pattern, name):
                    # print(f'过滤文件 {name}')
                    continue
                print('解压 %s 到 %s' % (name, out_dir))
                zip_file.extract(name, out_dir)


def clean_target_dir(software: Software):
    """清空 target 目录

    因为新版本可能减少部分文件，所以清空一个
    """
    common_utils.remove_dir(software.omegat_workspace_target_software)


def collect_tip_names(software: Software):
    """收集 tips 文件名"""
    tips_sources_dir = os.path.join(software.omegat_workspace_source_resources_en, 'tips')
    tip_names_set = set()  # 过滤重名
    for dirpath, dirnames, filenames in os.walk(tips_sources_dir):
        for file in filenames:
            name, ext = os.path.splitext(file)
            if ext == '.html':
                tip_names_set.add(name)

    # 输出，在 txt 中有换行才能分隔
    lines = [f'{name}\n\n' for name in sorted(tip_names_set)]
    tip_names_file = os.path.join(software.omegat_workspace_source_software, 'tip_names', 'TipNames.txt')

    common_utils.check_and_create_dir(tip_names_file)
    with open(tip_names_file, 'w') as f:
        f.writelines(lines)
    print(f'保存到 {tip_names_file}')


def zip_translation_jar(software: Software):
    """打包汉化包"""
    translation_dir = software.omegat_workspace_target_resources_en
    target_jar = software.translation_jar_path
    zip_jar(translation_dir, target_jar, software.get_file_zip_name)


def zip_jar(source_dir, target_jar, zip_name_callback: Callable = None):
    """打包文件

    :param source_dir:打包目录
    :param target_jar: 打包到的文件
    :param zip_name_callback: 处理要压缩文件名的回调
    :return:
    """
    print(f'将 {source_dir} 压缩到 {target_jar}')
    # 移除 target
    if os.path.exists(target_jar):
        os.remove(target_jar)
    common_utils.check_and_create_dir(target_jar)
    translation_file_list = []
    for dirpath, dirnames, filenames in os.walk(source_dir):
        for file_name in filenames:
            path = os.path.join(dirpath, file_name)
            translation_file_list.append(path.replace(source_dir, '').replace('\\', '/').lstrip('/'))
    with zipfile.ZipFile(target_jar, 'a') as zip_file:
        for file in translation_file_list:
            zip_name = None
            if zip_name_callback is not None:
                zip_name = zip_name_callback(file)
            if not zip_name:
                zip_name = file
            # print(f'压缩 {file} 为 {zip_name}')
            zip_file.write(os.path.join(source_dir, file), zip_name)
    print('压缩完成')


def camel_word_to_words(word):
    """驼峰转为多个单词，大写缩写及最后一位保持不变
    >>> camel_word_to_words('CtrlD')
    'ctrl D'

    >>> camel_word_to_words('LocalVCS')
    'local VCS'

    >>> camel_word_to_words('F4')
    'F4'
    """
    # 将每个单词（以大写开头，接多个小写）后面补充空格
    result = re.sub('[A-Z][a-z]+', lambda m: m.group().lower() + ' ', word).rstrip()
    # 少数情况，要再处理一次
    result = result.replace('Ifor', 'I for') \
        .replace('movefile', 'move file') \
        .replace('html 5outline', 'html5 outline')
    return result


def convert_tip_file_names(software: Software):
    """转换 tips"""
    source_file = os.path.join(software.omegat_workspace_target_software, 'IdeTipsAndTricks',
                               'IdeTipsAndTricks_en_zh_CN.properties')
    if not os.path.exists(source_file):
        print(f'文件不存在 {source_file}')
        return
    translation_dict = translatorx_utils.get_translation_dict_from_file(source_file)
    translation_dict = {k: translatorx_utils.unicode_str_to_chinese(v) for k, v in translation_dict.items()}
    target_file = os.path.join(software.omegat_workspace, 'tm', "tip_file_names_" + software.name + ".tmx")
    translatorx_utils.save_translation_dict_to_omegat_file(translation_dict, target_file)


def copy_translation_to_work_dir(software: Software):
    """复制汉化包到工作目录"""

    src = software.translation_jar_path
    if not os.path.exists(src):
        print(f'汉化包不在在 {src}')

        # 社区版使用正式版的汉化包
        src = src.replace('-C', '')
        if not os.path.exists(src):
            print(f'汉化包不在在 {src}')
            return
        else:
            print(f'使用非社区版汉化包 {src}')

    dst = os.path.join(software.home_path, 'lib', software.translation_jar_name)

    # 尝试删除旧版汉化包
    lib_dir = os.path.join(software.home_path, 'lib')
    for file in os.listdir(lib_dir):
        # 该判断还会删除较大区域，比如判断 zh 时 zh_CN 也会一并删除，反之则不会
        if file.startswith(f'resources_{software.locale}') and file.endswith('.jar'):
            file_path = os.path.join(lib_dir, file)
            try:
                os.remove(file_path)
                print('删除旧版汉化包成功', file_path)
            except PermissionError:
                print('删除旧版汉化包失败', file_path)

    print(f'复制 {src} -> {dst}')
    shutil.copyfile(src, dst)


def open_software(software: Software):
    """打开软件"""
    bin_path = os.path.join(software.home_path, 'bin', software.get_execute_file_name())
    if not os.path.exists(bin_path):
        print(f'不在在 {bin_path}')
        return
    cmd = f'start {bin_path}'
    print(cmd)
    subprocess.call(cmd, shell=True)


def print_name_and_version(software: Software):
    """输出名字和版本

    可用来填写 commit 信息等
    """
    print(f'{software.name} {software.version}')


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
