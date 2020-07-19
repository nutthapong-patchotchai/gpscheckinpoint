from django.db import models
from django.contrib.auth.models import User
from checkin.models.address import *

class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    geo = models.ForeignKey(Geography, on_delete=models.CASCADE)
    amphur = models.ForeignKey(Amphur, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, on_delete=models.CASCADE) 
    post = models.TextField()
    tel = models.TextField()
    question1 = models.IntegerField()
    question2 = models.IntegerField()
    question3 = models.IntegerField()
    address2 = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)