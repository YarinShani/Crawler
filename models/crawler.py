from urllib.parse import urljoin

from models.downloader import UrlDownloader
from models.extractor import UrlExtractor
from models.manager import Manager
from models.page import Page
from utils.utils import is_url


class Crawler:
    pages = set()

    def __init__(self, max_depth, max_urls_per_page, uniqueness, output_folder, logger):
        self.max_depth = max_depth
        self.max_urls_per_page = max_urls_per_page
        self.uniqueness = uniqueness
        self.output_folder = output_folder
        self.crawled_urls = set()
        self.downloader = UrlDownloader(self.output_folder)
        self.extractor = UrlExtractor()
        self.manager = Manager()
        self.logger = logger

    def run_crawler(self, url):
        depth = 0

        try:
            first_page = self.link_extractor(url, depth)
            self.manager.put(first_page)

            while not self.manager.empty():
                p: Page = self.manager.get()

                i = 0
                depth = p.depth + 1
                for link_url in p.innerLinks:
                    if i < self.max_urls_per_page:
                        fixed_link = urljoin(p.url, link_url)
                        if not is_url(fixed_link):
                            continue

                        try:
                            content = self.download_html_content(fixed_link, depth)
                            if content:
                                i += 1

                                if depth < self.max_depth:
                                    urls = self.extractor.extract_urls(content)
                                    new_page = Page(fixed_link, depth, self.max_urls_per_page, self.uniqueness)
                                    new_page.innerLinks = urls
                                    self.manager.put(new_page)

                        except Exception as err:
                            continue

                    else:
                        break

        except Exception as err:
            print(f"Error occurred: {err}")

    def link_extractor(self, url, depth):
        try:
            html_content = self.download_html_content(url, depth)
            if not html_content:
                return None

            urls = self.extractor.extract_urls(html_content)

            if self.uniqueness:
                urls.difference_update(self.crawled_urls)

            curr_page = Page(url, depth, self.max_urls_per_page, self.uniqueness)
            curr_page.innerLinks = urls
            curr_page.content = html_content

            return curr_page
        except Exception as e:
            self.logger.error(f"Exception: {e}")
            return None

    def download_html_content(self, url, depth):
        try:
            if self.uniqueness:
                if not self.extractor.check_uniqueness(url):
                    html_content = self.downloader.download_page(url, depth)  # page's content
                    self.extractor.add_crawler_url(url)
                else:
                    self.logger.info(f"url: {url}, already exists")
                    return None
            else:
                html_content = self.downloader.download_page(url, depth)  # page's content

            return html_content

        except Exception as e:
            self.logger.error(f"Exception: {e}")

    def get_max_links(self):
        return self.max_urls_per_page
