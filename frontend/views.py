from django.shortcuts import render

from django.db.models.functions import *
from django.shortcuts import render
from django.http import JsonResponse, QueryDict
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count


def dashboard(request):
    return render(request, 'dashboard.html', locals())


def ranklist_problem(request):
    return render(request, 'ranklist_problem.html', locals())

def ranklist_codeforces(request):
    return render(request, 'ranklist_codeforces.html', locals())


def submission(request):
    return render(request, 'submission.html', locals())


def user(request):
    return render(request, 'user_info.html', locals())
