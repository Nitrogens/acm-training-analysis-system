import requests

from bs4 import BeautifulSoup


class Crawler:
    def __init__(self, username, verdict_list):
        self.username = username
        self.headers = {
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/75.0.3770.100 Safari/537.36",
        }
        self.submission_data_dict_key = ['oj_name', 'problem_id', 'time', 'verdict']
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

    def get_submission_data_dict(self, submission_data_dict_value):
        submission_data_dict = {}
        index = 0
        for value in submission_data_dict_value:
            submission_data_dict[self.submission_data_dict_key[index]] = submission_data_dict_value[index]
            index += 1
        return submission_data_dict

