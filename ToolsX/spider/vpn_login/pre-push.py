#!/usr/bin/env python
import os
import subprocess


def check_vpn_login():
    """
    检查是否登录 vpn
    本来想在提交前自动登录 vpn，但是该 hook 的调用时机为
    pre-push 钩子会在 git push 运行期间， 更新了远程引用但尚未传送对象时被调用。
    """
    shell_path = r'D:\workspace\PythonX\ToolsX\spider\vpn_login\vpn_login.py'
    """检查的脚本路径"""

    return subprocess.call(shell_path, shell=True)


print(f'hook start:{os.path.basename(__file__)}')
return_recode = check_vpn_login()
print(f'hook finish:{os.path.basename(__file__)},return code {return_recode}')
exit(return_recode)
