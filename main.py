import os
import shutil
import sys
import argparse

from configparser import ConfigParser

from models.crawler import Crawler
from models.logger import Logger
from models.pool import Pool
from utils.utils import valid_url

config = ConfigParser()
config.read("utils/config.cfg")


def clear_output_folder(folder):
    if os.path.isdir(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))


def execute_crawler(max_urls_per_page, max_depth, uniqueness, output_folder, logger, using_threads=False):
    if using_threads:
        pool = Pool(max_urls_per_page, max_depth, uniqueness, output_folder, logger)
        pool.run(start_url, 0)
    else:
        crawler = Crawler(max_depth, max_urls_per_page, uniqueness, output_folder, logger)
        crawler.run_crawler(start_url)


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Please enter a valid input:")
        print("<start_url> <max_amount> <max_depth> <uniqueness>")
        print("or")
        print("-url <start_url> -a <max_amount> -d <max_depth> -u <uniqueness>")
        sys.exit(1)

    if len(sys.argv) > 5:
        parser = argparse.ArgumentParser()

        parser.add_argument("-u", "--start_url", dest="start_url",
                            help="The URL to start the process with.")
        parser.add_argument("-a", "--max_amount", dest="max_urls_per_page",
                            help="The maximal amount of different URLs to extract from the page.", type=int)
        parser.add_argument("-d", "--max_depth", dest="max_depth",
                            help="How deep the process should run (depth factor).", type=int)
        parser.add_argument("-q", "--uniqueness", dest="uniqueness", default=True,
                            help="Boolean flag indicating cross-level uniqueness", type=bool)

        args = parser.parse_args()
        start_url = args.start_url
        max_urls_per_page = args.max_urls_per_page
        max_depth = args.max_depth
        uniqueness = args.uniqueness

    else:
        start_url = valid_url(sys.argv[1])
        max_urls_per_page = int(sys.argv[2])
        max_depth = int(sys.argv[3])
        uniqueness = bool(sys.argv[4])

    output_folder = config.get("configuration", "output_folder")

    clear_output_folder(output_folder)

    logger = Logger()
    logger.start()

    # if you want to run the execution with thread, pass True as the last argument
    execute_crawler(max_urls_per_page, max_depth, uniqueness, output_folder, logger)

    logger.end()

