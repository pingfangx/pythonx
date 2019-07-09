from typing import List


class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        """
        让我们回忆一下两个数的和
        * 双重遍历不可取
        * 可以用差
        * 可以将差保存在字典中

        现在这里有序的
        想到可以 high 一直后移，如果大于 target 则 high 往回移，注意可能不只需要回移一位

        """
        low = 0
        high = 1
        while high < len(numbers):
            sum = numbers[low] + numbers[high]
            if sum == target:
                return [low + 1, high + 1]
            elif sum < target:
                # 如果小于，继续移动
                if high + 1 < len(numbers):
                    high += 1
                else:
                    low += 1
            else:
                # 如果大于，则 low+1 且 high 需要往回移，直到移到和小于 target
                low += 1
                while numbers[low] + numbers[high] > target:
                    high -= 1


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
