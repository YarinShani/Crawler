class Page:
    def __init__(self, url, depth, max_links, uniqueness):
        self.url = url
        self.depth = depth
        self.max_links = max_links
        self.uniqueness = uniqueness
        self.innerLinks = set()
        self.content = ""
        self.links_to_crawl = set()


