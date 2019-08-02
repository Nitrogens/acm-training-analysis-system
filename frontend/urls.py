from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('ranklist/accepted', views.ranklist_accepted),
    path('ranklist/', views.ranklist_accepted),
    path('submission/', views.submission),
    path('user/', views.user),
    path('', views.dashboard),
]
