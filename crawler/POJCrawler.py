import requests
import json
import datetime
import time

from bs4 import BeautifulSoup
from crawler.Crawler import Crawler


class POJCrawler(Crawler):
    def __init__(self, username):
        verdict_list = ["Accepted", "Wrong Answer", "Time Limit Exceeded", "Memory Limit Exceeded",
                        "Runtime Error", "Presentation Error", "Compile Error"]
        super(POJCrawler, self).__init__(username, verdict_list)

    def get_submission_data(self):
        is_finished = False
        url = "http://poj.org/status?problem_id=&user_id=%s&result=&language=" % self.username
        return_list = []

        index = 1
        while not is_finished:
            response = requests.get(url, headers=self.headers)
            html_data = response.text
            page_soup = BeautifulSoup(html_data, 'lxml')
            submission_html = page_soup.select('tr[align=center]')
            navigation_html = page_soup.select('body p[align=center] a')
            url = "http://poj.org/" + navigation_html[2].attrs['href']
            for submission in submission_html:
                print("Fetching POJ submission data %d..." % index)
                index += 1
                line_soup = BeautifulSoup(str(submission), 'lxml')
                submission_data_list = line_soup.select('td')
                submission_data_dict_value = ["POJ",
                                              submission_data_list[2].text,
                                              submission_data_list[8].text,
                                              self.verdict_standardize(submission_data_list[3].text)]
                return_list.append(self.get_submission_data_dict(submission_data_dict_value))
            if len(submission_html) == 0:
                is_finished = True
            time.sleep(0.2)

        return return_list

