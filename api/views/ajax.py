import json

from collections import Counter

from django.db.models.functions import *
from django.shortcuts import render
from django.http import JsonResponse, QueryDict
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count

from ..models import *


def verdict_id_to_str(id):
    verdict_list = [
        'Accepted',
        'Wrong Answer',
        'Time Limit Exceeded',
        'Memory Limit Exceeded',
        'Runtime Error',
        'Presentation Error',
        'Compilation Error',
        'Other verdict'
    ]
    return verdict_list[id]


class UserSubmissionGetAction(View):
    def get(self, request):
        username = request.GET.get('username')
        if username is None:
            return JsonResponse({'message': 'Failed', 'data': []})

        try:
            query_result = Submission.objects.filter(user=User.objects.get(username=username)).order_by("time").reverse()
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Failed', 'data': []})

        data_list = []
        for record in query_result:
            record_dict = {
                'oj_name': record.oj_name,
                'problem_id': record.problem_id,
                'time': str(record.time),
                'verdict': verdict_id_to_str(record.verdict),
            }
            data_list.append(record_dict)

        return JsonResponse({'message': 'OK', 'data': data_list})


class UserOJStatisticGetAction(View):
    def get(self, request):
        username = request.GET.get('username')
        if username is None:
            return JsonResponse({'message': 'Failed', 'data': []})

        try:
            query_result = Submission.objects.filter(user=User.objects.get(username=username), verdict=0)\
                .order_by('oj_name', 'problem_id').values('oj_name', 'problem_id').distinct()
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Failed', 'data': []})

        oj_count = {}

        for record in query_result:
            if oj_count.get(record['oj_name']) is None:
                oj_count[record['oj_name']] = 1
            else:
                oj_count[record['oj_name']] += 1

        data_list = []
        for key, value in oj_count.items():
            record_dict = {
                'oj_name': key,
                'oj_count': value,
            }
            data_list.append(record_dict)

        return JsonResponse({'message': 'OK', 'data': data_list})


class UserVerdictStatisticGetAction(View):
    def get(self, request):
        username = request.GET.get('username')
        if username is None:
            return JsonResponse({'message': 'Failed', 'data': []})

        try:
            query_result = Submission.objects.filter(user=User.objects.get(username=username)).values('verdict')
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Failed', 'data': []})

        verdict_count = {}
        for record in query_result:
            if verdict_count.get(record['verdict']) is None:
                verdict_count[record['verdict']] = 1
            else:
                verdict_count[record['verdict']] += 1

        data_list = []
        for key, value in verdict_count.items():
            record_dict = {
                'verdict_name': verdict_id_to_str(key),
                'verdict_count': value,
            }
            data_list.append(record_dict)

        return JsonResponse({'message': 'OK', 'data': data_list})


class UserMonthlyStatisticGetAction(View):
    def get(self, request):
        username = request.GET.get('username')
        if username is None:
            return JsonResponse({'message': 'Failed', 'data': []})

        try:
            query_result = Submission.objects.filter(user=User.objects.get(username=username), verdict=0)\
                    .annotate(year=ExtractYear('time'), month=ExtractMonth('time')).values('year', 'month')\
                    .annotate(num=Count('id'))
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Failed', 'data': []})

        data_list = []
        for element in query_result:
            record_dict = {
                'time': "%04d-%02d" % (int(element['year']), int(element['month'])),
                'count': int(element['num']),
            }
            data_list.append(record_dict)

        return JsonResponse({'message': 'OK', 'data': data_list})