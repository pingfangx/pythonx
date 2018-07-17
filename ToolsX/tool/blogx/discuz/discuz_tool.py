import os
import shutil
import time

from xx import iox


class DiscuzTool:
    workspace_dir = r'D:\file\program\webpage\www.pingfangx.com'
    file_list = [
        'index.php',  # 入口
        'favicon.ico',  # 图标
        'template/default/common/header_common.htm',  # 模板
        'template/default/common/footer.htm',  # 模板
        'source/include/spacecp/spacecp_profile.php',  # 禁止待审核用户修改资料
        'source/module/home/home_space.php',  # 因为转 https，在 .htaccess 中的跳转导致编码不正常，跳转至中文用户名空间失败
        'source/module/forum/forum_ajax.php',  # 用户名不能为纯数字
        'source/function/function_attachment.php',  # 好像是为了支持 apk 类型
        'source/class/class_member.php',  # 用户名不能为纯数字
        'source/class/discuz/discuz_error.php',  # 好像为了报错提醒
        'source/class/discuz/discuz_application.php',  # https 的判断
        'static/image/common/watermark.png',  # 水印
        'static/image/mobile/style.css',  # 样式
        'static/image/mobile/images/logo.png',  # logo
        'uc_server/avatar.php',  # https 判断
    ]

    def main(self):
        action_list = [
            ['退出', exit],
            ['还原文件', self.resotre_file, r'E:\file\download\thunder\Discuz_X3.2_SC_UTF8\upload'],
            ['更新时间', self.update_time],
        ]
        iox.choose_action(action_list)

    def resotre_file(self, source_dir):
        """还原为原版文件，用于 git 比较改了些什么东西"""
        for file in self.file_list:
            source_file = source_dir + os.path.sep + file
            target_file = self.workspace_dir + os.path.sep + file
            print(f'{source_file}→{target_file}')
            if not os.path.exists(source_file):
                print(f'{source_file} not exist.')
                return
            if not os.path.exists(target_file):
                print(f'{target_file} not exist.')
                return
            # 复制
            shutil.copy(source_file, target_file)

    def update_time(self):
        """更新时间，用于一起上传，方便 discuz 后台的文件校验"""
        now = time.time()
        for file in self.file_list:
            file = self.workspace_dir + os.path.sep + file
            print(f'update {file}')
            os.utime(file, (now, now))


if __name__ == '__main__':
    DiscuzTool().main()
