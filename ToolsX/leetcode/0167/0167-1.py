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

        1
        看了讨论，思路不正确啊，不取 high 从头开始移，只需要从最后移就可以了
        """
        low = 0
        high = len(numbers) - 1
        while low < high:
            sum = numbers[low] + numbers[high]
            if sum == target:
                return [low + 1, high + 1]
            elif sum < target:
                # 如果小于，增加 low
                low += 1
            else:
                # 如果大于，high 回移
                high -= 1


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
