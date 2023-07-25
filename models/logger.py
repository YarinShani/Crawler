import logging
from datetime import datetime


class Logger(object):

    def __init__(self, name='logger', level=logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        fh = logging.FileHandler('%s.log' % name, 'w', 'utf-8')
        self.logger.addHandler(fh)

        # write to stdout
        # sh = logging.StreamHandler()
        # self.logger.addHandler(sh)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def log_time(self):
        now = datetime.now()
        self.logger.info(now.strftime("%H:%M:%S"))

    def start(self):
        self.info("Start Crawling")
        self.log_time()

    def end(self):
        self.log_time()
        self.info("Done Crawling")
