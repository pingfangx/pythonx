class Version:
    """记录要翻译的版本"""

    version = '3.0'
    "版本号"

    project = r'D:/workspace/TranslatorX/AndroidStudio'
    "项目路径"

    source = project + '/source'
    "OmegaT的source路径"
    target = project + '/target'
    "OmegaT的target路径"
    original = project + '/original'

    source_version = source + '/' + version
    source_version_lib = source_version + '/lib'
    source_version_lib_resource_en = source_version_lib + '/resources_en'
    source_version_lib_resource_en_messages = source_version_lib_resource_en + '/messages'

    target_version = target + '/' + version
    target_version_lib = target_version + '/lib'
    target_version_lib_resource_en_messages = target_version_lib + '/resources_en/messages'

    original_version = original + '/' + version
    original_version_lib = original_version + '/lib'
    original_version_lib_resource_en_messages = original_version_lib + '/resources_en/messages'
