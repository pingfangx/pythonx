from typing import List


def binary_search1(nums: List[int], target: int):
    """
    判断顺序为 = < >
    """
    left = 0
    right = len(nums) - 1
    loop_times = compare_times = 0
    while left <= right:
        loop_times += 1
        # 向下取整，靠近左边
        mid = left + (right - left) // 2
        if nums[mid] == target:
            compare_times += 1
            return mid, loop_times, compare_times
        elif nums[mid] < target:
            compare_times += 2
            right = mid - 1
        else:
            compare_times += 2
            left = mid + 1
    return -1, loop_times, compare_times


def binary_search2(nums: List[int], target: int):
    """
    判断顺序为 < > =
    """
    left = 0
    right = len(nums) - 1
    loop_times = compare_times = 0
    while left <= right:
        loop_times += 1
        # 向下取整，靠近左边
        mid = left + (right - left) // 2
        if nums[mid] < target:
            compare_times += 1
            left = mid + 1
        elif nums[mid] > target:
            compare_times += 2
            right = mid - 1
        else:
            compare_times += 2
            return mid, loop_times, compare_times
    return -1, loop_times, compare_times


def binary_search3(nums: List[int], target: int):
    """
    判断顺序为 > < =
    """
    left = 0
    right = len(nums) - 1
    loop_times = compare_times = 0
    while left <= right:
        loop_times += 1
        # 向下取整，靠近左边
        mid = left + (right - left) // 2
        if nums[mid] > target:
            compare_times += 1
            right = mid - 1
        elif nums[mid] < target:
            compare_times += 2
            left = mid + 1
        else:
            compare_times += 2
            return mid, loop_times, compare_times
    return -1, loop_times, compare_times


def binary_search4(nums: List[int], target: int):
    """
    用 < 退出时 left==right
    """
    left = 0
    right = len(nums)  # 不需要 -1
    loop_times = compare_times = 0
    while left < right:
        loop_times += 1
        # 向下取整，靠近左边
        mid = left + (right - left) // 2
        if nums[mid] < target:
            compare_times += 1
            left = mid + 1
        elif nums[mid] > target:
            compare_times += 2
            right = mid  # 不需要 -1
        else:
            compare_times += 2
            return mid, loop_times, compare_times
    return -1, loop_times, compare_times


def test_method(method, n, reverse=False):
    """
    创建一个 [0,n] 的数组，然后在该数组中依次搜索 0-n
    """
    nums = [i for i in range(n)]
    nums.sort(reverse=reverse)
    ls = cs = 0
    # print(f'test {method.__name__}({nums},i)')
    # print(method.__doc__.strip())
    for i in range(n):
        ans, loop_times, compare_times = method(nums, i)

        ls += loop_times
        cs += compare_times
        # print(f'search {i},result {ans},loop {loop_times},compare {compare_times}')
    # print(f'sum loop_times {ls},sum compare_times {cs}')
    return ls, cs


def test():
    method_list = [
        binary_search1,
        binary_search2,
        binary_search3,
        binary_search4,
    ]
    for method in method_list:
        print(f'test {method.__name__} {method.__doc__.strip()}')
        ls = cs = 0
        start = 1
        stop = 101
        reverse = False
        for i in range(start, stop):
            loop_times, compare_times = test_method(method, i, reverse)
            ls += loop_times
            cs += compare_times
        print(f'[{start},{stop - 1}],reverse={reverse},sum loop_times {ls},sum compare_times {cs}')


if __name__ == '__main__':
    test()
