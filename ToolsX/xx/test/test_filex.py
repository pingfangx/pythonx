from unittest import TestCase

from xx import filex


class TestFilex(TestCase):
    def test_get_file_size_str(self):
        size_array = [
            -1,
            0,
            1,
            1023,
            1024,
            1025,
            1024 ** 1,
            1024 ** 2,
            1024 ** 3,
            1024 ** 4,
            1024 ** 5,
        ]
        for size in size_array:
            print(f'{size}B={filex.parse_file_size(size)}')
