def choose_action(action_list, loop=False):
    """
    选择操作

    :param action_list: 操作列表，每个操作格式为
    :param loop: 是否重复

    [操作名,操作对应的方法,操作对应的参数]

    可以有多个参数，直接拼在数组内即可。

    如果想用关键字参数，则将第3个参数设置为字典

    如果操作名以 '-' 开头，则表示为分隔线

    :return: None
    示例:
        action_list = [
            ['退出', exit],
            ['操作1', self.action1, 'param'],
            ['操作2', self.action2, {
                'param2': 2,
                'param1': 1
            }]
        ]
    """
    prompt = ''
    for i in range(0, len(action_list)):
        action = action_list[i]
        if isinstance(action, list) and len(action) > 0:
            if action[0].startswith('-'):
                text = action[0].lstrip('-')
                prompt += '\n\n{0}{1}{0}'.format('-' * 10, text)
            else:
                prompt += '\n%d--%s' % (i, action[0])
    if loop:
        while True:
            show_choose_action(action_list, prompt)
    else:
        show_choose_action(action_list, prompt)


def show_choose_action(action_list, prompt):
    choice = int(input('请选择操作\n%s\n' % prompt))
    if 0 <= choice < len(action_list):
        action = action_list[choice]
        if isinstance(action, list):
            if len(action) == 2:
                # 直接执行
                action[1]()
            elif len(action) > 2:
                if len(action) == 3:
                    param = action[2]
                    if isinstance(param, dict):
                        # 如果只有3个参数，且第3个参数是字典，将其认为是关键字参数
                        action[1](**param)
                        return

                params = action[2:]  # 带参数
                action[1](*params)
