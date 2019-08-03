from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('ranklist/', views.ranklist_problem),
    path('ranklist/codeforces/', views.ranklist_codeforces),
    path('submission/', views.submission),
    path('user/', views.user),
    path('', views.dashboard),
]
