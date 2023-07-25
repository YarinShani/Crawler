import os
import requests
from configparser import ConfigParser
from models.logger import Logger
from utils.utils import get_valid_filename

num = 0
logger = Logger()

config = ConfigParser()
config.read("utils/config.cfg")


class UrlDownloader:
    def __init__(self, output_folder):
        self.output_folder = output_folder

    def download_page(self, url, depth):
        try:
            response = requests.get(url, headers={'User-Agent': config.get("configuration", "user_agent")})
            response.raise_for_status()

            return self.save_content(response.text, depth, url)
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
            return None
        except Exception as err:
            logger.error(f"Error occurred: {err}")
            return None

    def save_content(self, content, depth, url):
        global num
        global logger

        try:
            filename = os.path.join(self.output_folder, f"{depth}/{get_valid_filename(url)}.html")
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
                logger.info(f"saved file: {filename}, number: {num}, depth: {depth}")
                num += 1

            return content
        except Exception as e:
            logger.error("error: " + str(e))
            return None

