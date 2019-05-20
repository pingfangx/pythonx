from xx import iox


class LoanCal:
    def main(self):
        action_list = [
            ['退出', exit],
            ['计算 714 高炮', self.cal_714],
            ['计算 55 高炮', self.cal_55],
        ]
        iox.choose_action(action_list)

    def cal_714(self):
        self.cal(1000, 700, 1100, 7)
        self.cal(2000, 1600, 2000, 14)

    def cal_55(self):
        self.cal(1000, 500, 1200, 5)

    def cal(self, loan, get, repay, days):
        """

        :param loan: 借款
        :param get: 得款
        :param repay: 还款
        :param days: 还款天数
        :return:
        """
        print(f'借 {loan},得 {get}；{days} 天后还 {repay}')
        # 每天利息
        interest_day = (repay - get) / get / days
        interest_week = interest_day * 7
        interest_month = interest_day * 30
        interest_year = interest_day * 360
        print(f'日利率 {percent(interest_day)}')
        print(f'周利率 {percent(interest_week)}')
        print(f'月利率 {percent(interest_month)}')
        print(f'年利率 {percent(interest_year)}')

        # 检查利息
        interest_check = interest_day * days
        repay_check = get * (1 + interest_check)
        print(f'{days} 天利率 {percent(interest_check)}, 如果借 {get}, {days} 天后需还 {repay_check}')

        # 计算坏帐率
        print(f'每成功一人获利 {percent(interest_day)}')
        # 成功 * 日利率 = 失败 * 1
        # (1-x)*interest=x
        # x=interest/(1+interest)
        doubtful_radio = interest_day / (1 + interest_day)
        success_radio = 1 - doubtful_radio
        print(f'{percent(success_radio)} * {percent(interest_day)} = {percent(success_radio * interest_day)}')
        print(f'只要坏帐率低于 {percent(doubtful_radio)} 即可暴利')


def percent(x):
    return f'{x * 100}%'


if __name__ == '__main__':
    LoanCal().main()
