import hashlib
import json
import datetime

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


def password_encrypt(password, salt='segmentation_fault'):
    hash_class = hashlib.sha256()
    password += salt
    hash_class.update(password.encode())
    return hash_class.hexdigest()


class UserAction(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def get(self, request):
        username = request.GET.get('username')
        if username is None:
            return JsonResponse({'message': 'Failed', 'data': []})

        try:
            user_data = User.objects.get(username=username)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Failed', 'data': []})

        return_dict = {
            'username': user_data.username,
            'nickname': user_data.nickname,
            'email': user_data.email,
            'group': 'User' if int(user_data.group) else 'Administrator',
            'oj_username': json.loads(user_data.oj_username),
            'codeforces_rating': int(user_data.codeforces_rating),
        }
        return JsonResponse({'message': 'OK', 'data': return_dict})

    def post(self, request):
        try:
            new_user = User()
            new_user.username = request.POST.get('username')
            new_user.password = password_encrypt(request.POST.get('password'))
            new_user.nickname = request.POST.get('nickname')
            new_user.email = request.POST.get('email')
            new_user.group = int(request.POST.get('group'))
            new_user.oj_username = request.POST.get('oj_username')
            new_user.codeforces_rating = int(request.POST.get('codeforces_rating'))
            new_user.save()
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Failed'})
        return JsonResponse({'message': 'OK'})

    def put(self, request):
        PUT = QueryDict(request.body)
        username = PUT.get('username')
        if username is None:
            return JsonResponse({'message': 'Failed'})

        try:
            user_data = User.objects.filter(username=username)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Failed'})

        param = {}
        for key, value in PUT.items():
            if key == 'password' or key == 'username':
                continue
            param[key] = value

        try:
            user_data.update(**param)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Failed'})

        return JsonResponse({'message': 'OK'})

    def delete(self, request):
        DELETE = QueryDict(request.body)
        username = DELETE.get('username')
        if username is None:
            return JsonResponse({'message': 'Failed'})

        try:
            user_data = User.objects.get(username=username)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Failed'})

        try:
            user_data.delete()
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Failed'})

        return JsonResponse({'message': 'OK'})


class CommentAction(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def get(self, request):
        username = request.GET.get('username')
        if username is None:
            return JsonResponse({'message': 'Failed', 'data': []})

        try:
            comment_data = Comment.objects.filter(target_user__username=username).order_by('create_time')
            print(comment_data.query)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Failed', 'data': []})

        return_list = []
        for comment in comment_data:
            print(comment)
            comment_dict = {
                'id': comment.id,
                'create_time': str(comment.create_time),
                'edit_time': str(comment.edit_time),
                'text': comment.text,
                'author_user': comment.author_user.username,
                'target_user': comment.target_user.username,
                'parent_comment_id': 0 if comment.parent_comment is None else comment.parent_comment.id,
            }
            return_list.append(comment_dict)

        return JsonResponse({'message': 'OK', 'data': return_list})

    def post(self, request):
        try:
            new_comment = Comment()
            new_comment.text = request.POST.get('text')
            new_comment.create_time = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
            new_comment.edit_time = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
            new_comment.author_user = User.objects.get(username=request.POST.get('author_user'))
            new_comment.target_user = User.objects.get(username=request.POST.get('target_user'))
            if request.POST.get('parent_comment_id') is not None:
                new_comment.parent_comment = Comment.objects.get(id=int(request.POST.get('parent_comment_id')))
            new_comment.save()
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Failed'})
        return JsonResponse({'message': 'OK'})

    def put(self, request):
        PUT = QueryDict(request.body)
        comment_id = PUT.get('id')
        if id is None:
            return JsonResponse({'message': 'Failed'})

        comment_id = int(comment_id)
        try:
            comment_data = Comment.objects.filter(id=comment_id)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Failed'})

        param = {}
        for key, value in PUT.items():
            if key == 'id' or key == 'parent_comment_id':
                continue
            param[key] = value

        param['edit_time'] = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")

        try:
            comment_data.update(**param)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Failed'})

        return JsonResponse({'message': 'OK'})

    def delete(self, request):
        DELETE = QueryDict(request.body)
        comment_id = DELETE.get('id')
        if comment_id is None:
            return JsonResponse({'message': 'Failed'})

        comment_id = int(comment_id)

        try:
            comment_data = Comment.objects.get(id=comment_id)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Failed'})

        try:
            comment_data.delete()
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Failed'})

        return JsonResponse({'message': 'OK'})


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