from django.contrib import admin
from django.urls import path, include
from .views import db, ajax

urlpatterns = [
    path('db/codeforces/rating/', db.CodeforcesRatingCrawAction.as_view()),
    path('db/codeforces/contest/', db.UserCodeforcesContestCrawAction.as_view()),
    path('db/submission/', db.UserSubmissionCrawAction.as_view()),
    path('user/', ajax.UserAction.as_view()),
    path('comment/', ajax.CommentAction.as_view()),
    path('submission/', ajax.SubmissionGetAction.as_view()),
    path('ranklist/', ajax.UserRanklistGetAction.as_view()),
    path('ranklist/codeforces/', ajax.UserCodeforcesRatingRanklistGetAction.as_view()),
    path('codeforces_contest/', ajax.UserCodeforcesContestGetAction.as_view()),
    path('stat/submission/', ajax.SubmissionStatisticAction.as_view()),
    path('stat/user/', ajax.UserStatisticAction.as_view()),
    path('stat/oj/', ajax.UserOJStatisticGetAction.as_view()),
    path('stat/verdict/', ajax.UserVerdictStatisticGetAction.as_view()),
    path('stat/monthly/', ajax.UserMonthlyStatisticGetAction.as_view()),
    path('stat/most_popular_problem/', ajax.MostPopularAcceptedProblemGetAction.as_view()),
]
