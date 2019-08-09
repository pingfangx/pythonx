from leetcode.algorithm.trick.check_sum.check_sum import CheckSum


def test_udp_check_sum():
    """
        该示例来自《计算机网络》 5.2.2 图 5-7
        书中求得和       10010110    11101101
    """
    # 12 字节伪首部
    check_sum = CheckSum()
    check_sum.add_ip('153.19.8.104')  # 源 IP 地址
    check_sum.add_ip('171.3.14.11')  # 目的 IP 地址
    check_sum.add_int(0)  # 0
    check_sum.add_int(17)  # 17
    check_sum.add_int(15, 2)  # UDP 长度

    # 8 字节 UDP 首部
    check_sum.add_int(1087, 2)  # 源端口
    check_sum.add_int(13, 2)  # 目的端口
    check_sum.add_int(15, 2)  # 用户数据报长度
    check_sum.add_int(0, 2)  # 检验和

    # 7字节数据
    check_sum.add_int(0b01010100)
    check_sum.add_int(0b01000101)
    check_sum.add_int(0b01010011)
    check_sum.add_int(0b01010100)

    check_sum.add_int(0b01001001)
    check_sum.add_int(0b01001110)
    check_sum.add_int(0b01000111)
    check_sum.add_int(0)  # 补1字节 0

    check_sum.check(18)


if __name__ == '__main__':
    test_udp_check_sum()
