from django.db import models


class proflie(models.Model):
    address = models.TextField()
    tel = models.TextField()
    question1 = models.IntegerField()
    question2 = models.IntegerField()
    question3 = models.IntegerField()
    address2 = models.TextField()