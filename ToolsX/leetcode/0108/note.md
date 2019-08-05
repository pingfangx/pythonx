# 学习并分析复杂度
在[讨论的回复](https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/discuss/35223/An-easy-Python-solution/195655)
中 fortuna911 提到
> This might be nice and easy to code up, but the asymptotic complexity is bad. Slices take O(s) where 's' is the size of the slice.
Therefore this algorithm has runtime O(n lg n), space O(n), wheras it could be done in O(n) runtime and O(lg n) space complexity if passing indices of the start and end of string instead of the slices directly.


这里的 O(n log n) O(n)
和 O(n) O(log n)
是如何分析的呢，学习后已写在 0118_2 和 0188_3 中