from uiautomator import Device


class MyDevice(Device):
    def __init__(self, pkg_name):
        super().__init__()
        self.pkg_name = pkg_name

    def find_view_by_id(self, view_id):
        if 'id/' not in view_id:
            view_id = 'id/' + view_id
        if ':' not in view_id:
            view_id = self.pkg_name + ':' + view_id
        return self(resourceId=view_id)


class OrderRoom:
    """签约房子"""

    @staticmethod
    def run():
        """运行"""
        d = MyDevice('com.miui.calculator')
        print('开始操作')
        d.find_view_by_id('id/btn_c_s').click()
        d(text='1').click()
        d.find_view_by_id('id/btn_plus_s').click()
        d(text='2').click()
        d.find_view_by_id('id/btn_equal_s').click()


def run():
    """运行"""
    OrderRoom().run()


if __name__ == '__main__':
    run()
    print('运行结束')
