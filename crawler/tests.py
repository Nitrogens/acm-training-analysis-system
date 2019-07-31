from django.test import TestCase
from crawler.CodeforcesCrawler import CodeforcesCrawler
from crawler.HDOJCrawler import HDOJCrawler
from crawler.POJCrawler import POJCrawler
from crawler.VJudgeCrawler import VJudgeCrawler

codeforces = CodeforcesCrawler("touris")
print(codeforces.get_user_contest_data())
# codeforces_submission_data = codeforces.get_submission_data()
# for submission in codeforces_submission_data:
#     print(submission)
# print(codeforces.get_contest_rating())

# hdoj = HDOJCrawler("nitrogens")
# hdoj_submission_data = hdoj.get_submission_data()
# for submission in hdoj_submission_data:
#     print(submission)

# poj = POJCrawler("nitrogens")
# poj_submission_data = poj.get_submission_data()
# for submission in poj_submission_data:
#     print(submission)


# vjudge = VJudgeCrawler("nitrogens")
# vjudge_submission_data = vjudge.get_submission_data()
# for submission in vjudge_submission_data:
#     print(submission)