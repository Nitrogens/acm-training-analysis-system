from django.contrib import admin
from django.urls import path, include
from .views import db, ajax

urlpatterns = [
    path('db/codeforces/rating', db.CodeforcesRatingCrawAction.as_view()),
    path('db/codeforces/contest', db.UserCodeforcesContestCrawAction.as_view()),
    path('db/submission', db.UserSubmissionCrawAction.as_view()),
    path('ajax/submission', ajax.UserSubmissionGetAction.as_view()),
    path('ajax/oj_stat', ajax.UserOJStatisticGetAction.as_view()),
    path('ajax/verdict_stat', ajax.UserVerdictStatisticGetAction.as_view()),
    path('ajax/monthly_stat', ajax.UserMonthlyStatisticGetAction.as_view()),
]
