from xx import iox


class Demo:
    def main(self):
        action_list = [
            ['退出', exit],
            ['操作1', self.action1, 'param'],
        ]
        iox.choose_action(action_list)

    def action1(self, param):
        pass


if __name__ == '__main__':
    Demo().main()
