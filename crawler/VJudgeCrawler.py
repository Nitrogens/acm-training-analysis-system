import requests
import json
import datetime
import time

from bs4 import BeautifulSoup
from crawler.Crawler import Crawler


class VJudgeCrawler(Crawler):
    def __init__(self, username):
        verdict_list = ["AC", "WA", "TLE", "MLE",
                        "RE", "PE", "CE"]
        super(VJudgeCrawler, self).__init__(username, verdict_list)

    def get_submission_data(self):
        param = {
            'draw': '1',
            'start': '0',
            'length': '20',
            'search[value]': '',
            'search[regex]': 'false',
            'un': self.username,
            'OJId': 'All',
            'probNum': '',
            'res': '0',
            'language': '',
            'onlyFollowee': 'false',
            'orderBy': 'run_id',
        }
        for index in range(0, 10):
            param['columns[%d][data]' % index] = '0'
            param['columns[%d][name]' % index] = ''
            param['columns[%d][searchable]' % index] = 'true'
            param['columns[%d][orderable]' % index] = 'false'
            param['columns[%d][search][value]' % index] = ''
            param['columns[%d][search][regex]' % index] = 'false'
        is_finished = False
        start_index = 0
        return_list = []

        index = 1
        while not is_finished:
            param['start'] = str(start_index)
            response = requests.post("https://vjudge.net/status/data/", data=param)
            json_data = json.loads(response.text)
            for submission in json_data['data']:
                print("Fetching VJudge submission data %d..." % index)
                index += 1
                if submission['oj'] == 'Gym':
                    submission['oj'] = 'CodeForces'
                submission_data_dict_value = [submission['oj'],
                                              submission['probNum'],
                                              str(datetime.datetime.fromtimestamp(submission['time'] // 1000)),
                                              self.verdict_standardize(submission['statusCanonical'])]
                return_list.append(self.get_submission_data_dict(submission_data_dict_value))
            if len(json_data['data']) < 20:
                is_finished = True
            else:
                start_index += 20
            time.sleep(0.2)

        return return_list

