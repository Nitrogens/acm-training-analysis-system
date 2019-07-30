import requests

from bs4 import BeautifulSoup


class Crawler:
    def __init__(self, username, verdict_list):
        self.username = username
        self.headers = {
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/75.0.3770.100 Safari/537.36",
        }
        self.mapping = {}
        index = 0
        for verdict in verdict_list:
            self.mapping[verdict] = index
            index += 1

    def verdict_standardize(self, verdict):
        value = self.mapping.get(verdict)
        if value is None:
            value = 7
        return value
