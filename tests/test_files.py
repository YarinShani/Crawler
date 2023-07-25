import os
import math
import unittest


class TestCrawler(unittest.TestCase):
    def test_files(self, max_urls, max_d):

        for i in range(0, max_d):
            _, _, files = next(os.walk(f"./scraped_data/{i}"))
            file_count = len(files)
            assert file_count == math.pow(max_urls, i)

