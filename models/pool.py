import concurrent.futures
import queue
import threading
from urllib.parse import urljoin

from models.downloader import UrlDownloader
from models.extractor import UrlExtractor
from models.manager import Manager
from models.page import Page
from utils.utils import is_url


class Pool:
    def __init__(self, max_links, max_depth, uniqueness, output_folder, logger):
        self.max_links = max_links
        self.max_depth = max_depth
        self.uniqueness = uniqueness
        self.output_folder = output_folder
        self.logger = logger
        self.crawled_urls = set()
        self.downloader = UrlDownloader(self.output_folder)
        self.extractor = UrlExtractor()
        self.q = Manager()
        self.lock = threading.Lock()

    def process_page(self, page):
        lock = threading.Lock()
        lock.acquire()
        i = 0
        lock.release()
        depth = page.depth + 1

        for link_url in page.innerLinks:
            if i < page.max_links:
                fixed_link = urljoin(page.url, link_url)
                if not is_url(fixed_link):
                    continue

                try:
                    content = self.download_html_content(fixed_link, depth)

                    if content:
                        lock.acquire()
                        i += 1
                        lock.release()

                        if depth < self.max_depth:
                            urls = self.extractor.extract_urls(content)
                            new_page = Page(fixed_link, depth, page.max_links, page.uniqueness)
                            new_page.innerLinks = urls
                            self.q.put(new_page)

                        elif depth == self.max_depth and i == page.max_links:
                            return True

                    else:
                        continue
                except Exception as e:
                    print(f"Error downloading page {fixed_link}: {e}")

            else:
                return True

        return True

    def download_html_content(self, url, depth):
        try:
            if self.uniqueness:
                if not self.extractor.check_uniqueness(url):
                    html_content = self.downloader.download_page(url, depth)  # page's content
                    self.extractor.add_crawler_url(url)
                else:
                    return None
            else:
                html_content = self.downloader.download_page(url, depth)  # page's content

            return html_content

        except Exception as e:
            self.logger.error(f"Exception: {e}")

    def link_extractor(self, url, depth):
        try:
            html_content = self.download_html_content(url, depth)

            if not html_content:
                return None

            urls = self.extractor.extract_urls(html_content)
            curr_page = Page(url, depth, self.max_links, self.uniqueness)
            curr_page.innerLinks = urls
            curr_page.content = html_content

            return curr_page
        except Exception as e:
            self.logger.error(f"Exception: {e}")
            return None

    def run(self, url, depth):
        # Add the first page to the queue
        first_page = self.link_extractor(url, depth)
        self.q.put(first_page)

        # Number of threads in the ThreadPool
        num_threads = self.max_links * self.max_depth

        responses = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            while True:
                try:
                    page = self.q.get()
                    responses.append(executor.submit(self.process_page, page))
                    if all(r.done() for (r) in responses):
                        break

                except queue.Empty:
                    # No more pages in the queue, break the loop
                    break

