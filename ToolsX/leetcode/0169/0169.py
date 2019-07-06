from typing import List


class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        """
        只能想到累计
        """
        counts = {}
        for i in nums:
            if i in counts:
                counts[i] += 1
            else:
                counts[i] = 1
        max_key = max_value = 0
        for k, v in counts.items():
            if max_value < v:
                max_value = v
                max_key = k
        return max_key


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
