from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
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


class CodeforcesContest(models.Model):
    name = models.CharField(max_length=256)
    rank = models.IntegerField()
    solved = models.IntegerField()
    rating_change = models.IntegerField()
    new_rating = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="target_user")
    author_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_user")
    create_time = models.DateTimeField()
    edit_time = models.DateTimeField()
    text = models.TextField()
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
