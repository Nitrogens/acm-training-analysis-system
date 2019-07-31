from django.db import models


class User(models.Model):
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=256)
    nickname = models.CharField(max_length=32, unique=True)
    email = models.CharField(max_length=200, unique=True)
    group = models.IntegerField()
    oj_username = models.TextField(null=True, blank=True)
    codeforces_rating = models.IntegerField(default=0)


class Submission(models.Model):
    oj_name = models.CharField(max_length=32)
    problem_id = models.CharField(max_length=128)
    time = models.DateTimeField()
    verdict = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="target_user")
    author_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_user")
    create_time = models.DateTimeField()
    edit_time = models.DateTimeField()
    text = models.TextField()
