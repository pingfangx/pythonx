import unittest


class BasePipelineTest(unittest.TestCase):
    """测试 pipeline"""
    pipeline = None

    def test_create_table(self):
        self.pipeline.open_spider(None)
