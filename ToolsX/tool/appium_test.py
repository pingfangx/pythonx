import time

from appium import webdriver


class OrderRoom:
    """签约房子"""

    @staticmethod
    def run():
        """运行"""
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '7.0'
        desired_caps['deviceName'] = 'MI 5'
        desired_caps['appPackage'] = 'com.miui.calculator'
        desired_caps['appActivity'] = '.cal.CalculatorActivity'

        print('连接设备中')
        driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        print('连接成功')
        # driver.find_element_by_android_uiautomator("1").click()

        start_time = time.time()
        e = driver.find_element_by_id('btn_9_s')
        print('text=%s' % e.text)
        e.click()
        print('spend %d' % (time.time() - start_time))

        driver.quit()


def run():
    """运行"""
    OrderRoom().run()


if __name__ == '__main__':
    run()
    print('运行结束')
