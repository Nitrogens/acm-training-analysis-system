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

    def get_contest_rating(self):
        response = requests.get("https://codeforces.com/api/user.info?handles=%s" % self.username)
        json_data = json.loads(response.text)
        if json_data['status'] != 'OK':
            return 0
        return int(json_data['result'][0]['rating'])

    def get_submission_data(self):
        response = requests.get("https://codeforces.com/api/user.status?handle=%s" % self.username, headers=self.headers)
        json_data = json.loads(response.text)
        if json_data['status'] != 'OK':
            return []
        return_list = []
        index = 1
        for submission in json_data['result']:
            print("Fetching CodeForces submission data %d..." % index)
            index += 1
            submission_data_dict_value = ["CodeForces",
                                          str(submission['contestId']) + submission['problem']['index'],
                                          str(datetime.datetime.fromtimestamp(submission['creationTimeSeconds'])),
                                          self.verdict_standardize(submission['verdict'])]
            return_list.append(self.get_submission_data_dict(submission_data_dict_value))
        return return_list

    def get_user_contest_data(self):
        response = requests.get("https://codeforces.com/contests/with/%s" % self.username, headers=self.headers)
        if response.url != "https://codeforces.com/contests/with/%s" % self.username:
            return []
        return_list = []
        html_data = response.text
        page_soup = BeautifulSoup(html_data, 'lxml')
        contest_list_html = page_soup.select('.user-contests-table tbody tr')
        for contest in contest_list_html:
            line_soup = BeautifulSoup(str(contest), 'lxml')
            column_data_list = line_soup.select('td')
            contest_data_dict = {
                'name': column_data_list[1].a.attrs['title'],
                'rank': int(column_data_list[2].text),
                'solved': int(column_data_list[3].text),
                'rating_change': int(column_data_list[4].text),
                'new_rating': int(column_data_list[5].text),
                'contest_id': int(column_data_list[0].text),
            }
            return_list.append(contest_data_dict)
        return return_list
