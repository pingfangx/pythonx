import copy

from xx import iox


class Team:
    def __init__(self, name, win, lose):
        self.name = name
        self.win = win
        self.lose = lose

    def win_a_game(self):
        self.win += 1

    def lose_a_game(self):
        self.lose += 1

    def __str__(self):
        return f'{self.name}({self.win}-{self.lose})'

    def __repr__(self):
        return self.__str__()


class Demo:
    def __init__(self, team_list, match_list):
        self.team_list = team_list
        self.match_list = match_list

    def main(self):
        action_list = [
            ['退出', exit],
            ['输出比分', self.print_team_list, self.team_list],
            ['列出所有比赛结果', self.list_all_match_result],
        ]
        iox.choose_action(action_list)

    @staticmethod
    def print_team_list(team_list):
        print(','.join([str(team) for team in team_list]))

    def list_all_match_result(self):
        match_list = []
        for match in self.match_list:
            if len(match) == 3:
                # 已结有结果，处理结果
                name1, name2, result = match
                self.result_a_match(self.team_list, name1, name2, result)
            else:
                match_list.append(match)
        print('当前结果是')
        self.print_team_list(self.team_list)
        print()

        # 计算所有可能的结果
        result = list(range(0, len(match_list)))
        all_result = self.list_match_result(result)
        print(f'共 {len(all_result)} 种结果')

        for result in all_result:
            print(result)
            t = copy.deepcopy(self.team_list)
            length = len(match_list)
            for i in range(length):
                match = match_list[i]
                name1, name2 = match
                self.result_a_match(t, name1, name2, result[i])
                if result[i]:
                    print(f'{name1} win, {name2} lose')
                else:
                    print(f'{name1} lose, {name2} win')
            self.print_team_list(t)
            print()

    def result_a_match(self, team_list, team_name1, team_name2, result):
        team_1 = self.find_team_by_name(team_list, team_name1)
        team_2 = self.find_team_by_name(team_list, team_name2)
        if result:
            team_1.win_a_game()
            team_2.lose_a_game()
        else:
            team_1.lose_a_game()
            team_2.win_a_game()

    def list_match_result(self, result: list, offset=0):
        # 将 offset 场置为 true 或 false
        r1 = list(result)
        r2 = list(result)
        r1[offset] = True
        r2[offset] = False
        if offset == len(result) - 1:
            # 如时是最后一场，返回
            return [
                r1,
                r2
            ]
        else:
            # 如时不是最后一场，则将两个分枝的结果合到一个 list 中
            result = []
            result.extend(self.list_match_result(r1, offset + 1))
            result.extend(self.list_match_result(r2, offset + 1))
            return result

    @staticmethod
    def find_team_by_name(team_list, team_name) -> Team:
        for team in team_list:
            if team.name == team_name:
                return team
        print(f'can not find tame:{team_name}')
        exit()


if __name__ == '__main__':
    init_team_list = [
        Team('RNG', 3, 0),
        Team('C9', 1, 2),
        Team('VIT', 1, 2),
        Team('GG', 1, 2),
    ]

    init_match_list = [
        ('VIT', 'RNG', True),
        ('GG', 'C9', False),
        ('VIT', 'GG', True),
        ('C9', 'RNG'),
        ('C9', 'VIT'),
        ('RNG', 'GG'),
    ]
    Demo(init_team_list, init_match_list).main()
