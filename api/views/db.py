import json

from django.shortcuts import render
from django.http import JsonResponse, QueryDict
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from ..models import *
from crawler.VJudgeCrawler import VJudgeCrawler
from crawler.POJCrawler import POJCrawler
from crawler.HDOJCrawler import HDOJCrawler
from crawler.CodeforcesCrawler import CodeforcesCrawler


class CodeforcesRatingGetAction(View):
    def get(self, request):
        username = request.GET.get('username')
        if username is None:
            return JsonResponse({'message': 'Failed'})

        try:
            username_json = User.objects.get(username=username).oj_username
        except Exception:
            return JsonResponse({'message': 'Failed'})

        username_dict = json.loads(username_json)
        if username_dict.get('CodeForces') is not None:
            crawler = CodeforcesCrawler(username_dict['CodeForces'])
            rating = crawler.get_contest_rating()
            User.objects.filter(username=username).update(codeforces_rating=rating)

        return JsonResponse({'message': 'OK'})


class SubmissionGetAction(View):
    def get(self, request):
        username = request.GET.get('username')
        if username is None:
            return JsonResponse({'message': 'Failed'})

        try:
            username_json = User.objects.get(username=username).oj_username
        except Exception:
            return JsonResponse({'message': 'Failed'})

        username_dict = json.loads(username_json)
        submission_list = []
        try:
            for key, value in username_dict.items():
                if key == 'CodeForces':
                    crawler = CodeforcesCrawler(value)
                    submission_list += crawler.get_submission_data()
                elif key == 'VJudge':
                    crawler = VJudgeCrawler(value)
                    submission_list += crawler.get_submission_data()
                elif key == 'HDOJ':
                    crawler = HDOJCrawler(value)
                    submission_list += crawler.get_submission_data()
                elif key == 'POJ':
                    crawler = POJCrawler(value)
                    submission_list += crawler.get_submission_data()
        except Exception:
            return JsonResponse({'message': 'Failed'})

        try:
            Submission.objects.filter(user=User.objects.get(username=username)).delete()
        except Exception:
            return JsonResponse({'message': 'Failed'})

        for submission in submission_list:
            try:
                Submission.objects.create(user=User.objects.get(username=username), **submission)
            except Exception:
                JsonResponse({'message': 'Failed'})

        return JsonResponse({'message': 'OK'})