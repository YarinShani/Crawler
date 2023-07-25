from bs4 import BeautifulSoup


class UrlExtractor:
    def __init__(self):
        self.crawled_urls = set()

    def check_uniqueness(self, url):
        return self.crawled_urls.__contains__(url)

    def add_crawler_url(self, url):
        self.crawled_urls.add(url)

    @staticmethod
    def extract_urls(html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        urls = set()
        for link in soup.find_all("a", href=True):
            urls.add(link["href"])

        return urls
