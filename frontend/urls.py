from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'frontend'
urlpatterns = [
    path('ranklist/', views.ranklist_problem),
    path('ranklist/codeforces/', views.ranklist_codeforces),
    path('submission/', views.submission),
    path('user/', views.user),
    path('login/', views.login_view),
    path('register/', views.register_view),
    path('setting/', views.setting_view),
    path('setting/password/', views.password_change_view),
    path('setting/delete/', views.user_delete_view),
    path('', views.dashboard, name='index'),
]
