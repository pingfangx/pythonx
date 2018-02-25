import json


def parse(data, sort=True):
    """
    解析一个 json 为类的属性
    如
    {
        a:'a',
        b:1
    }
    解析为
    self.a='a'
    self.b=1

    :param data: json 字符串或字典对象
    :param sort: 是否需要排序
    :return: 返回一个字符串，用于粘贴到代码中
    """
    if isinstance(data, str):
        data = json.dumps(data)
    if not isinstance(data, dict):
        return 'data is not a dict or valid json str'

    if sort:
        keys = sorted(data.keys())
    else:
        keys = data.keys

    result = ''
    for k in keys:
        v = data[k]
        if isinstance(v, str):
            result += "self.%s='%s'\n" % (k, v)
        else:
            result += 'self.%s=%s\n' % (k, str(v))
    return result
