/**
 * @author pingfangx
 * @date 2019/7/7
 */
class Solution {
    /**
     * 这个这么快么，可是耗时多，可能是不应该用 long 去存
     * Runtime: 1 ms, faster than 100.00% of Java online submissions for Reverse Integer.
     * Memory Usage: 33.4 MB, less than 7.89% of Java online submissions for Reverse Integer.
     */
    public int reverse(int x) {
        long r = 0;
        int symbol;
        if (x < 0) {
            x = -x;
            symbol = -1;
        } else {
            symbol = 1;
        }
        while (x > 0) {
            r *= 10;
            r += x % 10;
            x /= 10;
        }
        r *= symbol;
        if (r < Integer.MIN_VALUE || r > Integer.MAX_VALUE) {
            return 0;
        }
        return (int) r;
    }
}
