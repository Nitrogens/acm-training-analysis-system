from django.contrib import admin
from django.urls import path, include
from .views import db

urlpatterns = [
    path('db/rating/codeforces', db.CodeforcesRatingGetAction.as_view()),
    path('db/submission', db.SubmissionGetAction.as_view()),
]
