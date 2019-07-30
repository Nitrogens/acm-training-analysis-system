import requests
import json
import datetime

from bs4 import BeautifulSoup
from crawler.Crawler import Crawler


class CodeforcesCrawler(Crawler):
    def __init__(self, username):
        verdict_list = ["OK", "WRONG_ANSWER", "TIME_LIMIT_EXCEEDED", "MEMORY_LIMIT_EXCEEDED",
                        "RUNTIME_ERROR", "PRESENTATION_ERROR", "COMPILATION_ERROR"]
        super(CodeforcesCrawler, self).__init__(username, verdict_list)
        self.rating = 0
        self.get_contest_rating()

    def get_contest_rating(self):
        response = requests.get("https://codeforces.com/api/user.info?handles=%s" % self.username)
        json_data = json.loads(response.text)
        if json_data['status'] != 'OK':
            return None
        self.rating = int(json_data['result'][0]['rating'])
        return self.rating

    def get_submission_data(self):
        response = requests.get("https://codeforces.com/api/user.status?handle=%s" % self.username)
        json_data = json.loads(response.text)
        if json_data['status'] != 'OK':
            return None
        return_list = []
        for submission in json_data['result']:
            submission_dict = {
                'oj_name': "CodeForces",
                'problem_id': str(submission['contestId']) + submission['problem']['index'],
                'username': self.username,
                'time': str(datetime.datetime.fromtimestamp(submission['creationTimeSeconds'])),
                'verdict': self.verdict_standardize(submission['verdict']),
            }
            return_list.append(submission_dict)
        return return_list

