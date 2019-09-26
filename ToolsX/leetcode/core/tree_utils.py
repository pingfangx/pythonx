from typing import List


def to_tree_graph(root) -> str:
    return '\n'.join(to_level_array(root))


def to_level_array(root) -> List[str]:
    """转为分层的数组"""
    if not root:
        return ['None']
    if root.left or root.right:
        left = to_level_array(root.left)
        right = to_level_array(root.right)
        return merge_level_array(root, left, right)
    else:
        return [str(root.val)]


def merge_level_array(root, left: List[str], right: List[str]) -> List[str]:
    parent = str(root.val)
    if not left and not right:  # 没有左右
        return [parent]
    width = max(_max_line_width(left), _max_line_width(right), len(parent))
    n = max(len(left), len(right))
    while len(left) < n:
        left.append('')
    while len(right) < n:
        right.append('')
    left = [_fill_width(i, width) for i in left]
    right = [_fill_width(i, width) for i in right]
    res = [_fill_width(parent, width * 2 + 4)]
    for l, r in zip(left, right):
        res.append(l + ' ' * 4 + r)
    return res


def _max_line_width(lines: List[str]) -> int:
    if not lines:
        return 0
    return len(max(lines, key=lambda x: len(x)))


def _fill_width(line: str, width: int) -> str:
    n = width - len(line)
    left = n // 2
    right = n - left
    return ' ' * left + line + ' ' * right


if __name__ == '__main__':
    from leetcode import TreeNode

    print(to_tree_graph(TreeNode.from_num(123456)))
    print(to_tree_graph(TreeNode.from_array([3, None, 30, 10, None, None, 15, None, 45])))
