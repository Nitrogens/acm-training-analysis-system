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
from django.core.paginator import Paginator

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
            new_user.group = 1
            new_user.oj_username = request.POST.get('oj_username')
            new_user.codeforces_rating = 0
            new_user.save()
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Failed'})
        return JsonResponse({'message': 'OK'})

    def put(self, request):
        PUT = QueryDict(request.body)
        username = PUT.get('username')
        if username is None or username != request.session.get('username'):
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


class SubmissionGetAction(View):
    def get(self, request):
        page_size = 15
        page_id = 1
        try:
            param = {}
            order_param = "time"
            if request.GET.get('username') is not None:
                param['user'] = User.objects.get(username=request.GET.get('username'))
            if request.GET.get('verdict') is not None:
                param['verdict'] = int(request.GET.get('verdict'))
            if request.GET.get('order_by') is not None:
                order_param = request.GET.get('order_by')
            if request.GET.get('page_size') is not None:
                page_size = int(request.GET.get('page_size'))
            if request.GET.get('page_id') is not None:
                page_id = int(request.GET.get('page_id'))
            query_result = Submission.objects.filter(**param).order_by(order_param).reverse()
            paginator = Paginator(query_result, page_size)
            return_query_result = paginator.page(page_id)
            has_previous = return_query_result.has_previous()
            has_next = return_query_result.has_next()
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Failed', 'data': []})

        data_list = []
        for record in return_query_result:
            record_dict = {
                'id': record.id,
                'oj_name': record.oj_name,
                'problem_id': record.problem_id,
                'time': str(record.time),
                'verdict': record.verdict,
                'user': record.user.username,
            }
            data_list.append(record_dict)

        return JsonResponse({'message': 'OK',
                             'data': data_list,
                             'has_previous': int(has_previous),
                             'has_next': int(has_next),
                             'num_pages': paginator.num_pages,
                             })


class UserRanklistGetAction(View):
    def get(self, request):
        page_size = 15
        page_id = 1
        try:
            if request.GET.get('page_id') is not None:
                page_id = int(request.GET.get('page_id'))
            query_result = Submission.objects.filter(verdict=0).values('user__username').annotate(count=Count('id'))\
                .order_by('count').reverse()
            paginator = Paginator(query_result, page_size)
            return_query_result = paginator.page(page_id)
            has_previous = return_query_result.has_previous()
            has_next = return_query_result.has_next()
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Failed', 'data': []})

        data_list = []
        index = 0
        for record in return_query_result:
            record_dict = {
                'rank': return_query_result.start_index() + index,
                'username': record['user__username'],
                'count': record['count'],
            }
            data_list.append(record_dict)
            index += 1

        return JsonResponse({'message': 'OK',
                             'data': data_list,
                             'has_previous': int(has_previous),
                             'has_next': int(has_next),
                             'num_pages': paginator.num_pages,
                             })


class UserCodeforcesRatingRanklistGetAction(View):
    def get(self, request):
        page_size = 15
        page_id = 1
        try:
            if request.GET.get('page_id') is not None:
                page_id = int(request.GET.get('page_id'))
            query_result = User.objects.all().order_by('codeforces_rating').reverse()
            paginator = Paginator(query_result, page_size)
            return_query_result = paginator.page(page_id)
            has_previous = return_query_result.has_previous()
            has_next = return_query_result.has_next()
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Failed', 'data': []})

        data_list = []
        index = 0
        for record in return_query_result:
            record_dict = {
                'rank': return_query_result.start_index() + index,
                'username': record.username,
                'rating': int(record.codeforces_rating),
            }
            data_list.append(record_dict)
            index += 1

        return JsonResponse({'message': 'OK',
                             'data': data_list,
                             'has_previous': int(has_previous),
                             'has_next': int(has_next),
                             'num_pages': paginator.num_pages,
                             })


class UserCodeforcesContestGetAction(View):
    def get(self, request):
        username = request.GET.get('username')
        if username is None:
            return JsonResponse({'message': 'Failed', 'data': []})

        try:
            query_result = CodeforcesContest.objects.filter(user__username=username).order_by('contest_id')
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Failed', 'data': []})

        data_list = []
        for contest in query_result:
            record_dict = {
                'name': contest.name,
                'rank': contest.rank,
                'solved': contest.solved,
                'rating_change': contest.rating_change,
                'new_rating': contest.new_rating,
                'contest_id': contest.contest_id,
            }
            data_list.append(record_dict)

        return JsonResponse({'message': 'OK', 'data': data_list})


class MostPopularAcceptedProblemGetAction(View):
    def get(self, request):
        try:
            query_result = Submission.objects.filter(verdict=0).order_by("oj_name", "problem_id").reverse().values("oj_name", "problem_id").annotate(count=Count("id")).order_by("count")
            print(query_result.query)
            paginator = Paginator(query_result, 8)
            return_query_result = paginator.page(1)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Failed', 'data': []})

        data_list = []
        for record in return_query_result:
            record_dict = {
                'oj_name': record['oj_name'],
                'problem_id': record['problem_id'],
                'count': int(record['count']),
            }
            data_list.append(record_dict)

        return JsonResponse({'message': 'OK', 'data': data_list})


class SubmissionStatisticAction(View):
    def get(self, request):
        try:
            submission_today = Submission.objects.filter(time__day=datetime.datetime.now().day, time__month=datetime.datetime.now().month, time__year=datetime.datetime.now().year).count()
            accepted_submission_today = Submission.objects.filter(time__day=datetime.datetime.now().day, time__month=datetime.datetime.now().month, time__year=datetime.datetime.now().year, verdict=0).count()
            submission_total = Submission.objects.all().count()
            accepted_submission_total = Submission.objects.filter(verdict=0).count()
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Failed', 'data': []})

        data_dict = {
            'submission_today': submission_today,
            'accepted_submission_today': accepted_submission_today,
            'submission_total': submission_total,
            'accepted_submission_total': accepted_submission_total,
        }

        return JsonResponse({'message': 'OK', 'data': data_dict})


class UserStatisticAction(View):
    def get(self, request):
        username = request.GET.get('username')
        if username is None:
            return JsonResponse({'message': 'Failed', 'data': []})

        try:
            accepted_submission_total = Submission.objects.filter(verdict=0, user__username=username).count()
            codeforces_rating = User.objects.get(username=username).codeforces_rating
            problem_rank = Submission.objects.filter(verdict=0).values('user__username').annotate(count=Count('id'))\
                .filter(count__gt=accepted_submission_total).count() + 1
            codeforces_rating_rank = User.objects.filter(codeforces_rating__gt=codeforces_rating).count() + 1
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Failed', 'data': []})

        data_dict = {
            'accepted_submission_total': accepted_submission_total,
            'codeforces_rating': codeforces_rating,
            'problem_rank': problem_rank,
            'codeforces_rating_rank': codeforces_rating_rank,
        }

        return JsonResponse({'message': 'OK', 'data': data_dict})


class UserOJStatisticGetAction(View):
    def get(self, request):
        username = request.GET.get('username')
        if username is None:
            return JsonResponse({'message': 'Failed', 'data': []})

        try:
            query_result = Submission.objects.filter(user=User.objects.get(username=username), verdict=0)\
                .order_by('oj_name', 'problem_id').values('oj_name', 'problem_id')
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
                'verdict_id': int(key),
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
            query_result = Submission.objects.filter(user__username=username, verdict=0)\
                    .annotate(year=ExtractYear('time'), month=ExtractMonth('time')).values('year', 'month')\
                    .annotate(num=Count('id'))
            print(query_result.query)
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

        data_list.reverse()
        data_list = data_list[0:6]
        data_list.reverse()

        return JsonResponse({'message': 'OK', 'data': data_list})