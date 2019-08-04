from django.shortcuts import render

from django.db.models.functions import *
from django.shortcuts import render
from django.http import JsonResponse, QueryDict, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count


def login_view(request):
    if request.session.get('is_login') is not None:
        return HttpResponseRedirect(reverse('frontend:index', args=()))

    return render(request, 'login.html', locals())


def register_view(request):
    if request.session.get('is_login') is not None:
        return HttpResponseRedirect(reverse('frontend:index', args=()))

    return render(request, 'register.html', locals())


def setting_view(request):
    if request.session.get('is_login') is None:
        return HttpResponseRedirect(reverse('frontend:index', args=()))

    return render(request, 'setting.html', locals())


def password_change_view(request):
    if request.session.get('is_login') is None:
        return HttpResponseRedirect(reverse('frontend:index', args=()))

    return render(request, 'password.html', locals())


def user_delete_view(request):
    if request.session.get('is_login') is None:
        return HttpResponseRedirect(reverse('frontend:index', args=()))

    return render(request, 'user_delete.html', locals())


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
