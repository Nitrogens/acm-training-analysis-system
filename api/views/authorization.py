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
from api.models import *


def password_encrypt(password, salt='segmentation_fault'):
    hash_class = hashlib.sha256()
    password += salt
    hash_class.update(password.encode())
    return hash_class.hexdigest()


class UserLoginAction(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def get(self, request):
        if request.session.get('is_login') is not None:
            return JsonResponse({'message': 'Logged', 'username': request.session.get('username')})
        return JsonResponse({'message': 'Not logged'})

    def post(self, request):
        if request.session.get('is_login') is not None:
            return JsonResponse({'message': 'Logged'})

        username = request.POST.get('username')
        password = request.POST.get('password')
        if username is None or password is None:
            return JsonResponse({'message': 'Failed'})

        try:
            user_data = User.objects.get(username=username)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Failed'})

        if password_encrypt(password) != user_data.password:
            return JsonResponse({'message': 'Failed'})
        else:
            request.session['is_login'] = True
            request.session['username'] = username
            return JsonResponse({'message': 'OK'})


class UserLogoutAction(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def get(self, request):
        if request.session.get('is_login') is None:
            return JsonResponse({'message': 'Not logged'})

        request.session.flush()
        return JsonResponse({'message': 'OK'})


class UserPasswordChangeAction(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def get(self, request):
        return JsonResponse({'message': 'Failed'})

    def post(self, request):
        if request.session.get('is_login') is None:
            return JsonResponse({'message': 'Failed'})

        try:
            user_data = User.objects.filter(username=request.session.get('username'))
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Failed'})

        if password_encrypt(request.POST.get('current_password')) != user_data[0].password:
            return JsonResponse({'message': 'Failed'})

        try:
            user_data.update(password=password_encrypt(request.POST.get('new_password')))
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Failed'})

        return JsonResponse({'message': 'OK'})
