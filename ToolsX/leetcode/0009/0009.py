class Solution:
    def isPalindrome(self, x: int) -> bool:
        """
        想到几种
        一是收集数字，再判断
        二是通过弹出数字的时候就反转
        三是求出数字位数

        >>> Solution().isPalindrome(121)
        True
        >>> Solution().isPalindrome(-121)
        False
        >>> Solution().isPalindrome(10)
        False
        >>> Solution().isPalindrome(0)
        True
        """
        if x < 0:
            return False
        nums = []
        while x:
            nums.append(x % 10)
            x //= 10
        mid = len(nums) // 2
        for i in range(mid):
            if nums[i] != nums[-i - 1]:
                return False
        return True


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
